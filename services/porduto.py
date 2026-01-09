from conection import get_session
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from model.produtos import Produto, BaseCadastraProtudo, BaseVenderProtudo, BaseEditarProtudo
from sqlalchemy.exc import IntegrityError
from .depeds import RolePermitidas

#Aplica uma dependência em todas as rotas desse arquivo
Rota_Produto = APIRouter(dependencies=[Depends(RolePermitidas(['fucionario','adm']))])

#SECTION - Cadastra produto
@Rota_Produto.post('/cadastra_produto')
def cadastra_protudo(base: BaseCadastraProtudo, session: Session = Depends(get_session)):
    """\nCadastra um novo produto no sistema.\
        \nPara cadastrar, informe os dados na requisição.\
        \nParâmetros:\
        \n-nome : str \
        \n-qnt : int \
        \n-prc : str (formato: 00.00)\
        \nPermissões: funcionario \\ adm.\
        \nRetorno:\
        \n-{"mensagem": "produto cadastrado com sucesso."}.\
        \nErros:\
        \n-421: Insira um valor válido para Quantidade e para Preço.\
        \n-409: Já existe um produto cadastrado com esse nome."""
    if base.qnt <= 0 or float(base.prc) <= 0:
        #Erro no FastAPI
        raise HTTPException(
            #Código do erro
            status_code=status.HTTP_421_MISDIRECTED_REQUEST,
            #Descrição do motivo do erro
            detail="insira um valor válido para Quantidade e para Preço"
        )
    try:
        produto = Produto(base.nome,base.qnt,base.prc)
        session.add(produto)
        session.commit()
    #Tratamento caso tente cadastrar o produto com nome duplicado
        #pois o banco não permite dois produtos com o mesmo nome
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já existe um produto cadastrado com esse nome'
        )

    return {'mensagem':'produto cadastrado com sucesso'}

#SECTION - Listar todos Protudos
@Rota_Produto.get('/lista_todos_protudos')
def listar_todos_protudos(session: Session = Depends(get_session)):
    """\nLista todos os produtos cadastrados no sistema.\
        \nPermissões: funcionario \\ adm.\
        \nRetorno:\
        \n-{"mensagem": [{"id": ..., "nome": ..., "qnt": ..., "prc": ...}, ...]}.\
        \nErros:\
        \n-404: Não há produtos cadastrados."""
    query_p = session.query(Produto).all()
    #Verifica se há dados no banco de dados
    if query_p != []:
        produto_final = {'mensagem': []}
        #Percorre cada produto e o formata para uma lista melhor
        for i in query_p:
            produto_final['mensagem'].append({'id': i.id,
                                              'nome': i.nome,
                                              'qnt': i.qnt,
                                              'prc': float(i.prc)})  # type: ignore
        return produto_final
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="não há produtos cadastrados"
        )

#SECTION - Procurar Protudo
#O Optional é necessário pois, se definirmos o tipo como int e atribuirmos None diretamente,
    #o Python gera erro: "A expressão do tipo 'None' não pode ser atribuída ao parâmetro do tipo 'int'"
@Rota_Produto.get('/procurar_produtuo')
def procurar_produtuo(id: Optional[int] = None, nome: Optional[str] = None, session: Session = Depends(get_session)):
    """\nProcura um produto por ID ou Nome.\
        \nPode escolher se passa só ID ou Nome do produto. Não é necessário informar os dois.\
        \nParâmetros:\
        \n-id : int (opcional) \
        \n-nome : str (opcional)\
        \nPermissões: funcionario \\ adm.\
        \nRetorno:\
        \n-{"mensagem": {"id": ..., "nome": ..., "qnt": ..., "prc": ...}}.\
        \nErros:\
        \n-421: Informe um ID ou um Nome para a busca.\
        \n-404: Produto não cadastrado/encontrado."""
    query_p = None
    if id:
        query_p = session.query(Produto).filter_by(id=id).first()
    elif nome:
        query_p = session.query(Produto).filter_by(nome=nome).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_421_MISDIRECTED_REQUEST,
            detail="informe um ID ou um Nome para a busca"
        )
    
    #Verifica se há dados no banco de dados
    if query_p is not None:
        #Percorre cada produto e o formata para uma lista melhor
        return {'mensagem': {'id': query_p.id,
                             'nome': query_p.nome,
                             'qnt': query_p.qnt,
                             'prc': float(query_p.prc)}}# type: ignore
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
        )

#SECTION - Dell Produto
@Rota_Produto.delete('/dell_produto/{id_protudo}')
def dell_produto(id_protudo: int, session: Session = Depends(get_session)):
    """\nRemove o produto pelo ID. \
            \nPermissões: funcionario \\ adm.\
            \nRetorno:\
            \n-{"mensagem": "produto removido."}\
            \nErros:\
            \n-404: Produto não cadastrado/encontrado."""
    #Verifica se o produto existe e o deleta
    query_p = session.query(Produto).filter_by(id=id_protudo).delete()

    if query_p:
        session.commit()
        return {"mensagem": "produto removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
             )

#SECTION - Vender Pro
@Rota_Produto.post('/vender_protudo')
def vender_protudo(base: BaseVenderProtudo, session: Session = Depends(get_session)):
    """\nRealiza a venda de um produto, reduzindo sua quantidade no estoque.\
        \nCaso não queira buscar o produto pelo ID, basta não informá-lo. O mesmo vale para o Nome.\
        \nParâmetros:\
        \n-id : int (opcional) \
        \n-nome : str (opcional) \
        \n-qnt_removida_db : int\
        \nPermissões: funcionario \\ adm.\
        \nRetorno:\
        \n-{"mensagem": "produto vendido com sucesso.", "restam": ..., "custo_da_venda": ...}.\
        \n-{"mensagem": "produto vendido e removido do depósito.", "custo_da_venda": ...}.\
        \nErros:\
        \n-404: Não pode vender pois não há quantidade suficiente no depósito."""  
     
    dados_produtos = procurar_produtuo(base.id, base.nome)['mensagem']
    qnt = dados_produtos['qnt']
    id = int(dados_produtos['id'])
    custo = base.qnt_removida_db * dados_produtos['prc']
    qnt_ser_removida = qnt -base.qnt_removida_db
    if qnt_ser_removida < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="não pode vender pois não há quantidade suficiente no depósito"
        )   
    elif qnt_ser_removida == 0:
        dell_produto(id, session)
        return {"mensagem": "produto vendido e removido do depósito",
                'custo_da_venda': custo}
    else:
        #consulta só para pegar o objeto a ser removido
        p = session.query(Produto).filter_by(id=id).first()
        p.qnt = qnt_ser_removida  # type: ignore
        session.commit()
        return {'mensagem': f'produto vendido com sucesso', 'restam': {qnt_ser_removida},
                'custo_da_venda': custo}

@Rota_Produto.post('/etidar_protudo')
def etidar_protudo(base: BaseEditarProtudo, session: Session = Depends(get_session)):
    """\nEdita dados do produto (Quantidade e/ou Preço).\
        \nPara não alterar um campo, não o envie na requisição.\
        \nParâmetros:\
        \n-id : int \
        \n-qnt : int (opcional) \
        \n-prc : str (opcional, formato: 00.00)\
        \nPermissões: funcionario \\ adm.\
        \nRetorno:\
        \n-{"mensagem": "produto editado com sucesso."}.\
        \nErros:\
        \n-421: Informe uma nova Quantidade ou um novo Preço para editar o produto.\
        \n-421: Insira um valor válido para Quantidade.\
        \n-421: Insira um valor válido para Preço.\
        \n-404: Produto não cadastrado/encontrado."""
    query_p = session.query(Produto).filter_by(id=base.id).first()
    if query_p:
        if base.qnt != None :
            if base.qnt > 0: 
                query_p.qnt = base.qnt
            else:
                raise HTTPException(
                    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                    detail="insira um valor válido para Quantidade"
                )
            
        if base.prc != None:
            if float(base.prc) > 0: 
                query_p.prc = base.prc  # type: ignore
            else:
                raise HTTPException(
                    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                    detail="insira um valor válido para Preço"
                )
            
        if base.prc == None and base.qnt == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe uma nova Quantidade ou um novo Preço para editar o produto'
            )

        session.commit()
        return {'mensagem': 'produto editado com sucesso'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
        )

