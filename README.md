# ZadaniePython – FastAPI + MCP

Masz API FastAPI w pliku `api.py` (endpointy `/ksiazki`).

Żeby dodać to jako MCP (Model Context Protocol), najprościej uruchomić **adapter MCP** jako osobny proces, który wystawia narzędzia MCP i pod spodem woła Twoje HTTP API.

## Instalacja

Użyj venv i zależności z `requirements.txt`.

## Uruchomienie FastAPI

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Test (powinno zwrócić listę książek):

```bash
curl http://127.0.0.1:8000/ksiazki
```

## Uruchomienie MCP (adapter)

Adapter MCP jest w `mcp_server.py`.

Ustaw (opcjonalnie) gdzie działa FastAPI:

```bash
export FASTAPI_BASE_URL=http://127.0.0.1:8000
```

Następnie uruchom MCP w trybie stdio (najprostszy i najczęściej używany przez klientów MCP):

```bash
python3 mcp_server.py
```

Adapter udostępnia tools:
- `list_books(autor?)`
- `get_book(ksiazka_id)`
- `create_book(tytul, autor, rok_wydania?, isbn?)`

## Dlaczego adapter, a nie „FastAPI jako MCP”?

MCP to osobny protokół/transport (stdio/SSE), a FastAPI jest HTTP JSON. Adapter pozwala:
- zostawić Twoje API bez zmian,
- wystawić je jako MCP dla agentów/klientów MCP,
- mieć jasną separację: logika domeny (FastAPI) vs integracja (MCP).

Jeśli podasz, jakiego klienta MCP używasz (stdio czy SSE), mogę dopisać dokładną konfigurację i wariant SSE.
