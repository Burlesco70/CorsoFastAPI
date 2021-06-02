from typing import Optional, List

import fastapi
from fastapi import Depends

from models.localita import Localita
from models.errore_in_validazione import ValidationError
from models.reports import Report, ReportUtente
from services import openweather_servizio, report_servizio


router = fastapi.APIRouter()


@router.get('/api/chetempofa/{citta}', name='che_tempo_fa')
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

@router.get('/api/reports', name='lista_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    # Prova http://127.0.0.1:8000/api/reports
    
    # Per testare get prima di aver creato post
    await report_servizio.add_report("Sempre il sole", Localita(citta="Biella"))
    await report_servizio.add_report("Temporale", Localita(citta="Milano"))

    # Serve await perchè il servizio è async
    return await report_servizio.get_reports()


@router.post('/api/reports', name='aggiunta_report', status_code=201, response_model=Report)
async def reports_post(report_utente: ReportUtente) -> Report:
    '''
    Per la creazione di un entita, Report in
    questo caso il corretto status code da ritornare è 201
    essendo una creazione
    '''
    d = report_utente.descrizione
    loc = report_utente.localita

    return await report_servizio.add_report(d, loc)