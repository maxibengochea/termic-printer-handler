from typing import TypedDict, Literal

#tipar los estilos de texto
class FontStylesType(TypedDict, total=False):
  alignment: str
  fontType: str
  fontSize: str
  bold: bool
  underlined: bool

#tipar el texto con estilos
class PrintTextType(TypedDict):
  type: Literal['text']
  text: str
  styles: FontStylesType
