from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  TypeVar
)

if TYPE_CHECKING:
  from ..bot import  BotApp
  from ..context import AppBotContext

  BotAppT = TypeVar('BotAppT', bound='BotApp')
  AppBotContextT = TypeVar('AppBotContextT', bound='AppBotContext')
  Context = AppBotContext[BotApp]
else:
  BotAppT = TypeVar('BotAppT')
  AppBotContextT = TypeVar('AppBotContextT')
  Context = TypeVar('Context')