from sqlalchemy_utils           import database_exists, create_database
from sqlalchemy.orm             import sessionmaker
from sqlalchemy                 import create_engine

# importando os elementos definidos no modelo
from models.base                import Base
from database.ini.Database_Ini  import Database_Ini

# importa tabelas
from models.tabelas.usuario     import Usuario
from models.tabelas.senha       import Senha
from models.tabelas.game        import  Game

# recupera url de acesso ao banco de dados padrão do arquivo ini
db_config = Database_Ini()
db_url = db_config.get_url_db()
# print("DEBUG url acesso banco %s " %db_url)

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# Cria tabelas não existentes no banco
Base.metadata.create_all(engine)
