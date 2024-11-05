from logging import getLogger

from aiohttp.web import AppRunner, TCPSite
from discord import Intents
from discord.ext import commands

from .bot import PetTheCordCog
from .cache import CachedPet
from .server import Server


class PetTheCord(commands.Bot):
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

        self._logger = getLogger(__name__)

    async def on_ready(self) -> None:
        await self.add_cog(PetTheCordCog(self._origin))
        await self.tree.sync()

        petter = CachedPet(
            self,
            self._caching,
            self._cache_path,
            self._cache_lifetime,
            self._cache_gc_delay
        )
        runner = AppRunner(Server(petter))
        await runner.setup()
        site = TCPSite(runner, self._host, self._port)
        await site.start()

        self._logger.info(f"Started serving on {self._host}:{self._port}")

        if self._caching:
            await petter.gc_loop()
