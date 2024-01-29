from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  overload,
  Optional,
  Sequence,
  Union,
  Type,
  List,
  Any
)

if TYPE_CHECKING:
  from .types._etc import AppBotContextT
  from discord.message import Message
  from .abc import Snowflake

  from discord.flags import Intents

from discord.ext.commands.errors import CommandInvokeError
from discord.ext.commands.bot import Bot

from .context import AppBotContext
from .state import BotAppDatabase
from .errors import BaseError
from .guild import Guild

from random import choice
from glob import glob

import discord
import logging
import os

logger = logging.getLogger(__name__)

class BotApp(Bot):
  def __init__(self, prefix: str, *, intents: Intents) -> None:
    super().__init__(prefix, intents=intents)

    self._state = BotAppDatabase(self.morkato_dispatch, bot=self, base="data")
    
  async def on_ready(self) -> None:
    await self.tree.sync()

    await self.change_presence(activity = discord.Game("Pudim. O Game (LTS)"), status = discord.Status.dnd)

    logger.info("Estou conectado, como: %s", self.user)
  
  def morkato_dispatch(self, ev_name: str, *args, **kwargs) -> None: ...

  async def get_morkato_guild(self, obj: Snowflake) -> Guild:
    return await Guild.get(obj, database=self._state)

  @overload
  async def get_context(self, origin: Message, /) -> AppBotContext: ...
  @overload
  async def get_context(self, origin: Message, /, *, cls: Type[AppBotContextT]) -> AppBotContextT: ...
  async def get_context(self, origin: Message, /, *, cls: Optional[Type[AppBotContextT]] = None) -> Union[AppBotContext, AppBotContextT]:
    if cls is not None and not issubclass(cls, AppBotContext):
      raise RuntimeError

    return await super().get_context(origin, cls=cls or AppBotContext)

  async def on_message(self, message: Message) -> None:
    if message.guild is None:
      return
    
    guild = await self.get_morkato_guild(message.guild)
    trigger = await guild.get_trigger(message.content)

    if not trigger:
      return
    
    response = choice(trigger.responses)

    await message.channel.send(response)
  
  async def on_command_error(self, ctx: AppBotContext[BotApp], err: Exception) -> None:
    if not isinstance(err, CommandInvokeError):
      logger.error("Ignoring exception %s", err)

      raise err

    error = err.original

    if not isinstance(error, BaseError):
      await ctx.send(f'`[{type(error).__name__} - generic.unknown: Error!] {error}`')

      logger.error("Ignoring error: %s", error)

      raise err
    
    message = error.get_discord_message()

    await ctx.send(message)

  async def setup_hook(self) -> None:
    app = 'app'
    
    extensions = glob(os.path.join(app, 'extensions/**/*.py'), recursive=True)
    
    for ext in extensions:
      ext = ext.replace('/', '.')
      ext = ext[:-3]

      logger.info("Loading Extension: %s", ext)

      await self.load_extension(ext)