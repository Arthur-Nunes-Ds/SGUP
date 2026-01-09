from conection import get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException,status, Depends
from model.usarios import Usuario, BaseEditarUsuarioi
from .depeds import RolePermitidas

Rota_Cliente = APIRouter()

#SECTION - Dell User
#A Depends indica que a rota depende de RolePermitidas
    #assim executa essa classe e utiliza sua resposta
@Rota_Cliente.delete('/dell_user')
def dell_user(id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    """Remove o cliente pelo JWT. \
    \nPermissões: cliente \\ adm.\
    \nRetorno:\
    \n-{"mensagem": "cliente removido."}\
    \nErros:\
    \n-404: cliente não cadastrado/encontrado."""
    query_u = session.query(Usuario).filter_by(id = id_user, role = 'cliente').delete()

    if query_u:
        session.commit()
        return {"mensagem": "cliente removido."}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="cliente não cadastrado/encontrado."
        )
    
#SECTION - Editar Cliente    
@Rota_Cliente.post('/editar_cliente')
def editar_user(base : BaseEditarUsuarioi, id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    """\nEdita dados do cliente (nome e/ou senha).\
    \nPara não alterar um campo, não o envie na requisição.\
    \nParâmetros:\
    \n-nome : str \
    \n-senha : str\
    \nPermissões: cliente \\ adm.\
    \nRetorno:\
    \n-{"mensagem": "cliente editado com sucesso."}.\
    \nErros:\
    \n-421: Informe um novo nome ou uma nova senha.\
    \n-404: Cliente não cadastrado/encontrado."""

    query_u = session.query(Usuario).filter_by(id = id_user, role = 'cliente').first()
    if query_u:
        if base.senha != None :
            query_u.altera_senha(base.senha)
            
        if base.nome != None:
            query_u.nome = base.nome
            
        if base.nome == None and base.senha == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='Informe um novo Nome ou uma nova Senha.'
            )

        session.commit()
        return {'mensagem': 'cliente editado com sucesso.'}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="Cliente não cadastrado/encontrado."
        )

#SECTION - Dados Cliente
@Rota_Cliente.get('/dados_cliente')
def dados_user(id_user: int = Depends(RolePermitidas(['cliente','adm'])),session: Session = Depends(get_session)):
    """\nObtém os dados do cliente (nome e email).\
    \nRetorno:\
    \n-{"mensagem": {"nome": ..., "email": ...}}.\
    \nErros:\
    \n-404: cliente não encontrado."""
    
    query_u = session.query(Usuario).filter_by(id = id_user).first()

    if query_u != None:
        return {
            'mensagem':{
                'nome' : query_u.nome,
                'email' : query_u.email
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cliente não existe.'
        )
    