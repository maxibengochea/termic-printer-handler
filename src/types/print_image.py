from typing import TypedDict, Literal

#tipar la imagen 
class PrintImgType(TypedDict):
  type: Literal['img']
  image: str
  alignment: Literal['left', 'center', 'right']
