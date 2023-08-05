from pydantic import BaseModel


class Caneta(BaseModel):
    marca: str = "bic"
    cor: str = "azul"
    carga: int = 100

    def escrever(self, palavra: str):
        if self.carga:
            print(palavra[: self.carga])
            self.carga = max(0, self.carga - len(palavra))

    def recarregar(self, carga: int):
        self.carga += carga

    def mudar_cor(self, nova_cor):
        self.cor = nova_cor
