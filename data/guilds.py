from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Callable,
  Coroutine,
  Optional,
  Union,
  Dict,
  List,
  Any
)

if TYPE_CHECKING:
  from morkato.types.trigger import Trigger
  from morkato.types.guild import Guild

from morkato.state import BotDatabaseUnknownMethod, BotDatabaseInvalidPayload
from morkato.utils.etc import in_range, fmt

import orjson

CREATE_LOCK: bool = False
CREATE_TRIGGER_LOCK: bool = False

methods: Dict[str, Callable[[Any], Coroutine[Any, Any, Any]]] = { }
file = "data/guilds.json"

def on_load():
  global methods

  methods = {
    "GET": get,
    "GET_TRIGGER": get_trigger,
    'CREATE_TRIGGER': create_trigger,
    "DELETE_TRIGGER": delete_trigger
  }

async def main(method: str, payload: Any):
  method = method.upper()

  try:
    method_func = methods[method]

    return await method_func(**payload)
  except KeyError:
    raise BotDatabaseUnknownMethod

async def get(guild_id: Optional[str] = None, **kwgs) -> Any:
  with open(file, 'r') as fp:
    guilds = orjson.loads(fp.read())

  if guild_id is not None and not isinstance(guild_id, str):
    guild_id = str(guild_id)
  
  if guild_id is None:
    return guilds
  
  return next((guild for guild in guilds if guild["id"] == guild_id), { "id": guild_id, "triggers": [] })

async def get_trigger(name: str, guild_id: str) -> Any:
  with open(file, 'r') as fp:
    guilds = orjson.loads(fp.read())

  if not isinstance(name, str):
    name = str(name)
  
  name = fmt(name)

  try:
    guild = next((guild for guild in guilds if guild["id"] == guild_id))
    trigger = next((trigger for trigger in guild["triggers"] if fmt(trigger["name"]) == name))

    return trigger
  except StopIteration:
    return None

async def delete_trigger(name: str, guild_id: str) -> Any:
  with open(file, 'r') as fp:
    guilds = orjson.loads(fp.read())

  if not isinstance(name, str):
    name = str(name)
  
  name = fmt(name)
  
  triggers: List[Trigger] = None # type: ignore
  trigger: Trigger = None # type: ignore
  idx: int = None # type: ignore

  print('aqui')

  try:
    guild = next((guild for guild in guilds if guild["id"] == guild_id))
    triggers = guild["triggers"]

    (idx, trigger) = next(((idx, trigger) for (idx, trigger) in enumerate(triggers) if fmt(trigger["name"]) == name))
  except StopIteration:
    return None
  
  del triggers[idx]

  with open(file, 'w') as fp:
    fp.write(orjson.dumps(guilds).decode('utf8'))

  return trigger

async def create_trigger(guild_id: str, name: str, content: str) -> Any:
  with open(file, 'r') as fp:
    guilds = orjson.loads(fp.read())

  (gidx, guild) = next((
    (idx, guild)
    for (idx, guild) in enumerate(guilds)
    if guild['id'] == guild_id
  ), (-1, { 'id': guild_id, "triggers": [] }))
  triggers = guild["triggers"]

  nfm = fmt(name)

  (idx, trigger) = next((
    (idx, trigger)
    for (idx, trigger) in enumerate(triggers)
    if fmt(trigger["name"]) == nfm
  ), (-1, { "name": name, "responses": [] }))

  responses = trigger["responses"]

  if not isinstance(content, str):
    content = str(content)
  
  if not in_range(len(content), (0, 4000)):
    raise BotDatabaseInvalidPayload
  
  responses.append({"content":content})

  if idx == -1:
    triggers.append(trigger)
  
  if gidx == -1:
    guilds.append(guild)
  
  with open(file, 'w') as fp:
    fp.write(orjson.dumps(guilds).decode('utf8'))
  
  return trigger