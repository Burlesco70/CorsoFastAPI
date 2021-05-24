import datetime
from typing import Optional, Tuple

# Cache in memoria con variabile privata
__cache = {}
durata_in_ore = 1.0


def get_meteo(citta: str, regione: Optional[str], nazione: str, udm: str) -> Optional[dict]:
    '''
    Utilizza gli stessi argomenti del servizio API
    e restituisce un valore solo se presente nella cache
    entro la durata stabilita da durata_in_ore
    '''
    key = __crea_chiave(citta, regione, nazione, udm)
    data: dict = __cache.get(key)
    if not data:
        return None

    last = data['time']
    dt = datetime.datetime.now() - last
    # dt / datetime.timedelta(minutes=60) ci dice la durata in ore
    # tra ora e l'ultimo valore nella cache
    # Se entro l'ora ritorna il valore...
    if dt / datetime.timedelta(minutes=60) < durata_in_ore:
        #print("Usata cache in memoria",key)
        return data['value']
    # altrimenti cancella la chiave
    del __cache[key]
    return None


def set_meteo(citta: str, regione: str, nazione: str, udm: str, value: dict):
    key = __crea_chiave(citta, regione, nazione, udm)
    data = {
        'time': datetime.datetime.now(),
        'value': value
    }
    __cache[key] = data
    __pulisci_scaduti()


def __crea_chiave(citta: str, regione: str, nazione: str, udm: str) -> Tuple[str, str, str, str]:
    if not citta or not nazione or not udm:
        raise Exception("Città, nazione, e unità di misura sono obbligatorie")

    if not regione:
        regione = ""

    return citta.strip().lower(), regione.strip().lower(), nazione.strip().lower(), udm.strip().lower()


def __pulisci_scaduti():
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get('time')
        if dt / datetime.timedelta(minutes=60) > durata_in_ore:
            del __cache[key]