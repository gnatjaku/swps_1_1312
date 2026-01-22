"""MCP adapter for FastAPI bibliotek API.

Ten moduł wystawia narzędzia MCP (tools), a w środku wywołuje Twoje HTTP API z `api.py`.

Założenia:
- FastAPI działa pod `FASTAPI_BASE_URL` (domyślnie http://127.0.0.1:8000)
- MCP uruchamiasz jako osobny proces:
  - transport stdio (najprostszy) albo
  - transport SSE (gdy potrzebujesz po HTTP)

Uwaga: szczegóły uruchomienia zależą od klienta MCP. Ten plik jest celowo mały i czytelny.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx

# Oficjalne SDK MCP
from mcp.server import Server
from mcp.types import Tool, TextContent


FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

server = Server("biblioteka-mcp")


async def _request(method: str, path: str, **kwargs: Any) -> Any:
    url = f"{FASTAPI_BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.request(method, url, **kwargs)
        # FastAPI zwraca JSON z detail przy błędach
        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise RuntimeError(f"HTTP {resp.status_code} calling {url}: {detail}")
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return resp.text


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_books",
            description="Zwraca listę książek. Opcjonalnie filtruje po autorze.",
            inputSchema={
                "type": "object",
                "properties": {
                    "autor": {"type": "string", "description": "Fragment imienia/nazwiska autora"}
                },
            },
        ),
        Tool(
            name="get_book",
            description="Zwraca jedną książkę po id.",
            inputSchema={
                "type": "object",
                "properties": {"ksiazka_id": {"type": "integer", "description": "ID książki"}},
                "required": ["ksiazka_id"],
            },
        ),
        Tool(
            name="create_book",
            description="Dodaje nową książkę.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tytul": {"type": "string"},
                    "autor": {"type": "string"},
                    "rok_wydania": {"type": "integer"},
                    "isbn": {"type": "string"},
                },
                "required": ["tytul", "autor"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "list_books":
        autor: Optional[str] = arguments.get("autor")
        params = {"autor": autor} if autor else None
        data = await _request("GET", "/ksiazki", params=params)
        return [TextContent(type="text", text=str(data))]

    if name == "get_book":
        ksiazka_id = int(arguments["ksiazka_id"])
        data = await _request("GET", f"/ksiazki/{ksiazka_id}")
        return [TextContent(type="text", text=str(data))]

    if name == "create_book":
        payload: dict[str, Any] = {
            "tytul": arguments.get("tytul"),
            "autor": arguments.get("autor"),
            "rok_wydania": arguments.get("rok_wydania"),
            "isbn": arguments.get("isbn"),
        }
        # usuń None, żeby walidacja FastAPI nie dostawała pustych pól
        payload = {k: v for k, v in payload.items() if v is not None}
        data = await _request("POST", "/ksiazki", json=payload)
        return [TextContent(type="text", text=str(data))]

    raise RuntimeError(f"Unknown tool: {name}")


def main() -> None:
    """Uruchom MCP server (transport stdio)."""

    import anyio
    from mcp.server.stdio import stdio_server

    async def _run() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    anyio.run(_run)


if __name__ == "__main__":
    main()
