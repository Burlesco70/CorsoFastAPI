import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import chetempofa_api
from services import openweather_servizio, report_servizio
from views import home
from models.localita import Localita

# api = fastapi.FastAPI(dcs_url=None) per non pubblicare la documentazione
api = fastapi.FastAPI()

def configure():
    configure_templates_and_static()
    configure_routing()
    configure_api_keys()

def configure_templates_and_static():
    # No templates con Jinja, servono per altri tipi di templates
    # Mount della cartella statica
    api.mount('/static', StaticFiles(directory='static'), name='static')

def configure_api_keys():
    '''
    Carica il file di configurazione con la chiave api
    '''
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file di configurazione non trovato; guarda le note nel file settings_template.json")
        raise Exception("settings.json file non trovato, manca la chiave api; guarda le note sotto settings_template.json")

    with open('settings.json') as fin:
        settings = json.load(fin)
        openweather_servizio.api_key = settings.get('api_key')


def configure_routing():
    '''
    Configurazione dei vari routers logici, in questa app:
    - home
    - api
    '''
    api.include_router(home.router)
    api.include_router(chetempofa_api.router)

def configure_fake_data():
    # Dati solo per testare
    loop = None
    try:
        loop = asyncio.get_running_loop()
        print("got loop!", loop)
    except RuntimeError:
        pass  # Boo, why can't I just get nothing back?

    if not loop:
        loop = asyncio.get_event_loop()

    try:
        loc = Localita(citta="Cossato", nazione="IT")
        loop.run_until_complete(report_servizio.add_report("Tempo variabile", loc))
        loop.run_until_complete(report_servizio.add_report("Temporale in arrivo", loc))
    except RuntimeError:
        print("Note: Could not import starter date, this fails on some systems and "
              "some ways of running the app under uvicorn.")
        print("Dati fake non caricati.")


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
