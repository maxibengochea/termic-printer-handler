from typing import TypedDict

#tipar los estilos de texto
class FontStylesDto(TypedDict, total=False):
  alignment: str
  fontType: str
  fontSize: str
  bold: bool
  underlined: bool
