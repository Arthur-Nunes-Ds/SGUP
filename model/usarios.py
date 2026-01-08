from conection import engine,Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from passlib.hash import sha256_crypt as sha256

#cria a base da tabela
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = sha256.encrypt(senha)

    def altera_senha(self,senha):
        self.senha = sha256.encrypt(senha)
    
    def verificar_senha(self, senha):
        return sha256.verify(senha, self.senha) # type: ignore
    
#cria a tabela na paratica
Base.metadata.create_all(engine)

class BaseCriarUsuario(BaseModel):
    nome : str
    senha : str
    email : str

class BaseEditarUsuarioi(BaseModel):
    nome : str | None = None
    senha : str | None = None
