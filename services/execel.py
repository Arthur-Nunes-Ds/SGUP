from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from .depeds import RolePermitidas
from conection import engine
from io import BytesIO
import pandas as pd

Rota_Excel = APIRouter(dependencies=[Depends(RolePermitidas(['adm','fucionario']))])
Admin_Excel = APIRouter(dependencies=[Depends(RolePermitidas(['adm']))],tags=['Admin'])

@Admin_Excel.get('/usuarios.xlsx')
def get_user():
    #pega todos os dados da tabela direto do banco e já transforma para dataframe(tipo de dados do pandas)
    table_u = pd.read_sql_table('usuarios', engine)
    #o io.BytesIO() vai me permite joga tudo numa 'casa' da memoria ran do sistema; assim vou escrever o sitema na ran do os
    saida = BytesIO()
    #evitar da erro ou fecha a tebala incompleta, o 'openpyxl' é o drive que faz isso
    with pd.ExcelWriter(saida, engine='openpyxl') as execel:
        #escrevr o datafreme no arquivo execel, sheet_name= nome da aba
        table_u.to_excel(execel, sheet_name='usuarios',index=False)
    #faz o ponteiro volta para o zero da ram(pense na ran como uma lista)
    saida.seek(0)
    #fala para o navegado que é para baixar o arquivo e surgere o nome dele
    headers = {"Content-Disposition": "attachment; filename=usuarios.xlsx"}
    #classe do Fastapi que permite processar arquivo na requissições
    return StreamingResponse(
        saida,
        #aqui é o navegado indetificar o tipo de arquivo. os tipo você copnsegue pega no site https://docs.python.org/3/library/mimetypes.htm
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )

@Rota_Excel.get('/produtos.xlsx', tags=['Produtos'])
def get_protudo():
    table_p = pd.read_sql_table('produtos',engine)
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

@Admin_Excel.get('/all_tabelas.xlsx')
def get_all():
    table_p = pd.read_sql_table('produtos',engine)
    table_u = pd.read_sql_table('usuarios', engine)
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
                                                