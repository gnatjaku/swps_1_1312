import csv

# with open("ceny.csv", newline='', encoding="utf-8") as f:
#     reader = csv.reader(f, delimiter=';')
#     for row in reader:
#         print(row)


sumy = {}
liczniki = {}

with open("ceny.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        data = row['data']
        produkt = row['produkt']
        ilosc = row['ilosc']
        cena = float(row['cena'].replace(',', '.'))

        sumy[produkt] = sumy.get(produkt, 0) + cena

        liczniki[produkt] = liczniki.get(produkt, 0) + 1



with open("ceny3.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["produkt","srednia"])
    for produkt in sumy:
        srednia = round(sumy[produkt] / liczniki[produkt], 2)
        writer.writerow([produkt,srednia])