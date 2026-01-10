<h1 align="center">SGU</h1>

# Para iniciar o SGU, utilize o comando abaixo:
```bash
 python SGU.py
```
# Argumentos de inicialização opcionais:
- `--debug`: Inicia o projeto em modo de debug, abilita a regarga automática ao detectar mudanças no código exemplo: `SGU.py --debug`;
- `--sqlite`: Utiliza o banco de dados SQLite ao invés do banco de dados padrão exemplo: `SGU.py --sqlite`;
- `--host <endereço_ip>`: Define o endereço IP onde o servidor irá escutar (padrão: `localhost`) exemplo: `SGU.py --host 0.0.0.0`;
- `--port <número_porta>`: Define a porta onde o servidor irá escutar (padrão: `8000`) exemplo: `SGU.py --port 8080`;
- `--host-frontend <endereço_ip> <dns>`: Define o endereço IP do frontend que irá consumir a API(padrão: `[*]`, todos) exemplo: `SGU.py --host-frontend http://localhost:3000 http://192.168.1.100:3000`;

# Principais recurso usado no projeto:

[![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.45-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)