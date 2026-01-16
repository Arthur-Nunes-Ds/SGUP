from conection import engine,Base
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric
from pydantic import BaseModel

#Cria a base da tabela
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False, unique=True)
    qnt = Column(Integer, nullable=False)
    #Permite cadastrar números com vírgula, sendo que no total pode
        #conter até 11 números, contando com os dois reservados para
        #os números após a vírgula
    prc = Column(Numeric(precision=11, scale=2))

    def __init__(self, nome, qnt, prc):
        self.nome = nome
        self.qnt = qnt
        #Já converte corretamente para o Numeric do banco de dados, evitando erros
        self.prc = Decimal(prc)

#Cria a tabela na prática
Base.metadata.create_all(engine)

class BaseCadastraProtudo(BaseModel):
    nome: str 
    qnt: int
    prc: int | float | str

class BaseVenderProtudo(BaseModel):
    qnt_removida_db: int
    id: int | None = None
    nome: str | None = None

class BaseEditarProtudo(BaseModel):
    id: int
    qnt: int | None = None
    # O "|" quer dizer "ou"
    prc: int | float | str | None = None