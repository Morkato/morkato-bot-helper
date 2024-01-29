from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from discord.interactions import Interaction
  from morkato.bot import BotApp

from discord.ext.commands.cog import Cog

from discord.app_commands.commands import command, rename
from discord.app_commands.checks import has_permissions
from app.modals.trigger import TriggerCreateModal

class TriggerCog(Cog):
  @command(
    name="tcreate",
    description="[Moderação] Cria um trigger"
  )
  @has_permissions(manage_guild=True, manage_messages=True)
  async def trigger_create(self, interaction: Interaction[BotApp]) -> None:
    if interaction.guild is None:
      await interaction.response.send_message("Esse comando pode somente pode ser executado em servidores.")

      return
    
    modal = TriggerCreateModal(title="Create Trigger", timeout=300)

    await interaction.response.send_modal(modal)
  
  @command(
    name="tdelete",
    description="[Moderção] Deleta um trigger"
  )
  @has_permissions(manage_guild=True, manage_messages=True)
  @rename(name="trigger")
  async def trigger_delete(self, interaction: Interaction, name: str) -> None:
    if interaction.guild is None:
      await interaction.response.send_message("Esse comando pode somente pode ser executado em servidores.")

      return
    
    await interaction.response.defer()
    
    guild = await interaction.client.get_morkato_guild(interaction.guild)
    trigger = await guild.get_trigger(name)

    if trigger is None:
      await interaction.edit_original_response(content="Esse trigger não existe.")

      return

    await trigger.delete()

    await interaction.edit_original_response(content="O trigger chamado: **`%s`** foi deletado." % trigger.name)

async def setup(bot: BotApp) -> None:
  await bot.add_cog(TriggerCog())