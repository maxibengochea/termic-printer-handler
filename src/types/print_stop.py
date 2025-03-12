from typing import TypedDict, Literal

#tipar la imagen 
class PrintStopType(TypedDict):
  type: Literal['stop']
  time: int
