from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from services import Rota_Produto, Rota_Cliente, Rota_Adm, Rota_Publics, Rota_Excel
from config import HOST_FRONT

app = FastAPI(title='SGU')

#Configuração de CORS (Cross-Origin Resource Sharing) -> isso permite que o backend
    #se comunique com o frontend, mesmo que estejam em domínios diferentes.
app.add_middleware(
    CORSMiddleware,
    #quem pode fazer requisições para o bac
    allow_origins=HOST_FRONT,  
    #permite que o navegado envie credenciais(cookies, jwt) junto da requisição
    allow_credentials=True,
    #permite os metedos como get, post, etc.
    allow_methods=["*"], 
    #permite todos os tipos de cabeçalhos numa requisição.
    allow_headers=["*"],
)

#include_in_schema => indica se a rota será exibida no /docs ou não.
    #O padrão é que ela será exibida.
@app.get('/', include_in_schema=False)
def home_to_doc():
    #Toda vez que o usuário acessar essa rota, ele será redirecionado
    #automaticamente para /docs.
    return RedirectResponse(url='/docs')

#SECTION - Public
app.include_router(
    #Todas as rotas deste grupo começarão com /public.
    Rota_Publics,
    #Define o prefixo do endpoint. Para qualquer função neste roteador,
    #o caminho ficará assim: /public/endpoint — o endpoint pode mudar, mas /public não.
    prefix='/public',
    #Organiza as rotas deste grupo na documentação (/docs).
    tags=["Public"]
)

#SECTION - Cliente
app.include_router(
    Rota_Cliente,
    prefix='/cliente',
    tags=["Cliente"]
)

#SECTION - Admin
app.include_router(
    Rota_Adm,
    prefix='/adm',
    tags=["Admin"]
)

#SECTION - Produtos
app.include_router(
    Rota_Produto,
    prefix="/produtos",
    tags=["Produtos"]
)

#SECTION - Excel
app.include_router(
    Rota_Excel,
    prefix='/dwoload',
    tags=['Execel_Exporte']
)
