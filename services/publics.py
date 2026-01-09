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
EXPIRATION_TIMER_MINUTES = int(getenv('EXPIRATION_TIMER_MINUTES')) #type: ignore
USER_ADMIN = getenv('USER_ADMIN')
SENHA_ADMIN = getenv('SENHA_ADMIN')

Rota_Publics = APIRouter()

def criar_token(id_user, role):
    #Obtém o tempo atual e adiciona o tempo de expiração
    dt_expi = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIMER_MINUTES)
    #O dic_info está configurado com base no padrão JWT: https://www.jwt.io/
    dic_info = {'sub': str(id_user),'role': role,'exp': dt_expi}
    #Cria o JWT
    jwt_codificado = jwt.encode(dic_info, SECRETES_KEY, ALG)#type: ignore
    return jwt_codificado

#SECTION - Criar Cliente
@Rota_Publics.post('/criar_cliente', tags=['Cliente'])
def criar_cliente(base:BaseCriarUsuario, session: Session = Depends(get_session)):
    """\nCria um novo cliente no sistema.\
        \nPara criar um cliente, informe os dados na requisição.\
        \nParâmetros:\
        \n-nome : str \
        \n-email : str \
        \n-senha : str\
        \nRetorno:\
        \n-{"mensagem": "cliente criado com sucesso."}.\
        \nErros:\
        \n-409: Já existe um cliente com esse email."""
    try:
        user = Usuario(base.nome, base.email,base.senha, 'cliente')
        session.add(user)
        session.commit()
        return {'mensagem': 'cliente criado com sucesso'}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já existe um cliente com esse email'
        )

#SECTION - Cria Admin
@Rota_Publics.get('/criar_admin', tags=['Admin'])
def criar_admin(session: Session = Depends(get_session)):
    '''\nCria o usuário administrador do sistema.\
        \nATENÇÃO: O email e a senha do admin são definidos nas variáveis de ambiente (.env).\
        \nRetorno:\
        \n-{"mensagem": "admin criado com sucesso."}.\
        \nErros:\
        \n-423: Não pode existir mais de um usuário com a role de admin.'''
    try:
        user = Usuario(USER_ADMIN, USER_ADMIN, SENHA_ADMIN, 'adm')
        session.add(user)
        session.commit()
        return {'mensagem': 'admin criado com sucesso'}
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail='não pode existir mais de 1 usuário com a role de adm'
        )

#SECTION - Logar User 
#OAuth2PasswordRequestForm: padrão do FastAPI para fazer autenticação mais simples no /docs
@Rota_Publics.post('/logar_usuario')
def logar_usario(base: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    '''\nRealiza o login do cliente e retorna um token JWT.\
        \nPara autenticar, informe as credenciais na requisição.\
        \nParâmetros:\
        \n-username (email) : str \
        \n-password (senha) : str\
        \nRetorno:\
        \n-{"access_token": "...", "token_type": "bearer"}.\
        \nErros:\
        \n-401: Senha inválida.\
        \n-404: Cliente não cadastrado/encontrado.'''
    query_u = session.query(Usuario).filter_by(email=base.username).first()
    if query_u != None:
        if query_u.verificar_senha(base.password):
            _jwt = criar_token(query_u.id, query_u.role)
            #O retorno precisa ser neste formato para o /docs funcionar:
            return {
                "access_token": _jwt,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='senha inválida'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não cadastrado/encontrado.'
        )

