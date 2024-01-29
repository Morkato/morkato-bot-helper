from typing import TypedDict, List

from .response import ResponseMessage

class Trigger(TypedDict):
  name: str
  trigger: str

  responses: List[ResponseMessage]