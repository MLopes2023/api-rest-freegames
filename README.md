### API Aplication Free Games

- Projeto seguindo o estilo REST, responsável pela autenticação e registro do usuário na aplicação Free Games, habilitando o acesso grátis a plataforma dos catálogos de games online, sendo possível jogar todos os games do catálogo e registrar, remover e comentar games em sua lista pessoal de favoritos.

- A api será consumida pelo front-end APP Free Games.

- Tecnologias adotadas:
 - [Python:3.9](https://www.python.org/downloads/release/python-390/)
 - [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - [OpenAPI3](https://swagger.io/specification/)

---
### Execução em ambiente de Desenvolvimento 

- Abrir o terminal na pasta da api da aplicação, onde se encontram os arquivo app.py e requirements.txt

- Criar um ambiente virtual

  python3 -m venv env
  
- Comandos para ativação do ambiente, conforme sistema operacional:

   - env\Scripts\Activate (Sistema Operacional Windows)

     Observação: 
     Antes deverá liberar a execução de script no PowerShell basta seguir os passos abaixo:
     - Va em pesquisar no menu do Windows 10 digite PowerShell e selecione o ícone clicando nele com o botão direito e clique em executar como Administrador.

    - Caso apareça uma janela com a seguinte mensagem “Deseja permitir que esse aplicativo faça alterações no seu dispositivo?”; clique em Sim.

    - No PowerShell digite o  comando abaixo e pressione enter:
      Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
      Será perguntado se deseja aceitar as mudanças, digite s e pressione enter para confirmar: digitar S.

 - source env/Scripts/Activate (Sistema Operacional Mac / Linux)

- Instalar as dependências necessárias para rodar o projeto com base no arquivo requirements.txt, conforme comando abaixo:

  pip install -r requirements.txt

- Levantando o servidor Flask: 

   flask run --host 0.0.0.0 --port 5000

   O serviço poderá ser acessado no browser no link http://127.0.0.1:5000/#/.

---

### Executar através do Docker

- É imprescindível ter o Docker instalado e iniciado em seu computador.

- Navegue para o diretório em que se encontram os arquivos Dockerfile e requirements.txt, executar como **administrador** o comando abaixo, para construção da imagem Docker:  

  docker build -t api-rest-freegames .

- No mesmo diretório executar como **administrador** o comando abaixo, para execução do container:  
  
  docker run -p 5000:5000 api-rest-freegames

- API disponível e basta abrir o http://localhost:5000/#/ no navegador.

- Caso haja a necessidade de **parar um conatiner**, basta executar os comandos: 

  Efetuar o comando **docker container ls --all** (vai retornar containers existentes para localização do ID do container para ser utilizado no comando abaixo):

  Efetuar o comando **docker stop CONTAINER_ID**, sendo CONTAINER_ID recuperado no comanddo anterior.

  --- 

### Documentação para consumo da API Free Games

O consumo da API terá permissão dos seguintes procedimentos e respectivos endpoints:

Os campos que forem opcionais no request serão informados na coluna de descrição do layout, e caso não informados serão obrigatórios por padrão.

1.Registra um novo usuário no APP Free Games.

**Rota do Método**

/AdicionaUsuario
POST

**Layout**


| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| email  |string| 150 | E-mail
| nome  |string| 100 | Nome completo
| cep  |string| 8 | Nº do Cep com 8 caracteres
| endereco  |string| 80 | Endereço
| numero  |string| 15 | Número
| complemento  |string| 50 | Complemento do endereço
| cidade  |string| 50 | Cidade
| bairro  |string| 50 | Bairro
| uf  |string| 2 | Estado
| senhapwd  |string| 10 | Senha do usuário com no mínimo 5 caracteres
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuario  |Integer|  | Código identificador do usuário
| email  |string| 150 | E-mail
| nome  |string| 100 | Nome completo
| cep  |string| 8 | CEP
| endereco  |string| 80 | Endereço
| numero  |string| 15 | Número
| complemento  |string| 50 | Complemento do endereço
| cidade  |string| 50 | Cidade
| bairro  |string| 50 | Bairro
| uf  |string| 2 | Estado
| senhapwd  |string| 10 | Senha do usuário
| dtcadastro  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracao  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| **RESPONSE 400, 409 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

2.Edita um usuário registrado no APP Free Games.

**Rota do Método**

/EditaUsuario
PUT

**Layout**

| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuario  |Integer|  | Código identificador do usuário
| email  |string| 150 | E-mail
| nome  |string| 100 | Nome completo
| cep  |string| 8 | Nº do Cep com 8 caracteres
| endereco  |string| 80 | Endereço
| numero  |string| 15 | Número
| complemento  |string| 50 | Complemento do endereço
| cidade  |string| 50 | Cidade
| bairro  |string| 50 | Bairro
| uf  |string| 2 | Estado
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuario  |Integer|  | Código identificador do usuário
| email  |string| 150 | E-mail
| nome  |string| 100 | Nome completo
| cep  |string| 8 | CEP
| endereco  |string| 80 | Endereço
| numero  |string| 15 | Número
| complemento  |string| 50 | Complemento do endereço
| cidade  |string| 50 | Cidade
| bairro  |string| 50 | Bairro
| uf  |string| 2 | Estado
| senhapwd  |string| 10 | Senha do usuário
| dtcadastro  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracao  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| **RESPONSE 400, 404, 409 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

3.Consulta os dados do cadastro de um usuário registrado no APP Free Games.

**Rota do Método**

/BuscaUsuario
GET

**Layout**

| **REQUEST QUERY**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuario  |Integer|  | Código identificador do usuário
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuario  |Integer|  | Código identificador do usuário
| email  |string| 150 | E-mail
| nome  |string| 100 | Nome completo
| cep  |string| 8 | CEP
| endereco  |string| 80 | Endereço
| numero  |string| 15 | Número
| complemento  |string| 50 | Complemento do endereço
| cidade  |string| 50 | Cidade
| bairro  |string| 50 | Bairro
| uf  |string| 2 | Estado
| senhapwd  |string| 10 | Senha do usuário
| dtcadastro  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracao  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| **RESPONSE 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

4.Autenticação do usuário no APP Free Games.

**Rota do Método**

/AutenticacaoUsuario
POST

**Layout**

| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| emailpwd  |string| 150 | E-mail do usuário registrado
| senhapwd  |string| 10 | Senha do usuário registrado
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuarioauth  |Integer|  | Código identificador do usuário autenticado
| mensagemauth  |string| 50 | Mensagem de autenticação efetuada ou rejeitada
| situacaoauth  |boolean|  | Retorna true (autenticação ok) ou false (autenticação não efetuada)
| **RESPONSE 400, 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

5.Adiciona um novo game na lista do usuário no APP Free Games.

**Rota do Método**

/AdicionaGameLista
POST

**Layout**

| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do catálogo da plataforma free games
| observacao  |string| 255 | Observação referente ao game ( Preencher com "" na ausência de informação)
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do catálogo da plataforma free games
| observacao  |string| 255 | Observação referente ao game ( Preencher com "" na ausência de informação)
| dtcadastro  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracao  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| **RESPONSE 400, 409 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem


6.Edita um game da lista do usuário já cadastrado no APP Free Games.

**Rota do Método**

/EditaGameLista
PUT

**Layout**

| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do catálogo da plataforma free games
| observacao  |string| 255 | Observação referente ao game ( Preencher com "" na ausência de informação)
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do catálogo da plataforma free games
| observacao  |string| 255 | Observação referente ao game ( Preencher com "" na ausência de informação)
| dtcadastro  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracao  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| **RESPONSE 400, 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

7.Remove um game da lista do usuário já cadastrado no APP Free Games.

**Rota do Método**

/RemoveGameLista
DELETE

**Layout**

| **REQUEST BODY JSON**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do usuário
| observacao  |string| 255 | Observação referente ao game ( Preencher com "" na ausência de informação)
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem game removido com sucesso
| **RESPONSE 400, 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

8.Busca um game da lista do usuário cadastrado no APP Free Games.

**Rota do Método**

/BuscaGameLista
GET

**Layout**

| **REQUEST QUERY**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game do da lista do usuário
| **RESPONSE 200 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game da lista do usuário
| observacao  |string| 255 | Observação
| dtcadastrogame  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracaogame  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| titulo  |string| 255 | Título do game
| capa  |string| 200 | Capa do game
| descricao  |string| 300 | Descrição do game
| urlgame  |string| 255 | Url do game
| genero  |string| 30 | Gênero do game
| plataforma  |string| 30 | Plataforma do game
| urlgameperfil  |string| 255 | Url do perfil do game
| dtlancamento  |string| 19 | Data do lançamento do game no formato "YYYY-MM-DD"
| **RESPONSE 400, 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem

9.Busca uma lista de games do usuário cadastrados no APP Free Games.

**Rota do Método**

/BuscaGamesLista
GET

**Layout**

| **REQUEST QUERY**||||
| -- | --| --| --|
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado (campo obrigatório)
| liketitulo  |string| 50 | Parte do título o game (campo opcional)
| **RESPONSE 200 LISTA freetogames JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| idusuariogame  |integer| | Id do usuário autenticado
| idgame  |integer|  | Id do game da lista do usuário
| observacao  |string| 255 | Observação
| dtcadastrogame  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| dtalteracaogame  |string| 19 | Data do cadastro no formato "YYYY-MM-DD HH:MM:SS"
| titulo  |string| 255 | Título do game
| capa  |string| 200 | Capa do game
| descricao  |string| 300 | Descrição do game
| urlgame  |string| 255 | Url do game
| genero  |string| 30 | Gênero do game
| plataforma  |string| 30 | Plataforma do game
| urlgameperfil  |string| 255 | Url do perfil do game
| dtlancamento  |string| 19 | Data do lançamento do game no formato "YYYY-MM-DD"
| **RESPONSE 400, 404 JSON**||||
| CAMPO | TIPO | TAMANHO | DESCRICAO |
| mesage  |string| 255 | Mensagem
