from narzedzia.klasy_1 import Osoba, Zwierzak
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