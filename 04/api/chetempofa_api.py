from typing import Optional

import fastapi
from fastapi import Depends

from models.localita import Localita
from models.errore_in_validazione import ValidationError
from services import openweather_servizio


router = fastapi.APIRouter()


@router.get('/api/chetempofa/{citta}')
async def chetempofa(loc: Localita = Depends(), udm: Optional[str] = 'metric'):
    try:
        return await openweather_servizio.get_report_async(loc.citta, loc.regione, loc.nazione, udm)
    # Errori di validazione
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    # Errori generici, di più basso livello
    except Exception as x:
        # manca parte di logging... temporaneamente uso print
        print(f"Errore dal server: {x}")
        return fastapi.Response(content=str(x), status_code=500)