import json
#
# # Słownik Pythona
# dane = {
#     "imie": 'Anna',
#     'wiek': 28,
#     "umiejetnosci": ["Python", "SQL"]
# }
#
# # Zapisz do pliku JSON
# with open('dane.json', 'w') as f:
#     json.dump(dane, f, indent=2)
#
# # Zapisz jako string JSON
# json_string = json.dumps(dane)


# Wczytaj z pliku JSON
with open('dane.json', 'r') as f:
    wczytane = json.load(f)

print(wczytane['imie'])  # Anna
print(wczytane['umiejetnosci'])
print(wczytane['umiejetnosci'][0])

# Parse JSON string
json_str = '{"klucz": "wartość"}'
obiekt = json.loads(json_str)
print(obiekt)