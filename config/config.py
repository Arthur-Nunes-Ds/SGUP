import json
from pathlib import Path
from urllib.parse import quote_plus
from os import getenv
from dotenv import load_dotenv

#leitura das var de ambiente
load_dotenv()

#SECTION - db
IP_DB = getenv("IP_DB")
SENHA_DB = quote_plus(str(getenv("SENHA_DB")))
USER_DB = getenv("USER_DB")
BANCO_DB = getenv("BANCO_DB")
#tratamento para o int já que as var de ambiente são tratas como string automaticamente
PORTA_DB = int(getenv("PORTA_DB")) # type: ignore

#SECTION - jwt
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')
EXPIRATION_TIMER_MINUTES = int(getenv('EXPIRATION_TIMER_MINUTES'))# type: ignore

#SECTION - admin
USER_ADMIN = getenv('USER_ADMIN')
SENHA_ADMIN = getenv('SENHA_ADMIN')

#SECTION - agr
#valores padrão
DEBUG = False
SQLITE = False
HOST_FRONT = ['*']

#tenta ler do arquivo temporário
config_file = Path('config/.sgu_config.json')
if config_file.exists():
    with open(config_file, 'r') as f:
        dados = json.load(f)
        DEBUG = dados.get('DEBUG')
        SQLITE = dados.get('SQLITE')
        HOST_FRONT = dados.get('HOST_FRONT')

