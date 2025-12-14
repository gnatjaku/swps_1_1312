from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# MODELE DANYCH

class Ksiazka(BaseModel):
    id: int
    tytul: str = Field(..., min_length=1, max_length=200, description="Tytuł książki")
    autor: str = Field(..., min_length=1, max_length=100, description="Autor książki")
    rok_wydania: Optional[int] = Field(None, ge=1000, le=2100, description="Rok wydania")
    isbn: Optional[str] = Field(None, description="ISBN")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "tytul": "Wiedźmin",
                "autor": "Andrzej Sapkowski",
                "rok_wydania": 1990,
                "isbn": "978-83-7391-000-0"
            }
        }
    )

class KsiazkaCreate(BaseModel):
    tytul: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    rok_wydania: Optional[int] = Field(None, ge=1000, le=2100)
    isbn: Optional[str] = None

class Wiadomosc(BaseModel):
    message: str
    timestamp: str

# Aplikacja FastAPI

app = FastAPI(
    title="API Biblioteki",
    description="Proste API do zarządzania kolekcją książek",
    version="1.0.0"
)

#  Baza w pamięci

baza_ksiazek: List[Ksiazka] = [
    Ksiazka(id=1, tytul="Wiedźmin", autor="Andrzej Sapkowski", rok_wydania=1990),
    Ksiazka(id=2, tytul="Lalka", autor="Bolesław Prus", rok_wydania=1896),
    Ksiazka(id=3, tytul="Pan Tadeusz", autor="Adam Mickiewicz", rok_wydania=1834),
]

licznik_id = 4

# Endpoint

@app.get("/", response_model=Wiadomosc, tags=["Info"])
def root():
    return Wiadomosc(
        message="Witaj w API Biblioteki!",
        timestamp=datetime.now().isoformat()
    )

@app.get("/status", tags=["Info"])
def status():
    return {
        "status": "OK",
        "liczba_ksiazek": len(baza_ksiazek),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ksiazki", response_model=List[Ksiazka], tags=["Książki"])
def get_ksiazki(autor: Optional[str] = None):
    if autor:
        return [k for k in baza_ksiazek if autor.lower() in k.autor.lower()]
    return baza_ksiazek

@app.get("/ksiazki/{ksiazka_id}", response_model=Ksiazka, tags=["Książki"])
def get_ksiazka(ksiazka_id: int):
    for ksiazka in baza_ksiazek:
        if ksiazka.id == ksiazka_id:
            return ksiazka
    raise HTTPException(status_code=404, detail="Książka nie znaleziona")


@app.post("/ksiazki", response_model=Ksiazka, status_code=201, tags=["Książki"])
def create_ksiazka(data: KsiazkaCreate):
    global licznik_id

    nowa = Ksiazka(
        id=licznik_id,
        tytul=data.tytul,
        autor=data.autor,
        rok_wydania=data.rok_wydania,
        isbn=data.isbn
    )

    baza_ksiazek.append(nowa)
    licznik_id += 1

    return nowa

@app.put("/ksiazki/{ksiazka_id}", response_model=Ksiazka, tags=["Książki"])
def update_ksiazka(ksiazka_id: int, data: KsiazkaCreate):
    for i, ksiazka in enumerate(baza_ksiazek):
        if ksiazka.id == ksiazka_id:
            updated = Ksiazka(
                id=ksiazka_id,
                tytul=data.tytul,
                autor=data.autor,
                rok_wydania=data.rok_wydania,
                isbn=data.isbn
            )
            baza_ksiazek[i] = updated
            return updated

@app.delete("/ksiazki/{ksiazka_id}", status_code=204, tags=["Książki"])
def delete_ksiazka(ksiazka_id: int):
    for i, ksiazka in enumerate(baza_ksiazek):
        if ksiazka.id == ksiazka_id:
            baza_ksiazek.pop(i)
            return
    raise HTTPException(status_code=404, detail="Książka nie znaleziona")


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
   - API: http://127.0.0.1:8000 lub http://localhost:8000 

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