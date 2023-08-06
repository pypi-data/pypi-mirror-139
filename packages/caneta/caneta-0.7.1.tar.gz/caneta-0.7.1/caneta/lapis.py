from pydantic import BaseModel


class Lapis(BaseModel):
    tamanho: int = 100

    def escrever(self, palavra: str):
        if self.tamanho:
            print(palavra[: self.tamanho])
            self.tamanho = max(0, self.tamanho - len(palavra))

    def apontar(self, voltas: int):
        self.tamanho = max(0, self.tamanho - voltas)
