class Osoba:
    def __init__(self,imie,wiek):
        self.imie = imie
        self.wiek = wiek # pole, które działa na podstawie metody

    def przywitaj(self):
        print("Hej, mam na imię: ",self.imie)

    @property
    def wiek(self):
        return self._wiek

    @wiek.setter
    def wiek(self,value):
        if value < 0:
            raise ValueError("Wiek nie może być ujemny")
        self._wiek = value

    @wiek.deleter
    def wiek(self):
        print("Usuwam wiek")
        del self._wiek


# egzemplarze klasy


o = Osoba("Tomek", 10)
o.przywitaj()
o.wiek = 456
# del o.wiek
print(o.wiek)