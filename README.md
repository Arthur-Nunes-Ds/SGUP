<h1 align="center">SGU - Sistema de Gerenciamento de Usuários</h1>

# Para iniciar o SGU, utilize o comando abaixo:
Atenção: deve escutar o comando:  ```pip install .``` para buildar o projeto antes de executar como ```sgu```. caso não tenha feito isso, você pode executar o prjeto atraves do comando: ```python src/SGU.py``` para iniciar o sistema entre tudo você deve estár dentro de src para executar usando o python diretamente.

# Argumentos de inicialização disponíveis:
- `--debug`: Executa em modo debug com reload automático. Ex.: `sgu --debug`
- `--sqlite`: Cria/usa o arquivo `banco.db` (SQLite) em vez do banco padrão. Ex.: `sgu --sqlite`
- `--https`: Habilita HTTPS usando `src/certs/cert.pem` e `src/certs/key.pem` se existirem. 
O certificado tem que der o nome de `cert.pem` e a chave `key.pem`. Ex.: `sgu --https`
- `--host <endereco_ip>`: IP onde o servidor escuta (padrão: `localhost`). Ex.: `sgu --host 0.0.0.0`
- `--port <numero_porta>`: Porta onde o servidor escuta (padrão: `8000`). Ex.: `sgu --port 8080`
- `--host-fronte <enderecos...>`: Lista de IPs/URLs permitidos para o frontend (padrão: `*`[qualquer um]). Ex.: `sgu --host-fronte http://localhost:3000 http://192.168.1.100:3000`

# Documentação da API
A documentação da API está disponível em: `http://<host>:<port>/docs` ou `https://<host>:<port>/docs` se HTTPS estiver habilitado.

Substitua `<host>` e `<port>` pelos valores usados na inicialização do SGU.
