from jose import jwt, JWTError
from fastapi import HTTPException,status, Depends
from fastapi.security import OAuth2PasswordBearer
from conection import get_session
from model.usarios import Usuario
from sqlalchemy.orm import Session
from config import SECRETES_KEY,ALG

#Base para trancar rota
oauth_schema = OAuth2PasswordBearer('/public/logar_usuario/')

def verificar_toke(token: str = Depends(oauth_schema)):
    try:
        #Decodifica o token para um dicionário
        dic_info_u = jwt.decode(token, str(SECRETES_KEY), ALG)
        
        return dic_info_u 
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='acesso negado'
        )

#A classe é melhor do que função nesse caso, pois ela retorna o ID já como int
    #e o Depends do FastAPI não aceitaria se fosse função dando o mesmo retorno
class RolePermitidas:
    def __init__(self, roles: list):
        self.roles_depedecia = roles

    #O __call__ me permite usar o objeto como se ele fosse uma função
    def __call__(self, user=Depends(verificar_toke), session: Session = Depends(get_session)): 
        query = session.query(Usuario).filter_by(role='adm').all()
        #O len vai garantir que só tem apenas um admi
        if len(query) <= 1:
            if user['role'] not in self.roles_depedecia :
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="você não tem permissão para acessar este recurso"
                )
            else:
                return int(user['sub'])
        else:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail='não pode der mais de 1 user com a role de adm'
            )


