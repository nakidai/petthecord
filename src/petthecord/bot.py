from aiohttp.web import AppRunner, TCPSite
from discord import Intents
from discord.ext import commands

from .server import Server


class Bot(commands.Bot):
    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        super().__init__(
            command_prefix="!",
            intents=Intents.default()
        )
        self._host = host
        self._port = port

    async def on_ready(self) -> None:
        runner = AppRunner(Server(self))
        await runner.setup()
        site = TCPSite(runner, self._host, self._port)
        await site.start()
