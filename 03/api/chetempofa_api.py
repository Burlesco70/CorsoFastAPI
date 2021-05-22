from typing import Optional

import fastapi
from fastapi import Depends

from models.localita import Localita
from services import openweather_servizio

router = fastapi.APIRouter()


@router.get('/api/chetempofa/{citta}')
async def chetempofa(loc: Localita = Depends(), udm: Optional[str] = 'metric'):
    report = await openweather_servizio.get_report_async(loc.citta, loc.regione, loc.nazione, udm)

    return report
