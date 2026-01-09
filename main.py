from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from services import Rota_Produto, Rota_Cliente, Rota_Adm, Rota_Publics, Rota_Excel

app = FastAPI(title='SGU')

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

#Executa o servido altomaticamente quando o arquivo main.py for executado
if __name__ == "__main__":
    import uvicorn
    import config
    from argparse import ArgumentParser

    #Cria uma pase para o main.py aceitar comando de incialicação como --debug, --port, etc.
    paremtro = ArgumentParser(description='Inicia o servidor SGU')
    #Passo o argumento de inicilização, se o paremetro for passado ele e lido como true, e um help para que ele server
    paremtro.add_argument('--debug', action='store_true', help='Executa em modo debug')
    paremtro.add_argument('--sqlite', action='store_true', help='Cria um sqlite "banco.db"')
    #o type -> é o tipo que precisar ser pasado e o Default é o falo padrão caso não passado
    paremtro.add_argument('--port', type=int, default= 8000, help='Porta do projeto, o padrão: 8000')
    paremtro.add_argument('--host', type=str, default= "localhost", help='IP do projeto, o padrão: localhost')
    
    #Analisa os argumentos
    args = paremtro.parse_args()
    
    config.DEBUG = args.debug
    config.SQLITE = args.sqlite

    #Só executa se --debug foi passado
    if args.debug == True:
        uvicorn.run("main:app", host=args.host ,port=args.port, reload=True)
    else:
        #Modo produção (sem reload)
        uvicorn.run("main:app", host=args.host, port=args.port, reload=False)

