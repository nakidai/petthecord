from io import BytesIO

from aiohttp.web import Application, StreamResponse, get, Request, Response
from discord import NotFound, HTTPException
from discord.ext import commands
from petpetgif import petpet


class Server(Application):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

        self.add_routes([get("/{uid}", self.root)])

    async def root(self, request: Request) -> StreamResponse:
        try:
            uid = int(request.match_info["uid"][:request.match_info["uid"].find('.')])
        except ValueError:
            return Response(status=400)

        try:
            user = await self.client.fetch_user(uid)
        except NotFound:
            return Response(status=404)
        except HTTPException:
            return Response(status=403)

        if user.avatar is None:
            return Response(status=404)

        image = await user.avatar.read()
        dest = BytesIO()
        petpet.make(BytesIO(image), dest)
        dest.seek(0)

        return Response(body=dest.getvalue(), content_type="image/png")
