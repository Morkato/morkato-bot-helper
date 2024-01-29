from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from discord.interactions import Interaction

  from morkato.bot import BotApp

from discord.interactions import Interaction
from discord.ui import Modal, TextInput
from discord import TextStyle

class TriggerCreateModal(Modal):
  name = TextInput(label="Name", min_length=2, max_length=96, custom_id="trigger.name")
  content = TextInput(label="Content", min_length=2, max_length=4000, custom_id="trigger.content", style=TextStyle.long)

  async def on_submit(self, interaction: Interaction[BotApp]) -> None:
    guild = await interaction.client.get_morkato_guild(interaction.guild)

    trigger = await guild.create_trigger(name=str(self.name), content=str(self.content))

    await interaction.response.send_message("Foi criado um novo trigger chamado: **`%s`**." % trigger.name)