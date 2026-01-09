from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus
from os import getenv
from dotenv import load_dotenv
import config

#leitura das ver de ambiente
load_dotenv()
IP_DB = getenv("IP_DB")
SENHA_DB = quote_plus(str(getenv("SENHA_DB")))
USER_DB = getenv("USER_DB")
BANCO_DB = getenv("BANCO_DB")
#tratamento para o int já que as var de ambiente são tratas como string automaticamente
PORTA_DB = int(getenv("PORTA_DB")) # type: ignore

endereco_db = None
if config.DEBUG == True and config.SQLITE == True:
    endereco_db = "sqlite:///banco.db"
else:  
    #Garante que a senha com caracteres especiais seja lida como senha,
        #não como parte do endereço. Sem o quote_plus, o SQLAlchemy pode interpretar
        #'@' como parte do endereço, e não da senha.
        endereco_db = f"mysql+pymysql://{USER_DB}:{SENHA_DB}@{IP_DB}:{PORTA_DB}/{BANCO_DB}"
    
try:
    #Cria a engine para conectar o python ao mysql
    engine = create_engine(endereco_db) 
    #Cria uma conxeção e depois fecha amesma conexeção
    engine.connect().close()
    #Esse erro acontece quando o SQLalchemy não consegue se conectar com a DB
except OperationalError:
    print('Servidor não consigui se conectar com o MysQLL.\n \
           Iniciando o o sqlite.')
    engine = create_engine("sqlite:///banco.db")

#Classe base para os modelos
Base = declarative_base()

#Cria a sessão para manipular a db
Session = sessionmaker(bind=engine)

#Garante que, ao usar a ORM como dependência, a sessão será fechada automaticamente
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
