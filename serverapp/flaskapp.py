from flask_openapi3                         import OpenAPI, Info, Tag
from flask                                  import redirect
from flask_cors                             import CORS

########################################################################################################
# Apresentação documentação API
########################################################################################################

info = Info(title="API do APP Free Games", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) 

########################################################################################################
# Definição das tags
########################################################################################################

home_tag    = Tag(name="Documentação",  description="Documentação padrão: Swagger")
game_tag    = Tag(name="Game",          description="Adição, edição, remoção e visualização dos games da lista do usuário")
usuario_tag = Tag(name="Usuario",       description="Adição, edição, autenticação e visualização do usuário")

########################################################################################################
# Redireciona para para /openapi estilo padrão da documentação : swagger
########################################################################################################

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela para visualização estilo padrão de documentação swagger.
    """
    return redirect('/openapi/swagger')