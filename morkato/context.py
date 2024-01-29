from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  List
)

if TYPE_CHECKING:
  from discord.message import Message
  from discord.embeds import Embed

from discord.ext.commands.context import Context

from .types._etc import BotAppT
from .utils.etc import reaction_checker

class AppBotContext(Context[BotAppT]):
  async def send_page_embed(self, embeds: List[Embed]) -> Message:
    message = await self.send(embed=embeds[0])

    length = len(embeds)

    if length == 1:
      return
    
    index = 0

    await message.add_reaction('⏪')
    await message.add_reaction('⏩')

    while True:
      try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check=reaction_checker(self, message, [ 'author', 'channel', 'guild', 'message' ]))
      except:
        await message.clear_reactions()

        return message
      
      if str(reaction.emoji) == '⏪':
        index = length - 1 if index == 0 else index - 1

        await message.remove_reaction('⏪', user)
      elif str(reaction.emoji) == '⏩':
        index = 0 if index + 1 == length else index + 1

        await message.remove_reaction('⏩', user)

      await message.edit(embed=embeds[index])