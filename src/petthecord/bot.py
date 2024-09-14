from aiohttp.web import AppRunner, TCPSite
from discord import app_commands, Interaction, Intents, User
from discord.ext import commands

from .server import Server


class PatTheCordCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(
        name="petpet",
        description="Pat some user"
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
        await interaction.response.send_message(f"https://ptc.nakidai.ru/{user.id}.{r}.gif")


class Bot(commands.Bot):
    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        super().__init__(
            command_prefix="!",
            intents=Intents.default()
        )
        self._host = host
        self._port = port

    async def on_ready(self) -> None:
        await self.add_cog(PatTheCordCog(self))
        await self.tree.sync()

        runner = AppRunner(Server(self))
        await runner.setup()
        site = TCPSite(runner, self._host, self._port)
        await site.start()
