from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Union
)

if TYPE_CHECKING:
  from .types.guild import Guild as GuildPayload
  
  from .state import BotAppDatabase
  from .abc import Snowflake

from .trigger import Trigger

class Guild:
  @staticmethod
  async def get(obj: Snowflake, *, database: BotAppDatabase) -> Guild:
    payload = await database.request("GET", "data.guilds", payload={ "guild_id": str(obj.id) })

    return Guild(database, payload)
    
  def __init__(self, state: BotAppDatabase, payload: GuildPayload) -> None:
    self._state = state
    
    self.load_variables(payload)
  
  def load_variables(self, payload: GuildPayload) -> None:
    self._id = int(payload['id'])
  
  async def get_trigger(self, name: str) -> Union[Trigger, None]:
    payload = { "name": name, "guild_id": str(self._id) }
    data = await self._state.request("GET_TRIGGER", "data.guilds", payload=payload)

    if data is None:
      return
    
    return Trigger(self, data)

  async def create_trigger(
    self, *,
    name: str,
    content: str
  ) -> Trigger:
    payload = { "name": name, "content": content, "guild_id": str(self._id) }
    data = await self._state.request('CREATE_TRIGGER', 'data.guilds', payload=payload)

    return Trigger(self, data)