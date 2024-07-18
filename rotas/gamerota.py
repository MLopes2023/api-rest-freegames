import  json
import  requests
from datetime                               import datetime
from serverapp.flaskapp                     import *
from sqlalchemy.exc                         import IntegrityError
from operator                               import and_
from logger                                 import logger
from models.tabelas.game                    import Game
from rotas.usuariorota                      import *
from schemas                                import *
from configuracao.apiexterna                import ConfigApiExterna
from validador.gamevalidador                import *  
from database.operacao.database_manuseio    import DatabaseManuseio
from database.operacao.datatabase_operacao  import DatabaseOperacao

#################################################################################################################
#####                                       FUNÇÕES INTERNAS DA ROTA
#################################################################################################################


# Verifica existência do game na lista do usuário
def game_existe_minha_lista(dbmanuseio, idusuariogame, idgame):
    
    # variavel de retorno
    bexiste = False
    
    # verifica existência
    filtro      = and_(Game.idusuariogame == idusuariogame, Game.idgame == idgame)
    resultcount = dbmanuseio.get_select_count_number(Game.idgame, filtro)

    if resultcount > 0:
        bexiste = True
    
    return bexiste   

# Busca um único game da lista do usuário
def busca_game_usuario(dbmanuseio, idusuariogame, idgame):
    
    filtro = and_(Game.idusuariogame == idusuariogame, Game.idgame == idgame)
    return dbmanuseio.get_select_first(Game, filtro)

# Recupera game da api-externa acessando a api FreeToGame
def busca_free_to_game_response(idgame):
    
    # recupera url 
    config      = ConfigApiExterna("api-externa")
    url         = config.get_url_api_externa() + "/BuscaFreeToGame?idgame={}"
    urlrequest  = url.format(idgame)
    
    # Requisição para a api-externa para recuperar os dados da apiFreeToGame
    responsereq = requests.get(urlrequest)
    logger.info(f"Requisição dos dados do game id: {idgame}")
    
    # Verfica ocorrência de erro para ser tratada no método responsável pela chamada 
    if responsereq.status_code == 400:
        return 400
    elif responsereq.status_code == 404:
        return 404

    # Resposta da requsição
    dadosresponse = None
    if responsereq.status_code == 200:
        logger.info(f"Carregando informações do game id: {idgame}")
        dadosresponse = json.loads(responsereq.text)
       
        # Retorna dicionário com os dados do game
        logger.info(f"Game id {idgame} econtrado")
        return json.loads(responsereq.text)       

#################################################################################################################
#####                                               ROTAS 
#################################################################################################################


@app.get('/BuscaGameLista', tags=[game_tag],
         responses={"200": FreeToGameBodySchema, "400": ErrorSchema, "404": ErrorSchema})
def busca_game_lista_usuario(query: FreeToGameIdBuscaSchema):
    """Buscar um game da lista do usuário conforme id's do game e usuário

    Retorna uma representação de um game da lista do usuário.
    """
    
    try:
        
        # Recupera ids
        idusuariogame = query.idusuariogame
        idgame        = query.idgame
            
        # recupera objeto de manuseio de banco de dados
        dbmanuseio   = DatabaseManuseio()
        
        # recupera game da lista do usuário
        filtro  = and_(Game.idusuariogame == idusuariogame, Game.idgame == idgame)
        game = dbmanuseio.get_select_first(Game, filtro)    
        
        if not game:
           logger.info(f"Game id {idgame} da lista do usuário id {idusuariogame} não econtrado")
           return {}, 200     
        else:
             # recupera dados do game da api-externa
            freetogameresponse = busca_free_to_game_response(idgame)
            logger.debug(f"Recuperando dados do game id: {idgame} da api externa")

            # Verfica ocorrência de erro e existência do game na api externa FreeToGame
            if freetogameresponse == 400:
                returnerrormesage = ReturnErrorMesage("Ocorreu um erro na chamada da FreeToGame API", "Erro na resposta de busca do game :/" )
                logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
                return {"mesage": returnerrormesage.mesage + "."}, 400
            elif freetogameresponse == 404:
                returnerrormesage = ReturnErrorMesage(f"Game id {idgame} não encontrado", "Erro na resposta de busca do game :/" )
                logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg   }")
                return {"mesage": returnerrormesage.mesage + "."}, 404                
            
            # Cria um novo objeto FreeToGame model anexado os dados da freetoGame response com o objeto game
            objfreetogame = retorna_game_freeetogame_atualizado(game, freetogameresponse )

            logger.info(f"Game id {idgame} da lista do usuário id {idusuariogame} econtrado")
            return retorna_game_freeetogame(objfreetogame), 200     

    except Exception as e:
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto na busca game id {idusuariogame} usuário id {idusuariogame}", "Não foi possível efetuar a busca do game :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400


@app.get('/BuscaGamesLista', tags=[game_tag],
         responses={"200": ListaFreeToGames, "400": ErrorSchema, "404": ErrorSchema})
def busca_games_lista_usuario(query: FreeToGameIdTituloBuscaSchema):
    """Buscar um lista de games do usuário, pelo usuário ou ou parte do título.
    
    Retorna uma representação de uma lista de games do usuário.
    """
    
    try:
        
        # Recupera ids
        idusuariogame   = query.idusuariogame
        liketitulo      = None
        
        if query.liketitulo:
            liketitulo  = query.liketitulo
            
        # recupera objeto de manuseio de banco de dados
        dbmanuseio   = DatabaseManuseio()
        
        # recupera lista de games do usuário
        filtro  = Game.idusuariogame == idusuariogame
        games   = dbmanuseio.get_select_all(Game, filtro)    
        
        if len(games) == 0:
           logger.info(f"Games da lista do usuário id {idusuariogame} não econtrados")
           return {"freetogames": []}, 200     
        else:
            listobjfreetogame = []              
            for game in games:
            
                # recupera dados dos games do usuário da api-externa
                freetogameresponse = busca_free_to_game_response(game.idgame)
                logger.debug(f"Recuperando dados do game id: {game.idgame} da api externa")

                # Verfica ocorrência de erro e existência do game na api externa FreeToGame
                if freetogameresponse == 400:
                    returnerrormesage = ReturnErrorMesage("Ocorreu um erro na chamada da FreeToGame API", "Erro na resposta de busca do game :/" )
                    logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
                    return {"mesage": returnerrormesage.mesage + "."}, 400
                elif freetogameresponse == 404:
                    returnerrormesage = ReturnErrorMesage(f"Game id {game.idgame} não encontrado", "Erro na resposta de busca do game :/" )
                    logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg   }")
                    return {"mesage": returnerrormesage.mesage + "."}, 404                
               
                # Anexa os dados do objeto game ao objeto FreeToGame com base no freetoGame response retornada pela api externa
                if liketitulo is None:
                    listobjfreetogame.append(retorna_game_freeetogame_atualizado(game, freetogameresponse ))
                elif liketitulo.upper().strip() in freetogameresponse['titulo'].upper().strip(): 
                    listobjfreetogame.append(retorna_game_freeetogame_atualizado(game, freetogameresponse ))
            
            # retorna lista 
            if len(listobjfreetogame) == 0:
                return {"freetogames": []}, 200 
            else:
                logger.info(f"Lista de {len(listobjfreetogame)} game(s) do usuário id {idusuariogame} econtrada(s)")
                return retorna_games_freeetogame(listobjfreetogame), 200     

    except Exception as e:
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto na busca da lista de games do usuário id {idusuariogame}", "Não foi possível efetuar a busca do game :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400
    
# Adicionar um novo game na lista
@app.post('/AdicionaGameLista', tags=[game_tag],
          responses={"200": GameVisualizaSchema, "400": ErrorSchema, "404": ErrorSchema, "409": ErrorSchema})
def adiciona_game_lista_usuario(body: GameBodySchema):
    """Adicionar um novo game na lista do usuário.

   Representação da forma de retorno do game inserido na lista do usuário.
    """
    try:
        
        # valida informacoes recebidas no body
        validador   = GameValidador(body)
        error_msg   = validador.mensagemvalidador
        
        if error_msg != "" and error_msg != None:
            logger.warning(f"Erro na solicitação para adicionar game na lista do usuário {error_msg}.")
            return {"mesage": error_msg}, 400
        
        # recupera objeto de manuseio de banco de dados
        dbmanuseio = DatabaseManuseio()

        # critica não existência do usuário
        if not id_usuario_existe(dbmanuseio, body.idusuariogame):
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage("Usuário não encontrado no cadastro.", "Erro de na solicitação :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 404
        
        # critica duplicidade do game na lista do usuário
        if game_existe_minha_lista(dbmanuseio, body.idusuariogame, body.idgame):
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage("Game já cadastrado na lista do usuário", f"Erro de integridade na base de dados id usuário {body.idusuariogame} id game {body.idgame}:/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 409

        # recupera dados do game da api-externa
        freetogameresponse = busca_free_to_game_response(body.idgame)

        # Verfica ocorrência de erro e existência do game na api externa FreeToGame
        if freetogameresponse == 400:
            returnerrormesage = ReturnErrorMesage("Ocorreu um erro na chamada da FreeToGame API", "Erro na resposta de busca do game :/" )
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 400
        elif freetogameresponse == 404:
            returnerrormesage = ReturnErrorMesage(f"Game id {body.idgame} não encontrado", "Erro na resposta de busca do game :/" )
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg   }")
            return {"mesage": returnerrormesage.mesage + "."}, 404

        # recupera dados do game
        game = retorna_game_atualizado(True, body)    
        logger.info(f"Adicionando game id: {body.idgame} id usuário {body.idusuariogame}.")

        # adicionando cadastro do game
        dbmanuseio.add_tabela(game)
        logger.info(f"Adicionado cadastro do game: {game}")
        
        # retorna objeto    
        return retorna_game(game), 200

    except IntegrityError as e:
        # duplicidade do e-mail pode ser uma razão do IntegrityError, porém já foi tratada no método
        returnerrormesage = ReturnErrorMesage(f"Erro de integridade ao adicionar id usuário {body.idusuariogame}' game {body.idusuariogame} na lista", "Erro de integridade na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 409

    except Exception as e:
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto ao adicionar usuário id {body.idusuariogame}  game id {body.idusuariogame} na lista", "Não foi possível salvar novo game :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400
    
# Editar um game da lista do usuário
@app.put('/EditaGameLista', tags=[game_tag],
          responses={"200": GameVisualizaSchema, "400": ErrorSchema, "404": ErrorSchema})
def edita_game_lista_usuario(body: GameBodySchema):
    """Editar um game da lista do usuário já cadastrado.

    Representação da forma de solicitação e retorno de uma edição do cadastro do game do usuário.
    """   
    try:
        
        # valida informacoes recebidas do body GameBodySchema
        validador   = GameValidador(body)
        error_msg   = validador.mensagemvalidador
        
        if error_msg != "" and error_msg != None:
            logger.warning(f"Erro na solicitação de edição do game do usuário {error_msg}.")
            return {"mesage": error_msg}, 400
        
        # recupera objeto de manuseio de banco de dados
        dbmanuseio = DatabaseManuseio()

        # critica não existência do usuário
        if not id_usuario_existe(dbmanuseio, body.idusuariogame):
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage("Usuário não encontrado no cadastro.", "Erro de na solicitação :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 404
        
        # recupera dados do game na api-externa FreeToGame para criticar não existência do game na plataforma
        freetogameresponse = busca_free_to_game_response(body.idgame)

        # Verfica ocorrência de erro e existência do game na api externa FreeToGame
        if freetogameresponse == 400:
            returnerrormesage = ReturnErrorMesage("Ocorreu um erro na chamada da FreeToGame API", "Erro na resposta de busca do game :/" )
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 400
        elif freetogameresponse == 404:
            returnerrormesage = ReturnErrorMesage(f"Game id {body.idgame} não encontrado", "Erro na resposta de busca do game :/" )
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg   }")
            return {"mesage": returnerrormesage.mesage + "."}, 404
        
        # recupera objeto game do usuário com os dados originais no banco de dados 
        game_original = busca_game_usuario(dbmanuseio, body.idusuariogame, body.idgame)
        if not game_original:
            # retorna mensagem de erro
            returnerrormesage = ReturnErrorMesage(f"Game id {body.idgame} usuário id {body.idusuariogame} não encontrado", "Erro de solicitação na base de dados :/")
            logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
            return {"mesage": returnerrormesage.mesage + "."}, 404 
      
        # recupera objeto game do usuario alterando os dado originais com base do body passado na api
        game    = retorna_game_atualizado( False, body, game_original=game_original)    
        filtro  = and_(Game.idusuariogame == body.idusuariogame, Game.idgame == body.idgame)
        values  = {Game.observacao: body.observacao,            Game.dtalteracaogame: datetime.now()}
        logger.info(f"Editando game id {body.idusuariogame} do usuário id : {body.idgame}.")

        # editando registro
        dbmanuseio.update_tabela(Game, filtro, values)
        logger.info(f"Editado game id {body.idusuariogame} do usuário id : {body.idgame}." )
            
        # retorna objeto
        return retorna_game(game), 200

    except IntegrityError as e:
        # Erro de integridade do IntegrityError
        returnerrormesage = ReturnErrorMesage(f"Erro integridade ao editar game id {body.idusuariogame} do usuário id : {body.idgame}", "Erro de integridade na base de dados :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 409

    except Exception as e:
        # exceção fora do previsto
        returnerrormesage = ReturnErrorMesage(f"Erro fora do previsto ao editar game id {body.idusuariogame} do usuário id : {body.idgame}", "Não foi possível salvar novo usuário :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400


@app.delete('/RemoveGameLista', tags=[game_tag],
            responses={"200": GameDeleteSchema, "400": ErrorSchema, "404": ErrorSchema})
def remove_game_lista_usuario(query: GameDeleteIdBuscaSchema):
    """Remove um game da lista do usuário conforme id's do usuário e game informados.

    Retorna uma mensagem de confirmação da remoção.
    """
    # Recupe ids para remoção
    idgame        = query.idgame
    idusuariogame = query.idusuariogame
    
    # Recupera objeto de manuseio de banco de dados
    dbmanuseio = DatabaseManuseio()

    # critica não existência do usuário
    if not id_usuario_existe(dbmanuseio, idusuariogame):
        # retorna mensagem de erro
        returnerrormesage = ReturnErrorMesage("Usuário não encontrado no cadastro.", "Erro de na solicitação :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 404
        
    # recupera dados do game na api-externa FreeToGame para criticar não existência do game na plataforma
    freetogameresponse = busca_free_to_game_response(idgame)

    # Verfica ocorrência de erro e existência do game na api externa FreeToGame
    if freetogameresponse == 400:
        returnerrormesage = ReturnErrorMesage("Ocorreu um erro na chamada da FreeToGame API", "Erro na resposta de busca do game :/" )
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 400
    elif freetogameresponse == 404:
        returnerrormesage = ReturnErrorMesage(f"Game id {idgame} não encontrado", "Erro na resposta de busca do game :/" )
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg   }")
        return {"mesage": returnerrormesage.mesage + "."}, 404

    # Critica não existência do game na lista do usuário
    if not game_existe_minha_lista(dbmanuseio, idusuariogame, idgame):
        # retorna mensagem de erro
        returnerrormesage = ReturnErrorMesage("Game não faz parte da lista do usuário lista do usuário", f"Erro na busca do game id {idgame} usuário id{idusuariogame} :/")
        logger.warning(f"{returnerrormesage.mesage}, {returnerrormesage.error_msg}")
        return {"mesage": returnerrormesage.mesage + "."}, 404

    # Remove game da lista do usuário
    logger.info(f"Deletando game id {idgame} da lista do usuário id {idusuariogame}")
    
    # removendo registro
    filtro  = and_(Game.idusuariogame == idusuariogame, Game.idgame == idgame)
    count   = dbmanuseio.del_tabela(Game, filtro)
    logger.info(f"Removendo game id: {idusuariogame} do usuário id: {idgame}." )

    if count:
        # retorna representação de confirmação da mensagem
        logger.info(f"Deletado game id {idgame} da lista do usuário id: {idusuariogame}")
        return {"mesage": "Game removido da lista do usuário."}, 200
    else:
        # se o game não foi encontrado
        error_msg = "Game da lista do usuário não encontrado na base :/"
        logger.warning(f"Erro ao deletar game id: {idgame} da lista do usuário id: {idusuariogame}, {error_msg}")
        return {"mesage": error_msg}, 404
    

    
    

