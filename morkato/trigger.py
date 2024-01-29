from __future__ import annotations

from typing import (
  TYPE_CHECKING
)

if TYPE_CHECKING:
  from .types.trigger import Trigger as TriggerPayload
  
  from .guild import Guild

class Trigger:
  def __init__(self, guild: Guild, payload: TriggerPayload) -> None:
    self._state = guild._state
    self.guild = guild

    self.load_variables(payload)
  
  def load_variables(self, payload: TriggerPayload) -> None:
    self.name = payload['name']

    self.responses = [response["content"] for response in payload["responses"]]
  
  async def delete(self) -> None:
    await self._state.request("DELETE_TRIGGER", "data.guilds", payload={ "guild_id": str(self.guild._id), "name": self.name })