from typing import Optional
import httpx

api_key: Optional[str] = None


async def get_report_async(citta: str, regione: Optional[str], nazione: str, udm: str) -> dict:
    if regione:
        q = f'{citta},{regione},{nazione}'
    else:
        q = f'{citta},{nazione}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&lang=it&appid={api_key}&units={udm}'
    #print(url)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    data = resp.json()
    previsione = data['main']
    return previsione