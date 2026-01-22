"""Minimalny probe do wypisania narzędzi z MCP servera (transport stdio).

Uruchom:
  ./.venvubuntu/bin/python3 tools/list_mcp_tools.py

Wymaga: mcp (sdk), python>=3.10
"""

from __future__ import annotations

import asyncio
import sys

from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


async def main() -> None:
    server = StdioServerParameters(
        command="/media/jakub/4A0826CD0826B839/Users/jakub/PycharmProjects/ZadaniePython/.venvubuntu/bin/python3",
        args=[
            "/media/jakub/4A0826CD0826B839/Users/jakub/PycharmProjects/ZadaniePython/mcp_server.py"
        ],
        env={
            "FASTAPI_BASE_URL": "http://127.0.0.1:8000",
        },
    )

    # errlog pokaże stderr subprocessa, jeśli serwer się wysypie przy starcie
    async with stdio_client(server, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.list_tools()

    tools = getattr(res, "tools", res)
    for t in tools:
        print(f"- {t.name}: {t.description}")


if __name__ == "__main__":
    asyncio.run(main())
