from typing import TypedDict
from src.types.print_image import PrintImgType
from src.types.print_text import PrintTextType

#tipar la peticion de imprimir
class PrintDto(TypedDict):
  printerName: str
  content: list[PrintImgType | PrintTextType]
  openDrawer: bool
