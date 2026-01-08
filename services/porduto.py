from conection import session
#fala que o paremetro e opicional para o fastapi
from typing import Optional
from fastapi import APIRouter, HTTPException,status
#from .depeds import verificar_toke
from model.produtos import Produto,BaseCadastraProtudo, BaseVenderProtudo,BaseEditarProtudo
from sqlalchemy.exc import IntegrityError

#FIXME - bloque todas rotas para que só o fucionario possa acessar
Rota_Produto = APIRouter()

@Rota_Produto.post('/cadastra_produto')
def cadastra_protudo(base : BaseCadastraProtudo):
    '''O preço tem que ser informato no seguinte formato: 00.00 '''
    if base.qnt <= 0 or float(base.prc) <= 0:
         #erro no fatapi 
         raise HTTPException(
             #o codigo do erro
             status_code=status.HTTP_421_MISDIRECTED_REQUEST,
             #uma descrição pq o erro acontecel
             detail="insira um valor valido para Quantidade e para Preço"
         )
    try:
        produto = Produto(base.nome,base.qnt,base.prc)
        session.add(produto)
        session.commit()
    #tratamento caso tenta cadastra o produto com memo. 
    #pois o banco não permite dois produto com o mesmo nome
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='já há um produto cadastrado com esse nome'
        )

    return {'mensagem':'produto cadastrado com sucesso'}

@Rota_Produto.get('/lista_todos_protudos')
def listar_todos_protudos():
    query_p = session.query(Produto).all()
    #ver se tem o dados na db
    if not query_p == None:
        produto_final = {'mesagem':[]}
        #pecorre cada produto e o formata para uma lista melhor
        for i in query_p:
            produto_final['mesagem'].append({'id':i.id,
                                            'nome': i.nome,
                                            'qnt':i.qnt,
                                            'prc':float(i.prc)}) # type: ignore 
        return produto_final
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="não á produto cadastrado"
        )

#o Optional é nessario pq se eu deija qu eo tipo e int e atribuir ele direto a None o python aponta
    # o erro ->  A expressão do tipo "None" não pode ser atribuída ao parâmetro do tipo "int" "None" 
    # não pode ser atribuído a "int" 
@Rota_Produto.get('/procurar_produtuo')
def procurar_produtuo(id: Optional[int] = None, nome: Optional[str] = None):
    '''Pode escolhe se pasa só Id ou Nome do prodtudo. Não é necesario informa os dois'''
    query_p = None
    if id:
        query_p = session.query(Produto).filter_by(id = id).first()
    elif nome:
        query_p = session.query(Produto).filter_by(nome = nome).first()
    else:
        raise HTTPException(
             status_code=status.HTTP_421_MISDIRECTED_REQUEST,
             detail="informe um ID ou um Nome para a busca"
        )
    
    #ver se tem o dados na db
    if query_p != None:
        #pecorre cada produto e o formata para uma lista melhor
        return {'mesagem':{'id':query_p.id,
                        'nome': query_p.nome,
                        'qnt':query_p.qnt,
                        'prc':float(query_p.prc)}} # type: ignore 
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
        )

@Rota_Produto.delete('/dell_produto/{id}')
def dell_produto(id: int):
    #já ver se o produto existe e o deleta
    query_p = session.query(Produto).filter_by(id = id).delete()

    if query_p:
        session.commit()
        return {"mensagem": "produto removido"}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
        )

@Rota_Produto.post('/vender_protudo')
def vender_protudo(base: BaseVenderProtudo):
    '''informe o Id ou o Nome sendoo que o Id tem que ser int e o nome tem que ser str  \
    \n caso não queira achar o protudo pelo Id pasta não informa-lo. \
    \n O mesmo vale para o Nome'''

    dados_produtos = procurar_produtuo(base.id, base.nome)['mesagem']
    qnt = dados_produtos['qnt']
    id = int(dados_produtos['id']) 
    custo = base.qnt_removida_db * dados_produtos['prc'] 
    qnt_ser_removida = qnt - base.qnt_removida_db
    if qnt_ser_removida < 0:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="não pode vende pois não tem o suviciente no deposito"
        )

    elif qnt_ser_removida == 0:
        dell_produto(id)
        return {"mensagem": "produto vendido e removido do depoisto",
                'custo_da_venda':custo}
    else:
        #consulta só para pega o objeto para se removido
        p = session.query(Produto).filter_by(id = id).first()
        p.qnt = qnt_ser_removida # type: ignore
        session.commit()
        return {'mesagem': f'produto vendido com sucesso', 'restam' : {qnt_ser_removida},
                'custo_da_venda':custo}

@Rota_Produto.post('/etidar_protudo')
def etidar_protudo(base: BaseEditarProtudo):
    '''caso não queira altera o dado do protudo basta só não pasa a chave'''
    query_p = session.query(Produto).filter_by(id = base.id).first()
    if query_p:
        if base.qnt != None :
            if base.qnt > 0: 
                query_p.qnt = base.qnt
            else:
                raise HTTPException(
                    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                    detail="insira um valor valido para Quantidade"
                )
            
        if base.prc != None:
            if float(base.prc) > 0: 
                query_p.prc = base.prc  # type: ignore
            else:
                raise HTTPException(
                    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                    detail="insira um valor valido para Preço"
                )
            
        if base.prc == None and base.qnt == None:
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST,
                detail='informe uma nova Quantidade ou um novo Preço para editar o produto'
            )

        session.commit()
        return {'mesagem': 'produto editado com sucesso'}
    else:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="produto não cadastrado/encontrado"
        )
    
