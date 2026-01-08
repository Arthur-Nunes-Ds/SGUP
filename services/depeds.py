from jose import jwt, JWTError
from fastapi import HTTPException,status, Depends
from dotenv import load_dotenv
from os import getenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')

oauth_schema = OAuth2PasswordBearer('/usuario/logar_usuario')

def verificar_toke(token: str = Depends(oauth_schema)):
    try:
        dic_info_u = jwt.decode(token, str(SECRETES_KEY), ALG)
        id_user = dic_info_u.get('sub')
        return int(id_user) # type: ignore
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Acesso Negado'
        )
    