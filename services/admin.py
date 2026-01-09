from conection import get_session
from fastapi import APIRouter, HTTPException,status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
#from .depeds import verificar_toke
from .depeds import RolePermitidas
from model.usarios import Usuario, BaseCriarUsuario, BaseEditarFucionario
from model.produtos import Produto
from typing import Literal
from dotenv import load_dotenv
from os import getenv

load_dotenv()
is_debug = bool(int(getenv('IS_DEBUG'))) # type: ignore

#aplica uma depedencia em todas as rotas desse arquivo
Rota_Adm = APIRouter(dependencies=[Depends(RolePermitidas(['adm']))])

@Rota_Adm.get('/listar_user')
#o Literal server como um xor entre as opção ou seja tem que ser exatamente o que tá na lista
def listar_user(role : Literal['cliente','fucionario','adm'] | None = None, session: Session = Depends(get_session)):
    '''Caso deseja aplicar um filtro para pega só user especificos basta informa qual das roles \
        \n deseja ['cliente','fucionario','adm'] caso não passa a role tera d]e todos os user do banco.'''
    
    if role != None:
        query_u = session.query(Usuario).filter_by(role = role).all()
    else:
        query_u = session.query(Usuario).all()

    if query_u != []:
        user_final = {'mesagem': []}
        for i in query_u:
            user_final['mesagem'].append({'id':i.id,
                                        'nome': i.nome,
                                        'role':i.role,
                                        'email':i.email})
        return user_final
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='não foi possivel encontra alguem cadastrado com essa role'
        )
        
@Rota_Adm.post('/criar_fucionario')
def criar_fucionario(base: BaseCriarUsuario, session: Session = Depends(get_session)):
    try:
        fucionario = Usuario(base.nome, base.email, base.senha, 'fucionario')
        session.add(fucionario)
        session.commit()
        return {'mesagem':'fucionario criado com suceso'}
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já há um fucionario com esse email'
        )

@Rota_Adm.delete('/dell_fucionario/{id_func}')
def dell_fucionario(id_func : int, session: Session = Depends(get_session)):
    query = session.query(Usuario).filter_by(id = id_func, role = 'fucionario').delete()

    if query:
        session.commit()
        return {"mensagem": "fucionario removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="fucionario não cadastrado/encontrado"
        )
    
@Rota_Adm.post('/editar_fucioanrio')
def editar_fucionario(base: BaseEditarFucionario, session = get_session):
    '''caso não queira altera o dado do protudo basta só não pasa a chave'''
    query_u = session.query(Usuario).filter_by(id = base.id, role = 'fucionario').first()
    if query_u:
        if base.senha != None :
            query_u.altera_senha(base.senha)
            
        if base.nome != None:
            query_u.nome = base.nome
            
        if base.nome == None and base.senha == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe um novo Nome ou uma nova Senha para editar o fucionario'
            )

        session.commit()
        return {'mesagem': 'fucionario editado com sucesso'}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="fucionario não cadastrado/encontrado"
        )

#rotas feitas só para debug
@Rota_Adm.delete('/dell_all_user/{senha_db}', include_in_schema=is_debug, tags=['debug'])
def dell_all_user(senha_db : str, session: Session = Depends(get_session)):
    '''ATENÇÃO AQUI VOCÊ VAI DELETAR TUDO QUE TIVER NA TABELA USUARIO \
    \n INCLUINDO O ADM. OS USER AINDA PODERAR FAZER APLICAÇÃO POR 5 MINUTOS PORQUASA DO JWT\
    \n PARA QUE A AÇÃO SEJA PERMITE VOCÊ DEVE PASSA A SENHA DO USER QUE ESTÁ USANDO PARA MANIPULAR O BANCO.'''
    if senha_db == getenv('SENHA_DB'):
        session.query(Usuario).delete()
        session.commit()
        return {'mesagem': 'tabela USUARIO zerada com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='você não pode fazer isso'
        )

@Rota_Adm.delete('/dell_all_produtos/{senha_db}',include_in_schema=is_debug, tags=['debug'])
def dell_all_produtos(senha_db: str, session: Session = Depends(get_session)):
    '''ATENÇÃO AQUI VOCÊ VAI DELETAR TUDO QUE TIVER NA TABELA PROTUDOS\
    \n PARA QUE A AÇÃO SEJA PERMITE VOCÊ DEVE PASSA A SENHA DO USER QUE ESTÁ USANDO PARA MANIPULAR O BANCO.'''
    if senha_db == getenv('SENHA_DB'):
        session.query(Produto).delete()
        session.commit()
        return {'mesagem': 'tabela PROTUDOS zerada com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='você não pode fazer isso'
        )

@Rota_Adm.delete('/dell_all/{senha_db}',include_in_schema=is_debug, tags=['debug'])
def dell_all(senha_db: str, session: Session = Depends(get_session)):
    '''ATENÇÃO AQUI VOCÊ VAI DELETAR TUDO QUE TIVER NA TABELA PROTUDOS E USUARIOS\
    \n PARA QUE A AÇÃO SEJA PERMITE VOCÊ DEVE PASSA A SENHA DO USER QUE ESTÁ USANDO PARA MANIPULAR O BANCO.'''
    if senha_db == getenv('SENHA_DB'):
        session.query(Produto).delete()
        session.query(Usuario).delete()
        session.commit()
        return {'mesagem': 'tabela PROTUDOS e USUARIOS zerada com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='você não pode fazer isso'
        )
