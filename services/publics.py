from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException,status, Depends
from conection import get_session
from model.usarios import Usuario, BaseCriarUsuario
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv()
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')
EXPIRATION_TIMER_MINUTES = int(getenv('EXPIRATION_TIMER_MINUTES')) # type: ignore
USER_ADMIN = getenv('USER_ADMIN')
SENHA_ADMIN = getenv('SENHA_ADMIN')

Rota_Publics = APIRouter()

def criar_token(id_user, role):
    #vai pega o tempo de agora e soma mas o tempo de EXPIRATION_TIMER_MINUTES
    dt_expi = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIMER_MINUTES)
    #o dic_info está configurado com base no site: https://www.jwt.io/
    dic_info = {'sub': str(id_user),'role':role ,'exp': dt_expi}
    #isso cria o jwt 
    jwt_codificado = jwt.encode(dic_info, SECRETES_KEY, ALG) # type: ignore
    return jwt_codificado

@Rota_Publics.post('/criar_usuario', tags=['Usuario'])
def criar_usario(base:BaseCriarUsuario, session: Session = Depends(get_session)):
    try:
        user = Usuario(base.nome, base.email,base.senha, 'cliente')
        session.add(user)
        session.commit()
        return {'mesagem': 'user criado com sucesso'}
    except IntegrityError:
        #restar a sessação da orm se não a proxima requizição feita vai usar 
        #o resto da sessação quebrada
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já há um usuario com esse email'
        )
    
#OAuth2PasswordRequestForm padrão do fastapi para fazer altenticação mas simples no /docs
@Rota_Publics.post('/logar_usuario')
def logar_usario(base: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    query_u = session.query(Usuario).filter_by(email = base.username).first()
    if query_u != None:
        if query_u.verificar_senha(base.password):
            _jwt = criar_token(query_u.id, query_u.role)
            # O retorno precisa ser assim para o /docs funcionar:
            return {
                "access_token": _jwt, 
                "token_type": "bearer"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='senha invalida'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user não encontrado/cadastrado'
        )

@Rota_Publics.get('/criar_admin', tags=['Admin'])
def criar_admin(session: Session = Depends(get_session)):
    '''ATENÇÃO O EMAIL E A SENHA DO AMIN SÃO DEFINIDAS NAS VAR DE ABIENTE(.env)'''
    try:
        user = Usuario(USER_ADMIN, USER_ADMIN, SENHA_ADMIN, 'adm')
        session.add(user)
        session.commit()
        return {'mesagem': 'admin criado com sucesso'}
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail='não pode der 2 user com a role de adm'
        )
    