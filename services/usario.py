from conection import session
from fastapi import APIRouter, HTTPException,status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from model.usarios import Usuario, BaseCriarUsuario, BaseEditarUsuarioi
from sqlalchemy.exc import IntegrityError
from jose import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from os import getenv
from .depeds import verificar_toke

load_dotenv()
SECRETES_KEY = getenv('SECRETES_KEY')
ALG = getenv('ALG')
EXPIRATION_TIMER_MINUTES = int(getenv('EXPIRATION_TIMER_MINUTES')) # type: ignore

def criar_token(id_user):
    #vai pega o tempo de agora e soma mas o tempo de EXPIRATION_TIMER_MINUTES
    dt_expi = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIMER_MINUTES)
    #o dic_info está configurado com base no site: https://www.jwt.io/
    dic_info = {'sub': str(id_user), 'exp': dt_expi}
    #isso cria o jwt 
    jwt_codificado = jwt.encode(dic_info, SECRETES_KEY, ALG) # type: ignore
    return jwt_codificado

Rota_Usuario = APIRouter()

@Rota_Usuario.post('/criar_usuario')
def criar_usario(base:BaseCriarUsuario):
    try:
        user = Usuario(base.nome, base.email,base.senha)
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
@Rota_Usuario.post('/logar_usuario')
def logar_usario(base: OAuth2PasswordRequestForm = Depends()):
    query_u = session.query(Usuario).filter_by(email = base.username).first()
    if query_u != None:
        if query_u.verificar_senha(base.password):
            _jwt = criar_token(query_u.id)
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

#a depends basicamente fala que depende o do verifica_toke ou seja executa a função
#e pega a resposta dela
@Rota_Usuario.delete('/dell_user')
def dell_user(id_user: int = Depends(verificar_toke)):
    query_u = session.query(Usuario).filter_by(id = id_user).delete()

    if query_u:
        session.commit()
        return {"mensagem": "user removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user não cadastrado/encontrado"
        )
    
@Rota_Usuario.post('/editar_user')
def editar_user(base : BaseEditarUsuarioi, id_user: int = Depends(verificar_toke)):
    '''caso não queira altera o dado do protudo basta só não pasa a chave'''
    query_u = session.query(Usuario).filter_by(id = id_user).first()
    if query_u:
        if base.senha != None :
            query_u.altera_senha(base.senha)
            
        if base.nome != None:
            query_u.nome = base.nome
            
        if base.nome == None and base.senha == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe uma nova Nome ou uma nova Senha para editar o user'
            )

        session.commit()
        return {'mesagem': 'user editado com sucesso'}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user não cadastrado/encontrado"
        )
    
@Rota_Usuario.get('/dados_user')
def dados_user(id_user: int = Depends(verificar_toke)):
    query_u = session.query(Usuario).filter_by(id = id_user).first()

    if query_u != None:
        return {
            'mesagem':{
                'nome' : query_u.nome,
                'email' : query_u.email
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user não existe'
        )