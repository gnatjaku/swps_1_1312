try:
    x = int(input("Podaj liczbę: "))
    wynik = 10 / x
except ZeroDivisionError:
    print("wystąpił błąd")
except ValueError:
    print("To nie jest liczba")
else:
    print(wynik)
    f = open("test.txt", "w")
    f.write(str(wynik))
finally:
    print("zakończono działanie programu")

wiek = -5
if wiek < 0:
    raise ValueError("Wiek nie może być ujemny")


try:
    x = int(input())
    print(10 / x)
except (ValueError, ZeroDivisionError):
    print("Błędne dane wejściowe")

# antywzorzec
try:
    x = int(input("Podaj liczbę: "))
    wynik = 10 / x
except:
    print("To nie jest liczba")