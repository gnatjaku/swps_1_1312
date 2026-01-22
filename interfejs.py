from abc import ABC, abstractmethod

class Zwierzak(ABC):

    @abstractmethod
    def przedstaw_sie(self):
        pass


class Kot(Zwierzak):
    def przedstaw_sie(self):
        print("Miau")


k = Kot()
