from typing import TypedDict, Literal

#tipar los estilos de texto
class FontStylesType(TypedDict, total=False):
  alignment: Literal['left', 'center', 'right']
  fontType: Literal['fontA', 'fontB', 'fontC']
  fontSize: Literal['doubleWidth', 'doubleHeight', 'doubleWidthHeight']
  bold: bool
  underlined: bool

#tipar el texto con estilos
class PrintTextType(TypedDict):
  type: Literal['text']
  text: str
  styles: FontStylesType
