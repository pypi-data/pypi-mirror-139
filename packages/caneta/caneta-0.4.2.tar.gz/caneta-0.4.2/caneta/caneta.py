from typing import List

from pydantic import BaseModel


class Caneta(BaseModel):
    marca: str = "bic"
    cores: List[str] = ["azul", "vermelho"]
    carga: int = 100

    def escrever(self, palavra: str, cor: str):
        if cor not in self.cores:
            raise ValueError(f"A caneta só tem as cores {self.cores}")
        if self.carga:
            print(palavra[: self.carga])
            self.carga = max(0, self.carga - len(palavra))

    def recarregar(self, carga: int):
        self.carga += carga
