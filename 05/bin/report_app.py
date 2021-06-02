import requests

def main():
    scelta = input("Vuoi [R]iportare una segnalazione o [v]edere le segnalazioni? ")
    while scelta:
        if scelta.lower().strip() == 'r':
            riporta()
        elif scelta.lower().strip() == 'v':
            vedi()
        else:
            print(f"Nessuna opzione per {scelta}.")
        scelta = input("Vuoi [R]iportare una segnalazione o [v]edere le segnalazioni? ")

def riporta():
    '''
    Client della post
    '''
    desc = input("Cosa sta succedendo? ")
    citta = input("In che città? ")
    data = {
        "descrizione": desc,
        "localita": {
            "citta": citta
        }
    }
    url = "http://127.0.0.1:8000/api/reports"
    resp = requests.post(url, json=data)
    resp.raise_for_status()
    result = resp.json()
    print(f"Id segnalazione riportata: {result.get('id')}")


def vedi():
    '''
    Client della get
    '''
    url = "http://127.0.0.1:8000/api/reports"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    for r in data:
        print(f"{r.get('localita').get('citta')} - {r.get('descrizione')}")


if __name__ == '__main__':
    main()