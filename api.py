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

baza_ksiazek.extend([
    Ksiazka(id=4, tytul="Solaris", autor="Stanisław Lem", rok_wydania=1961, isbn="978-83-08-02000-1"),
    Ksiazka(id=5, tytul="Duma i uprzedzenie", autor="Jane Austen", rok_wydania=1813, isbn="978-83-240-0000-2"),
    Ksiazka(id=6, tytul="Zbrodnia i kara", autor="Fiodor Dostojewski", rok_wydania=1866, isbn="978-83-240-0000-3"),
    Ksiazka(id=7, tytul="Rok 1984", autor="George Orwell", rok_wydania=1949, isbn="978-83-240-0000-4"),
    Ksiazka(id=8, tytul="Folwark zwierzęcy", autor="George Orwell", rok_wydania=1945, isbn="978-83-240-0000-5"),
    Ksiazka(id=9, tytul="Mistrz i Małgorzata", autor="Michaił Bułhakow", rok_wydania=1967, isbn="978-83-240-0000-6"),
    Ksiazka(id=10, tytul="Imię róży", autor="Umberto Eco", rok_wydania=1980, isbn="978-83-240-0000-7"),
    Ksiazka(id=11, tytul="Sto lat samotności", autor="Gabriel García Márquez", rok_wydania=1967, isbn="978-83-240-0000-8"),
    Ksiazka(id=12, tytul="Diuna", autor="Frank Herbert", rok_wydania=1965, isbn="978-83-240-0000-9"),
    Ksiazka(id=13, tytul="Władca Pierścieni: Drużyna Pierścienia", autor="J.R.R. Tolkien", rok_wydania=1954, isbn="978-83-240-0001-0"),
])

licznik_id = 14

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

@app.get("/ksiazki/rok/{rok}", response_model=Wiadomosc, tags=["Książki"])
def get_ksiazki_by_rok(rok: int):

    ksiazki = [] # Lista książek wydanych w podanym roku

    for ksiazka in baza_ksiazek:
        if ksiazka.rok_wydania == rok:
            ksiazki.append(ksiazka)
    count = sum(1 for k in baza_ksiazek if k.rok_wydania == rok)

    return Wiadomosc(
        message=f"Liczba książek wydanych w roku {rok}: {count}, szczegóły: {ksiazki}",
        timestamp=datetime.now().isoformat()
    )


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

    if any(k.autor == nowa.autor and k.tytul == nowa.tytul for k in baza_ksiazek):
        raise HTTPException(status_code=400, detail="Książka o danym tytule i autorze już istnieje")


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