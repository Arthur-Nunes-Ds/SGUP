from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from services import Rota_Produto, Rota_Usuario, Rota_Adm, Rota_Publics, Rota_Excel

app = FastAPI(title='SGU', summary=' ')

#include_in_schema => é se a rota vai ser mostratda no /docs ou não
    #o padrão é que ela sera mostrada
app.get('/', include_in_schema=False)
def home_to_doc():
    #toda fez que o user entrar nessa rota ele vai ser rederecionato
        #altomaticamente para /docs
    return RedirectResponse(url='/docs')

#public
app.include_router(
    #todas as rotas de usuario.py começarão com /usuario
    Rota_Publics,
    #fala o inicio do endpote. Ou seja qual request que fezer para qualquer função dentro de usuario.py
        #ele vai ficar assim /usuario/end_point <- sendo que o end_point pode muda agora mas o /usu.. não
    prefix='/public',
    #organiza as rotas sob este grupo no /docs   
    tags=["Public"]
)

#user
app.include_router(
    Rota_Usuario,
    prefix='/usuario',
    tags=["Usuario"]
)

#admin
app.include_router(
    Rota_Adm,
    prefix='/adm',
    tags=["Admin"]
)

#produtos
app.include_router(
    Rota_Produto,
    prefix="/produtos", 
    tags=["Produtos"]      
)

#execel
app.include_router(
    Rota_Excel,
    prefix='/dwoload',
    tags=['Execel_Exporte']
)

