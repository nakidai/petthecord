from io import BytesIO
from logging import getLogger

from discord import app_commands, File, Interaction, User
from discord.ext import commands

from .defaults import Defaults
from .petter import Petter, HTTPException, NotFound


class PetTheCordCog(commands.Cog):
    def __init__(
        self,

        origin: str = Defaults.Network.ORIGIN,
        petter: Petter | None = None,
    ) -> None:
        self._origin = origin
        self._petter = petter or Petter()
        super().__init__()

        self._logger = getLogger(__name__)

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(
        name="petpetlink",
        description="Pet some user and take a link",
    )
    @app_commands.describe(
        user="User to pet",
        r="Some random stuff, set it if avatar is not up to date",
    )
    async def petwithlink(
        self,
        interaction: Interaction,

        user: User,
        r: str = "",
    ) -> None:
        self._logger.info(f"Petting {user.id} with link for {interaction.user.id}")
        await interaction.response.send_message(f"{self._origin}/{user.id}.{r}.gif")

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(
        name="petpet",
        description="Pet some user and take a link"
    )
    @app_commands.describe(
        user="User to pet",
    )
    async def petwithgif(
        self,
        interaction: Interaction,

        user: User,
    ) -> None:
        self._logger.info(f"Petting {user.id} with gif for {interaction.user.id}")
        try:
            await interaction.response.send_message(
                file=File(
                    BytesIO(await self._petter.petpet(user)),
                    filename=f"{user.id}.gif"
                )
            )
        except HTTPException:
            self._logger.error(f"Couldn't pet {user.id}")
            await interaction.response.send_message(
                "Couldn't pet your user :<",
                ephemeral=True,
            )
        except NotFound:
            await interaction.response.send_message(
                "Avatar or user was not found :<",
                ephemeral=True,
            )
