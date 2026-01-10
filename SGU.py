if __name__ == "__main__":
    from json import dump
    from pathlib import Path
    from argparse import ArgumentParser
    import atexit

    #para deletar o json_sqlite apos ser o servidor se encerado
    def dell_json_sqlite():
        json = Path('config/.sgu_config.json')
        slqlite = Path('banco.db')
        try:
            if json.exists():
                #unlink deleta o arvivo <- isso fica mas versatios para os
                json.unlink()

            if slqlite.exists():
                slqlite.unlink()
        except Exception as e:
            print(f"Erro ao deletar: {e}")

        print("\nServidor encerrado. Arquivo de config/temporario removido.")

    #Registra para quando o programa fechar (qualquer motivo) ele támbe já fecha o programa
    atexit.register(dell_json_sqlite)

    #Cria uma pase para o main.py aceitar comando de incialicação como --debug, --port, etc.
    paremtro = ArgumentParser(description='Inicia o servidor SGU')
    #Passo o argumento de inicilização, se o paremetro for passado ele e lido como true, e um help para que ele server
    paremtro.add_argument('--debug', action='store_true', help='Executa em modo debug')
    paremtro.add_argument('--sqlite', action='store_true', help='Cria um sqlite "banco.db"')
    #o type -> é o tipo que precisar ser pasado e o Default é o falo padrão caso não passado
    paremtro.add_argument('--port', type=int, default= 8000, help='Porta do SGU, o padrão: 8000')
    paremtro.add_argument('--host', type=str, default= "localhost", help='IP do SGU, o padrão: localhost')
    #nargs -> me fala que eu posso varios paremtros como por exempl-> pip install pandas fastapi flet
        #assim tuddo isso vai ser baixodo pelo pip 
    paremtro.add_argument('--host-fronte', nargs='*', type=str, default=['*'] ,help='Lista de IP do fronte')

    #Analisa os argumentos
    args = paremtro.parse_args()
    
    #add um json temp só para no modo de reload ele não fica redefinindo toda hora
    with open('config/.sgu_config.json', 'w') as f:
        dump({'DEBUG': args.debug, 'SQLITE': args.sqlite, 'HOST_FRONT': args.host_fronte}, f)

    #o unicorvn tem que se puxado antes para que de tempo das var DEBUG e SQLITE serem alterada
    import uvicorn

    #Só executa se --debug foi passado
    if args.debug == True:
        uvicorn.run("main:app", host=args.host ,port=args.port, reload=True)
    elif args.debug == False and args.sqlite == False:
        #Modo produção (sem reload)
        uvicorn.run("main:app", host=args.host, port=args.port, reload=False)
    else:
        print('por motivode seguranção o código não sera executado em modo de produção')
        uvicorn.run("main:app", host=args.host ,port=args.port, reload=True)
