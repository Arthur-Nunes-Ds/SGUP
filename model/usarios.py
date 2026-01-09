from conection import engine,Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from passlib.hash import sha256_crypt as sha256

#Cria a base da tabela
class Usuario(Base):
    #Var do SQLAlchemy: nome da tabela
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    #O default faz com que, mesmo que eu não passe a role, ele cadastre como "cliente" automaticamente
    role = Column(String(200), nullable=False, default='cliente')

    def __init__(self, nome, email, senha, role='cliente'):
        self.nome = nome
        self.email = email
        #Já criptografa a senha
        self.senha = sha256.encrypt(senha)
        self.role = role

    def altera_senha(self,senha):
        self.senha = sha256.encrypt(senha)
    
    def verificar_senha(self, senha):
        return sha256.verify(senha, self.senha) # type: ignore
    
#Cria a tabela na prática
Base.metadata.create_all(engine)

#Parâmetros de como tem que ser enviado. Qualquer coisa contrária já será rejeitada automaticamente.
class BaseCriarUsuario(BaseModel):
    nome: str
    senha: str
    email: str

class BaseEditarUsuarioi(BaseModel):
    #Igualar a None gera um campo opcional, ou seja, se ele não for passado, o código continua
    nome: str | None = None
    senha: str | None = None

class BaseEditarFucionario(BaseModel):
    id: int 
    nome: str | None = None
    senha: str | None = None

