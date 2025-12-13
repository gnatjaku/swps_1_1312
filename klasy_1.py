class Osoba:
    def __init__(self,imie,wiek,it):
        self.imie = imie
        self.wiek = wiek
        self.it = True

    def __del__(self):
        print("koniec instancji")

    def przywitaj(self):
        print("Hej, mam na imię: ",self.imie)


class Zwierzak:
    __wiek = 0

    def __init__(self):
        Zwierzak.__wiek += 1

    @staticmethod
    def kim_jestem(imie):
        print("Jestem sobie zwierzak o imieniu", imie)

    @classmethod
    def jaki_wiek(cls):
        print(cls.__wiek)

    def __str__(self):
        return "Jestem obiektem klasy zwierzak"
    # pass

# egzemplarze klasy

os1 = Osoba("Tomek",'45',False)
print(os1.imie)
os1.przywitaj()

zw1 = Zwierzak()
zw2 = Zwierzak()
zw1.kim_jestem("Azor")
print(zw1)
zw1.jaki_wiek()

del os1