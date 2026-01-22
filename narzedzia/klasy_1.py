class Osoba:
    def __init__(self,imie,wiek,it):
        self.imie = imie
        self.wiek = wiek
        self.it = True

    def __del__(self):
        print("koniec instancji")

    def przywitaj(self):
        print("Hej, mam na imię: ",self.imie)

    def przedstaw_sie(self):
        print(f"Cześć, jestem {self.imie} i mam {self.wiek} lat.")


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

class Kot(Zwierzak):

    def __init__(self, imie, kolor_sierci):
        super().__init__()
        self.__imie = imie
        self.__kolor_sierci = kolor_sierci


    def przedstaw_sie(self):
        print(f"Jestem kotem, mam {self.__kolor_sierci} futro i na imię mi {self.__imie}.")
