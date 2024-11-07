from logging import getLogger

from discord import app_commands, Interaction, User
from discord.ext import commands

from .defaults import Defaults


class PetTheCordCog(commands.Cog):
    def __init__(self, origin: str = Defaults.Network.ORIGIN) -> None:
        self._origin = origin
        super().__init__()

        self._logger = getLogger(__name__)

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(
        name="petpet",
        description="Pet some user"
    )
    @app_commands.describe(
        user="User to pet",
        r="Some random stuff, set it if avatar is not up to date"
    )
    async def petthecord(
        self,
        interaction: Interaction,

        user: User,
        r: str = ""
    ) -> None:
        self._logger.info(f"Petting {user.id} for {interaction.user.id}")
        await interaction.response.send_message(f"{self._origin}/{user.id}.{r}.gif")
