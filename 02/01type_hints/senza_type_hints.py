from collections import namedtuple

Elemento = namedtuple("Elemento", "voce, prezzo")

costo_massimo = None


def calcola_costo(elementi):
    global costo_massimo
    total = 0

    for e in elementi:
        total += e.prezzo

    if not costo_massimo or total > costo_massimo:
        costo_massimo = total

    return total


def main():
    print("Inseriamo i pasti consumati nel giorno")

    cena = [Elemento('Pizza', 20), Elemento('Birra', 9), Elemento('Birra', 9)]
    colazione = [Elemento('Pancakes', 11), Elemento('Bacon', 4), Elemento('Caffè', 3), Elemento('Caffè', 3), Elemento('Brioche', 2)]

    totale_cena = calcola_costo(cena)
    print(f"Costo cena EUR {totale_cena:,.02f}")

    totale_colazione = calcola_costo(colazione)
    print(f"Costo colazione EUR {totale_colazione:,.02f}")

    print(f"Oggi il costo più elevato è stato EUR {costo_massimo:.02f}")


if __name__ == '__main__':
    main()