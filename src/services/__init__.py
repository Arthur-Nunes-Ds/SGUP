#Isso define o que pode ser importado se escrever o código da seguinte forma:
    #import services #<- assim só posso usar o que está no __all__
from .porduto import Rota_Produto
from .cliente import Rota_Cliente
from .admin import Rota_Adm
from .publics import Rota_Publics
from .execel import Rota_Excel
__all__ = ['Rota_Produto', 'Rota_Cliente', 'Rota_Adm', 'Rota_Publics', 'Rota_Excel']