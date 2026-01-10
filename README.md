<h1 align="center">SGU</h1>

# Para iniciar o SGU, utilize o comando abaixo:
```bash
 python SGU.py
```
# Argumentos de inicialização disponíveis:
- `--debug`: Executa em modo debug com reload automático. Ex.: `python SGU.py --debug`
- `--sqlite`: Cria/usa o arquivo `banco.db` (SQLite) em vez do banco padrão. Ex.: `python SGU.py --sqlite`
- `--htpps`: Habilita HTTPS usando `/certs/cert.pem` e `/certs/key.pem` se existirem. Ex.: `python SGU.py --htpps`
- `--host <endereco_ip>`: IP onde o servidor escuta (padrão: `localhost`). Ex.: `python SGU.py --host 0.0.0.0`
- `--port <numero_porta>`: Porta onde o servidor escuta (padrão: `8000`). Ex.: `python SGU.py --port 8080`
- `--host-fronte <enderecos...>`: Lista de IPs/URLs permitidos para o frontend (padrão: `*`[qualquer um]). Ex.: `python SGU.py --host-fronte http://localhost:3000 http://192.168.1.100:3000`

# Principais recurso usado no projeto:

[![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.45-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)