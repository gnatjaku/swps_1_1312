import csv
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

sumy = {}
liczniki = {}
laczna_wartosc = {}

logger = logging.getLogger("ceny_logger")

with open("ceny.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        data = row['data']
        produkt = row['produkt']
        ilosc = row['ilosc']
        cena = float(row['cena'].replace(',', '.'))

        sumy[produkt] = sumy.get(produkt, 0) + cena
        liczniki[produkt] = liczniki.get(produkt, 0) + 1
        logger.info(f"Produkt: {produkt}, ilość: {ilosc}, cena: {cena} lączna wartość {cena * int(ilosc)}")
        laczna_wartosc[produkt] = laczna_wartosc.get(produkt, 0) + cena * int(ilosc)


with open("ceny3.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["produkt","srednia","łączna_wartość"])
    for produkt in sumy:
        srednia = round(sumy[produkt] / liczniki[produkt], 2)
        writer.writerow([produkt,srednia,laczna_wartosc[produkt]])