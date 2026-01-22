from narzedzia.klasy_1 import Osoba, Zwierzak, Kot
from dziedziczenie import Pies
import sys


os1 = Osoba("Tomek",'45',False)
print(os1.imie)
os1.przywitaj()

zw1 = Zwierzak()
zw2 = Zwierzak()
zw1.kim_jestem("Azor")
print(zw1)
zw1.jaki_wiek()

p1 = Pies("azorek", rasa="mopsik")
print(sys.path)

os2 = Osoba("Jakub",'48',True)
os2.przedstaw_sie()


kot1 = Kot("Muza","szare")
kot1.przedstaw_sie()