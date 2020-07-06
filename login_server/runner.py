from login_server.config import loop
from login_server.protocol.tcp import Lineage2LoginProtocol


async def main():
    server = await loop.create_server(
        lambda: Lineage2LoginProtocol(),
        "0.0.0.0", 2106)

    async with server:
        await server.serve_forever()


loop.run_until_complete(main())
