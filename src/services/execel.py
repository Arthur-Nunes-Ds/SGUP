from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from .depeds import RolePermitidas
from conection import engine
from io import BytesIO
import pandas as pd

Rota_Excel = APIRouter(dependencies=[Depends(RolePermitidas(['adm', 'fucionario']))])
Admin_Excel = APIRouter(dependencies=[Depends(RolePermitidas(['adm']))], tags=['Admin'])

#SECTION - User 
@Admin_Excel.get('/usuarios.xlsx')
def get_user():
    """\nExporta a tabela de usuários em formato Excel (.xlsx).\
        \nAutenticação: Envie o JWT no header: Authorization: Bearer <token>\
        \nPermissões: adm.\
        \nRetorno:\
        \n-Arquivo usuarios.xlsx para download.\
        \nErros:\
        \n-Nenhum erro específico."""
    #Pega todos os dados da tabela direto do banco e transforma para DataFrame (tipo de dados do pandas)
    table_u = pd.read_sql_table('usuarios', engine)
    #Remove o campo das senha
    table_u = table_u.drop(columns=['senha'])
    #O BytesIO() permite armazenar tudo em uma posição da memória RAM do sistema, assim o arquivo é escrito na RAM do OS
    saida = BytesIO()
    #Evita erros ou fechamento incompleto da tabela. O 'openpyxl' é o driver que permite manipular Excel com uma precição melhor 
    with pd.ExcelWriter(saida, engine='openpyxl') as execel:
        #Escreve o DataFrame no arquivo Excel, sheet_name = nome da aba
        table_u.to_excel(execel, sheet_name='usuarios', index=False)
    #Faz o ponteiro voltar para o início da RAM (pense na RAM como uma lista)
    saida.seek(0)
    #Informa ao navegador que é para baixar o arquivo e sugere o nome dele
    headers = {"Content-Disposition": "attachment; filename=usuarios.xlsx"}
    #Classe do FastAPI que permite processar arquivos nas requisições
    return StreamingResponse(
        saida,
        #Aqui o navegador identifica o tipo de arquivo. Os tipos você consegue consultar em https://docs.python.org/3/library/mimetypes.html
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )

#SECTION - Produtos
@Rota_Excel.get('/produtos.xlsx', tags=['Produtos'])
def get_protudo():
    """\nExporta a tabela de produtos em formato Excel (.xlsx).\
        \nAutenticação: Envie o JWT no header: Authorization: Bearer <token>\
        \nPermissões: adm \\ funcionario.\
        \nRetorno:\
        \n-Arquivo produtos.xlsx para download.\
        \nErros:\
        \n-Nenhum erro específico."""
    table_p = pd.read_sql_table('produtos', engine)
    saida = BytesIO()
    with pd.ExcelWriter(saida, engine='openpyxl') as execel:
        table_p.to_excel(execel, sheet_name='produtos', index=False)
    saida.seek(0)
    headers = {"Content-Disposition": "attachment; filename=produtos.xlsx"}
    return StreamingResponse(
        saida,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )

#SECTION - All
@Admin_Excel.get('/all_tabelas.xlsx')
def get_all():
    """\nExporta todas as tabelas (produtos e usuários) em um único arquivo Excel (.xlsx).\
        \nAutenticação: Envie o JWT no header: Authorization: Bearer <token>\
        \nPermissões: adm.\
        \nRetorno:\
        \n-Arquivo all_tabelas.xlsx para download com múltiplas abas.\
        \nErros:\
        \n-Nenhum erro específico."""
    table_p = pd.read_sql_table('produtos', engine)
    table_u = pd.read_sql_table('usuarios', engine)
    table_u = table_u.drop(columns=['senha'])
    saida = BytesIO()
    with pd.ExcelWriter(saida, engine='openpyxl') as execel:
        table_p.to_excel(execel, sheet_name='produtos', index=False)
        table_u.to_excel(execel, sheet_name='usuarios', index=False)
    saida.seek(0)
    headers = {"Content-Disposition": "attachment; filename=all_tabelas.xlsx"}
    return StreamingResponse(
        saida,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )

Rota_Excel.include_router(Admin_Excel)
