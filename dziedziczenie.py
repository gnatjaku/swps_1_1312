class Zwierzak:
    def __init__(self, imie):
        self.imie = imie

    def przedstaw_sie(self):
        print("Jestem zwierzakiem")


class Pies(Zwierzak):
    def __init__(self, imie, rasa):
        super().__init__(imie)
        self.rasa = rasa

    def przedstaw_sie(self):
        super().przedstaw_sie()
        print("Jestem psem o imieniu", self.imie)


# p1 = Pies("Azor", "mops")
# p1.przedstaw_sie()
