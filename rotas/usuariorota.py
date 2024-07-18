from datetime                               import datetime
from serverapp.flaskapp                     import *
from sqlalchemy.exc                         import IntegrityError
from operator                               import and_
from logger                                 import logger
from models.tabelas.usuario                 import Usuario
from models.tabelas.senha                   import Senha
from cripto.criptomd5                       import *
from schemas                                import *
from validador.usuariovalidador             import *  
from validador.senhavalidador               import *  
from database.operacao.database_manuseio    import DatabaseManuseio
from database.operacao.datatabase_operacao  import DatabaseOperacao

#################################################################################################################
#####                                       FUNÇÕES INTERNAS DA ROTA
#################################################################################################################

# Recupera id do usuário livre
def id_usuario_novo(dbmanuseio):
    
    idusuarionovo = dbmanuseio.get_select_max_value(Usuario.idusuario, None);
    if idusuarionovo:
        idusuarionovo +=1
    else: 
        idusuarionovo = 1

    return idusuarionovo                
    
# Verifica existência do id do usuário
def id_usuario_existe(dbmanuseio, idusuario):
    
    # variavel de retorno
    bexiste = False
    
    # verifica existência
    filtro      = Usuario.idusuario == idusuario
    resultcount = dbmanuseio.get_select_count_number(Usuario.idusuario, filtro)
    
    if resultcount > 0:
        bexiste = True
    
    return bexiste    

# Verifica existência do e-mail do usuário
def email_usuario_existe(dbmanuseio, idusuario, email):
    
    # variavel de retorno
    bexiste = False
    
    # verifica existência
    filtro      = and_(Usuario.idusuario != idusuario, Usuario.email == email)
    resultcount = dbmanuseio.get_select_count_number(Usuario.email, filtro)

    if resultcount > 0:
        bexiste = True
    
    return bexiste        

# Recupera senha da última vigência do usuário
def senha_usuario_ultima_vigencia(dbmanuseio, idusuariopwd, senhapwd, dtultimavigencia):
    return dbmanuseio.session.query(Senha).filter(and_(Senha.idusuariopwd == idusuariopwd, Senha.senhapwd == senhapwd)).\
                                           filter(Senha.dtvigenciapwd == dtultimavigencia).first()

# Adiciona novo registro na tabela de senhas do usuário                                           
def cria_senha(dbmanuseio, senha, autocommit):
    dbmanuseio.add_tabela(senha, autocommit)
        

#################################################################################################################
#####                                               ROTAS 
#################################################################################################################

# Buscar um determinado usuário
@app.get('/BuscaUsuario', tags=[usuario_tag],
         responses={"200": UsuarioVisualizaSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioIdBuscaSchema):
    """Efetua a busca do usuário a partir do id.

    Representação da forma de retorno do usuário.
    """
 
     # recupera objeto de manuseio de banco de dados
    dbmanuseio = DatabaseManuseio()
        
    # recupera id
    usuario_id = query.idusuario
    logger.info(f"Recuperando dados do usuário id {usuario_id}")
           
    # efetua busca no banco de dados
    usuario = dbmanuseio.get_select_first(Usuario, Usuario.idusuario == usuario_id)
        
    # critica se usuário não foi encontrado
    if not usuario:
        returnerrormesage = ReturnErrorMesage(f"Usuário id {usuario_id} não encontrado", "Busca Usuário na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 404
        
    # retorna a representação do usuário
    logger.info(f"usuario econtrado: {usuario}"  )

    return retorna_usuario(usuario);
    
# Adicionar um novo usuário    
@app.post('/AdicionaUsuario', tags=[usuario_tag],
          responses={"200": UsuarioVisualizaSchema, "400": ErrorSchema, "409": ErrorSchema})
def adicionar_usuario(body: UsuarioInsereBodySchema):
    """Adicionar um novo usuário à base de dados.

   Representação da forma de retorno de um usuário adicionado.
    """
    try:
        
        # valida informacoes recebidas do body UsuarioBodySchema
        validador   = UsuarioValidador(DatabaseOperacao().incluir, body)
        error_msg   = validador.mensagemvalidador
        
        if error_msg != "" and error_msg != None:
            logger.warning(f"Erro na solicitação para adicionar usuário {error_msg}.")
            return {"mesage": error_msg}, 400
        
        # recupera objeto de manuseio de banco de dados
        dbmanuseio = DatabaseManuseio()
        
        # critica duplicidade e-mail
        if email_usuario_existe(dbmanuseio, 0, body.email):
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage(f"E-mail {body.email} já cadastrado", "Erro de integridade na base de dados :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 409

        # recupera dados do usuário
        usuario = retorna_usuario_atualizado(True, body)    
        logger.info(f"Adicionando usuário de email: {body.email} nome {body.nome}.")

        # recupra novo id do usuário livre
        idusuarionovo     = id_usuario_novo(dbmanuseio)
        usuario.idusuario = idusuarionovo 

        # inicia variavel de transação
        booltransacaoiniciada = False;
        
        # adicionando cadastro do usuário 
        dbmanuseio.add_tabela(usuario, autocommit=False)
        logger.info(f"Adicionado cadastro do usuário: {usuario}")
        
        # após efetuar a inserção do usuário inicia transação
        booltransacaoiniciada = True;
        
        # criptografa senha 
        criptomd5 = CriptoMD5(body.senhapwd)        
        senhapwd  = criptomd5.get_cripto_md5();
    
        # adicionando senha do usuário
        senha = Senha(usuario.idusuario, senhapwd)
        logger.info(f"Adicionando senha usuário de email: {body.email} nome {body.nome}.")
        
        cria_senha(dbmanuseio, senha, False)
        logger.info(f"Senha do usuário e-mail {usuario.email} criada: {senha}.")
        
        # adicionando senha commit session
        dbmanuseio.commit_sessao();
        
        # retorna objeto    
        return retorna_usuario(usuario), 200

    except IntegrityError as e:
        # roolback transação se foi iniciada
        if booltransacaoiniciada == True:
            dbmanuseio.rollback_sessao();
        # duplicidade do e-mail pode ser uma razão do IntegrityError, porém já foi tratada no método
        returnerrormesage = ReturnErrorMesage(f"Erro de integridade ao adicionar usuário {usuario.nome}' e-mail {usuario.email}", "Erro de integridade na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 409

    except Exception as e:
        # roolback transação se foi iniciada
        if booltransacaoiniciada == True:
            dbmanuseio.rollback_sessao();
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto ao adicionar usuário {usuario.nome}", "Não foi possível salvar novo usuário :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400

# Editar um usuário    
@app.put('/EditaUsuario', tags=[usuario_tag],
          responses={"200": UsuarioVisualizaSchema, "400": ErrorSchema, "404": ErrorSchema, "400": ErrorSchema})
def editar_usuario(body: UsuarioBodyEditarSchema):
    """Editar um usuário já cadastrado.

    Representação da forma de solicitação e retorno de uma edição do cadastro do usuário.
    """   
    try:
        
        # valida informacoes recebidas do body UsuarioBodyEditarSchema
        validador   = UsuarioValidador(DatabaseOperacao().alterar, body)
        error_msg   = validador.mensagemvalidador
        
        if error_msg != "" and error_msg != None:
            logger.warning(f"Erro na solicitação de edição do usuário {error_msg}.")
            return {"mesage": error_msg}, 400
        
        # recupera objeto de manuseio de banco de dados
        dbmanuseio = DatabaseManuseio()
        
        # recupera objeto usuário com os dados originais no banco de dados 
        usuario_original = dbmanuseio.get_select_first(Usuario, Usuario.idusuario == body.idusuario)
        if not usuario_original:
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage(f"Usuário {body.nome}, e-mail {body.email} e id {body.idusuario} não encontrado", "Erro de solicitação na base de dados :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 404 

        # critica duplicidade e-mail
        if email_usuario_existe(dbmanuseio, body.idusuario, body.email):
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage(f"E-mail {body.email} já cadastrado", "Erro de integridade na base de dados :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 409
        
        # recupera objeto usuario alterando os dado originais com base do body passado na api
        usuario = retorna_usuario_atualizado( False, body, usuario_original=usuario_original)    
        filtro  = Usuario.idusuario == body.idusuario
        values  = {Usuario.email: body.email,           Usuario.nome: body.nome,               Usuario.cep: body.cep,\
                   Usuario.endereco: body.endereco,     Usuario.numero: body.numero,      Usuario.complemento: body.complemento,\
                   Usuario.bairro: body.bairro,         Usuario.cidade: body.cidade,      Usuario.uf: body.uf,\
                   Usuario.dtalteracao: datetime.now()}
        logger.info(f"Editando usuário de email: {body.email} nome {body.nome}.")

        # editando registro
        dbmanuseio.update_tabela(Usuario, filtro, values)
        logger.info(f"Editado usuário: {usuario}." )
            
        # retorna objeto
        return retorna_usuario(usuario), 200

    except IntegrityError as e:
        # duplicidade do e-mail pode ser uma razão do IntegrityError, porém já foi tratada no método
        returnerrormesage = ReturnErrorMesage(f"Erro integridade ao editar usuário {usuario.nome}' e-mail {usuario.email}", "Erro de integridade na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 409

    except Exception as e:
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto ao editar usuário {usuario.nome}", "Não foi possível salvar novo usuário :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400

# Autenticação do usuário
@app.post('/AutenticacaoUsuario', tags=[usuario_tag],
         responses={"200": SenhaAuthVisualizaSchema, "400": ErrorSchema, "404": ErrorSchema})
def get_autenticacao_usuario(body: SenhaInputAuthSchema):
    """Efetua a autenticação do usuário.

    Representação da forma de retorno da autenticação do usuário.
    """
    
    # Inicializa variáveis de autenticação
    situacaoauth = False
    mensagemauth = "Usuário não autenticado."
    
    # recupera objeto de manuseio de banco de dados
    dbmanuseio = DatabaseManuseio()

    # valida e-mail 
    if not Util.get_email_valido(body.emailpwd):
        # retorna mensagem de erro
        returnerrormesage = ReturnErrorMesage(f"E-mail {body.emailpwd} inválido", "Erro na autenticação do usuário :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400
       
            
    # criptografa senha 
    criptomd5 = CriptoMD5(body.senhapwd)        
    senhapwd  = criptomd5.get_cripto_md5()
    
    # recupera objeto usuário conforme e-mail query
    usuario = dbmanuseio.get_select_first(Usuario, Usuario.email == body.emailpwd)
        
    if not usuario:
        # retorna mensagem de erro
        returnerrormesage = ReturnErrorMesage("Usuário não encontrado", "Erro na autenticação do usuário :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 404
        
    # recupera ultima data de vigência da senha do usuário
    dtmaxvigencia = dbmanuseio.get_select_max_value(Senha.dtvigenciapwd, Senha.idusuariopwd == usuario.idusuario)
        
    if not dtmaxvigencia:
        # retorna mensagem de erro
        returnerrormesage = ReturnErrorMesage("Senha vigente do usuário não encontrada", "Erro na autenticação do usuário na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 404
        
    # recupera objeto senha do usuário conforme data da última vigência da senha o usuário
    senha = senha_usuario_ultima_vigencia(dbmanuseio, usuario.idusuario, senhapwd, dtmaxvigencia)
    logger.info(f"Recuperando dados da senha do usuário e-mail {body.emailpwd}.")
    
    if senha:
        situacaoauth = True  
        mensagemauth = "Usuário autenticado com sucesso."  
        logger.info(f"Usuário e-mail {body.emailpwd} autenticado com sucesso.")        
 
    # retorna autenticação
    return retorna_senha_autenticacao(usuario.idusuario, situacaoauth, mensagemauth);
