import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import chetempofa_api
from services import openweather_servizio
from views import home

api = fastapi.FastAPI()

def configure():
    configure_routing()
    configure_api_keys()


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
    Configurazione della directory static e dei vari routers logici, in questa app:
    - home
    - api
    '''
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(chetempofa_api.router)

'''
Formato già adatto all'esecuzione in produzione, che sarà uvicorn modulo:var_name
uvicorn main:api
'''
if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
