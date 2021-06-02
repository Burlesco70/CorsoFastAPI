from typing import Optional, Tuple
import httpx
from httpx import Response

from infrastructure import meteo_cache
from models.errore_in_validazione import ValidationError

api_key: Optional[str] = None


async def get_report_async(citta: str, regione: Optional[str], nazione: str, udm: str) -> dict:
    citta, regione, nazione, udm = valida(citta, regione, nazione, udm)
    # Prima cerca nella cache in memoria
    previsione = meteo_cache.get_meteo(citta, regione, nazione, udm)
    if previsione:
        return previsione
    
    # Altrimenti richiama il servizio
    if regione:
        q = f'{citta},{regione},{nazione}'
    else:
        q = f'{citta},{nazione}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&lang=it&appid={api_key}&units={udm}'
    #print(url)

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)
        #resp.raise_for_status()

    data = resp.json()
    previsione = data['main']

    # Salvo in cache
    meteo_cache.set_meteo(citta, regione, nazione, udm, previsione)

    return previsione

def valida(citta: str, regione: Optional[str], nazione: Optional[str], udm: str) -> \
        Tuple[str, Optional[str], str, str]:
    citta = citta.lower().strip()
    if not nazione:
        nazione = "it"
    else:
        nazione = nazione.lower().strip()

    if len(nazione) != 2:
        error = f"Nazione non valida: {nazione}. Deve essere di due lettere e abbreviazione codice ISO (es. IT o  US)"
        raise ValidationError(status_code=400, error_msg=error)

    if regione:
        regione = regione.strip().lower()

    if regione and len(regione) != 2:
        error = f"Regione non valida, da usare solo per USA: {regione}. Deve essere di due lettere, come ad esempio CA o KS."
        raise ValidationError(status_code=400, error_msg=error)

    if udm:
        udm = udm.strip().lower()

    valid_udm = {'standard', 'metric', 'imperial'}
    if udm not in valid_udm:
        error = f"Invalid units '{udm}', it must be one of {valid_udm}."
        raise ValidationError(status_code=400, error_msg=error)

    return citta, regione, nazione, udm    