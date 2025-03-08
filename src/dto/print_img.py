from typing import TypedDict

#tipar el body de la petición de imprimir imagen
class PrintImgDto(TypedDict):
  printerName: str
  image: str
