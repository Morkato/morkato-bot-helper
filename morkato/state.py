from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Optional,
  Callable,
  Dict,
  Any
)

if TYPE_CHECKING:
  from morkato.types.guild import Guild as GuildPayload
  from morkato.bot import BotApp

from .errors import EndpointNotfound
from .guild import Guild

from types import ModuleType
from glob import glob

import importlib.util
import logging
import asyncio
import inspect
import os

logger = logging.getLogger(__name__)

class BotDatabaseGenericError(Exception): ...

class BotDatabaseInvalidEndpoint(BotDatabaseGenericError): ...
class BotDatabaseUnknownMethod(BotDatabaseGenericError): ...
class BotDatabaseInvalidPayload(BotDatabaseGenericError): ...

class BotAppDatabase:
  def __init__(self, dispatch: Callable[..., None], *, bot: BotApp, base: str) -> None:
    self.dispatch = dispatch
    self.bot = bot
    self.base = base
    
    self.load_modules()
    self.clear()
  
  def load_modules(self) -> None:
    self.modules: Dict[str, ModuleType] = {  }
    
    for file in glob(os.path.join(self.base, "*") + '.py'):
      if file[-3:] != '.py':
        continue

      ext = file[:-3].replace('/', '.')

      module = ModuleType(ext)

      spec = importlib.util.find_spec(ext)
      spec.loader.exec_module(module)

      main_func = getattr(module, 'main', None)

      if not asyncio.iscoroutinefunction(main_func) and not len(inspect.signature(main_func).parameters) == 2:
        raise BotDatabaseInvalidEndpoint

      on_load_func = getattr(module, 'on_load', None)

      if on_load_func is not None:
        try:
          on_load_func()
        except Exception as err:
          logger.error("Ignoring module: %s this error: %s" % (module.__name__, err))

          continue
      
      self.modules[module.__name__] = module

  def clear(self) -> None:
    self._guilds: Dict[int, Guild] = {  }

  async def request(self, method: str, endpoint: str, *, payload: Optional[Any] = None) -> Any:
    module = self.modules.get(endpoint)

    if module is None:
      raise EndpointNotfound
    
    main_func = getattr(module, 'main')

    return await main_func(method, payload)
    