from src.dto.font_styles import FontStylesDto
from typing import TypedDict

#tipar el body de la petición de imprimir texto
class PrintextDto(TypedDict):
  text: str
  printerName: str
  styles: dict
  styles: FontStylesDto
