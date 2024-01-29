from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from sys import _ExitCode

from sys import exit

import os

def main() -> _ExitCode:
  BOT_TOKEN: str = os.getenv('BOT_TOKEN')

  if BOT_TOKEN is None:
    print("Insira no \".env\" a chave BOT_TOKEN com o token de autorização do discord.")

    return 1
  
  setup_logging()

  bot = BotApp('/', intents=Intents.all())

  print(bot._state.modules)

  bot.run(BOT_TOKEN)

  return 0

if __name__ == '__main__':
  from dotenv import load_dotenv

  load_dotenv()
  
  from morkato.utils.logging import setup_logging
  
  from discord.flags import Intents
  from morkato.bot import BotApp

  exit(main())