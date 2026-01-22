class Lata:
    gatunek = "Lot"
    def lec(self):
        print("Lecę")

class Plywa:
    def plywaj(self):
        print("Płynę")

class Kaczka(Plywa,Lata):
    pass

print(Kaczka.mro())
print(Kaczka.gatunek)