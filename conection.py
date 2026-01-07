from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from os import getenv

#leitura das ver de abiente
load_dotenv()
IP_DB = getenv("IP_DB")
SENHA_DB = getenv("SENHA_DB")
USER_DB = getenv("USER_DB")
BANCO_DB = getenv("BANCO_DB_DB")
#tratamento para o int já que as var de abiente são tratas com string automaticamente
PORTA_DB = int(getenv("PORTA_DB")) # type: ignore

ENDERECO_DB = f"mysql+pymysql://{USER_DB}:{SENHA_DB}@{IP_DB}:{PORTA_DB}/{BANCO_DB}"

#criação da engine para conectar o "python com mysql"
engine = create_engine(ENDERECO_DB)

#classe base para os modelos
Base = declarative_base()
