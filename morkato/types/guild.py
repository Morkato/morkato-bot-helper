from typing import TypedDict, List

from .trigger import Trigger

class Guild(TypedDict):
  id: str

  triggers: List[Trigger]