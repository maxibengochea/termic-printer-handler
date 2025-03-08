from src.types.font_styles import FontStylesType
from typing import TypedDict

#tipar el body de la petición de imprimir texto
class PrintTextDto(TypedDict):
  text: str
  printerName: str
  styles: FontStylesType
