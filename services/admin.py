from conection import get_session
from fastapi import APIRouter, HTTPException,status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .depeds import RolePermitidas
from model.usarios import Usuario, BaseCriarUsuario, BaseEditarFucionario
from model.produtos import Produto
from typing import Literal
from dotenv import load_dotenv
from os import getenv
from config import DEBUG

load_dotenv()

#Aplica uma dependência em todas as rotas desse arquivo
Rota_Adm = APIRouter(dependencies=[Depends(RolePermitidas(['adm']))])

#SECTION - Listar User
@Rota_Adm.get('/listar_user')
#O Literal serve como um XOR entre as opções, ou seja, tem que ser exatamente o que está na lista
def listar_user(role: Literal['cliente', 'fucionario', 'adm'] | None = None, session: Session = Depends(get_session)):
    """\nLista usuários cadastrados, com opção de filtro por role.\
        \nCaso deseje aplicar um filtro para pegar apenas usuários específicos, informe qual das roles deseja.\
        \nParâmetros:\
        \n-role : str (opcional: 'cliente', 'fucionario', 'adm')\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": [{"id": ..., "nome": ..., "role": ..., "email": ...}, ...]}.\
        \nErros:\
        \n-404: Não foi possível encontrar alguém cadastrado com essa role ou não há ninguém cadastrado no banco."""
    
    if role is not None:
        query_u = session.query(Usuario).filter_by(role=role).all()
    else:
        query_u = session.query(Usuario).all()

    if query_u != []:
        user_final = {'mensagem': []}
        for i in query_u:
            user_final['mensagem'].append({'id':i.id,
                                        'nome': i.nome,
                                        'role':i.role,
                                        'email':i.email})
        return user_final
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='não foi possível encontrar alguém cadastrado com essa role ou não há ninguém cadastrado no banco'
        )

#SECTION - Criar Fuc
@Rota_Adm.post('/criar_fucionario')
def criar_fucionario(base: BaseCriarUsuario, session: Session = Depends(get_session)):
    """\nCria um novo funcionário no sistema.\
        \nPara criar, informe os dados na requisição.\
        \nParâmetros:\
        \n-nome : str \
        \n-email : str \
        \n-senha : str\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": "funcionário criado com sucesso."}.\
        \nErros:\
        \n-409: Já existe um funcionário com esse email."""
    try:
        fucionario = Usuario(base.nome, base.email, base.senha, 'fucionario')
        session.add(fucionario)
        session.commit()
        return {'mensagem': 'funcionário criado com sucesso'}
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já existe um funcionário com esse email'
        )

#SECTION - Dell Fuc
@Rota_Adm.delete('/dell_fucionario/{id_func}')
def dell_fucionario(id_func: int, session: Session = Depends(get_session)):
    """\nRemove o funcionário pelo ID. \
            \nPermissões: adm.\
            \nRetorno:\
            \n-{"mensagem": "funcionário removido."}\
            \nErros:\
            \n-404: Funcionário não cadastrado/encontrado."""
    query = session.query(Usuario).filter_by(id=id_func, role='fucionario').delete()

    if query:
        session.commit()
        return {"mensagem": "funcionário removido"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="funcionário não cadastrado/encontrado"
        )

#SECTION - Editar Fuc
@Rota_Adm.post('/editar_fucioanrio')
def editar_fucionario(base: BaseEditarFucionario, session: Session = Depends(get_session)):
    """\nEdita dados do funcionário (nome e/ou senha).\
        \nPara não alterar um campo, não o envie na requisição.\
        \nParâmetros:\
        \n-id : int \
        \n-nome : str (opcional) \
        \n-senha : str (opcional)\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": "funcionário editado com sucesso."}.\
        \nErros:\
        \n-421: Informe um novo nome ou uma nova senha para editar o funcionário.\
        \n-404: Funcionário não cadastrado/encontrado."""
    query_u = session.query(Usuario).filter_by(id=base.id, role='fucionario').first()
    if query_u:
        if base.senha != None :
            query_u.altera_senha(base.senha)
            
        if base.nome != None:
            query_u.nome = base.nome
            
        if base.nome == None and base.senha == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe um novo nome ou uma nova senha para editar o funcionário'
            )

        session.commit()
        return {'mensagem': 'funcionário editado com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="funcionário não cadastrado/encontrado"
        )

#NOTE -Rotas feitas apenas para debug
#SECTION - Zerar User
@Rota_Adm.delete('/dell_all_user/{senha_db}', include_in_schema=DEBUG, tags=['debug'])
def dell_all_user(senha_db: str, session: Session = Depends(get_session)):
    """\nATENÇÃO: Deleta todos os usuários da tabela, incluindo o admin.\
        \nOs usuários ainda poderão fazer requisições por 5 minutos por causa do JWT.\
        \nPara que a ação seja permitida, você deve passar a senha do usuário que está usando para manipular o banco.\
        \nParâmetros:\
        \n-senha_db : str\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": "tabela USUARIO zerada com sucesso."}.\
        \nErros:\
        \n-401: Você não pode fazer isso."""
    if senha_db == getenv('SENHA_DB'):
        session.query(Usuario).delete()
        session.commit()
        return {'mensagem': 'tabela USUARIO zerada com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Você não pode fazer isso.'
        )

#SECTION - Zerar Produtos
@Rota_Adm.delete('/dell_all_produtos/{senha_db}',include_in_schema=DEBUG, tags=['debug'])
def dell_all_produtos(senha_db: str, session: Session = Depends(get_session)):
    """\nATENÇÃO: Deleta todos os produtos da tabela.\
        \nPara que a ação seja permitida, você deve passar a senha do usuário que está usando para manipular o banco.\
        \nParâmetros:\
        \n-senha_db : str\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": "tabela PRODUTOS zerada com sucesso."}.\
        \nErros:\
        \n-401: Você não pode fazer isso."""
    if senha_db == getenv('SENHA_DB'):
        session.query(Produto).delete()
        session.commit()
        return {'mensagem': 'tabela PRODUTOS zerada com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Você não pode fazer isso.'
        )

#SECTION - Zerar Tudo
@Rota_Adm.delete('/dell_all/{senha_db}',include_in_schema=DEBUG, tags=['debug'])
def dell_all(senha_db: str, session: Session = Depends(get_session)):
    """\nATENÇÃO: Deleta tudo das tabelas de PRODUTOS e USUARIOS.\
        \nPara que a ação seja permitida, você deve passar a senha do usuário que está usando para manipular o banco.\
        \nParâmetros:\
        \n-senha_db : str\
        \nPermissões: adm.\
        \nRetorno:\
        \n-{"mensagem": "tabelas PRODUTOS e USUARIOS zeradas com sucesso."}.\
        \nErros:\
        \n-401: Você não pode fazer isso."""
    if senha_db == getenv('SENHA_DB'):
        session.query(Produto).delete()
        session.query(Usuario).delete()
        session.commit()
        return {'mensagem': 'tabelas PRODUTOS e USUARIOS zeradas com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Você não pode fazer isso.'
        )
