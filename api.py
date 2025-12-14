from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime



# ============== INSTRUKCJE URUCHOMIENIA ==============

"""
Aby uruchomić, wykonaj następujące kroki:

1. Zainstaluj wymagane pakiety:
   pip install fastapi uvicorn pydantic

2. Uruchom serwer:
   uvicorn nazwa_pliku:app --reload

3. Otwórz w przeglądarce:
   - Dokumentacja Swagger UI: http://127.0.0.1:8000/docs
   - Dokumentacja ReDoc: http://127.0.0.1:8000/redoc
   - API: http://127.0.0.1:8000

4. Przykładowe zapytania (w terminalu powershell lub cmd z dostępnym curl):

   # Pobierz wszystkie książki
   curl http://127.0.0.1:8000/ksiazki

   # Pobierz książkę o ID 1
   curl http://127.0.0.1:8000/ksiazki/1

   # Dodaj nową książkę
   curl -X POST http://127.0.0.1:8000/ksiazki \
     -H "Content-Type: application/json" \
     -d '{"tytul":"Hobbit","autor":"J.R.R. Tolkien","rok_wydania":1937}'

   # Aktualizuj książkę
   curl -X PUT http://127.0.0.1:8000/ksiazki/1 \
     -H "Content-Type: application/json" \
     -d '{"tytul":"Wiedźmin (edycja rozszerzona)","autor":"Andrzej Sapkowski"}'

   # Usuń książkę
   curl -X DELETE http://127.0.0.1:8000/ksiazki/1
   
   !!!UWAGA NA '' w wierszu polecenia - stosuj \"
"""