from aiohttp.web import AppRunner, TCPSite
from discord import app_commands, Interaction, Intents, User
from discord.ext import commands

from .server import Server


class PatTheCordCog(commands.Cog):
    def __init__(self, client: commands.Bot, origin: str = "https://ptc.pwn3t.ru") -> None:
        self.client = client
        self.origin = origin

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
        await interaction.response.send_message(f"{self.origin}/{user.id}.{r}.gif")


class Bot(commands.Bot):
    def __init__(
        self,

        host: str = "127.0.0.1",
        port: int = 8080,
        origin: str = "https://ptc.pwn3t.ru",
        caching: bool = True,
        cache_path: str = "/var/cache/petthecord",
        cache_lifetime: int = 86400,
        cache_gc_delay: int = 14400,
    ) -> None:
        super().__init__(
            command_prefix="!",
            intents=Intents.default()
        )
        self._host = host
        self._port = port
        self._origin = origin
        self._caching = caching
        self._cache_path = cache_path
        self._cache_lifetime = cache_lifetime
        self._cache_gc_delay = cache_gc_delay

    async def on_ready(self) -> None:
        await self.add_cog(PatTheCordCog(self, self._origin))
        await self.tree.sync()

        server = Server(
            self,
            self._caching,
            self._cache_path,
            self._cache_lifetime,
            self._cache_gc_delay
        )
        runner = AppRunner(server)
        await runner.setup()
        site = TCPSite(runner, self._host, self._port)
        await site.start()

        if self._caching:
            await server.clean_cache()
