import datetime
import uuid
from typing import List

from models.localita import Localita
from models.reports import Report

# Finto DB come lista in memoria
__reports: List[Report] = []


async def get_reports() -> List[Report]:
    '''
    Lista dei reports
    '''
    # Dovrebbe esserci una chiamata asincrona qui per legere dal DB...
    return list(__reports)


async def add_report(descrizione: str, localita: Localita) -> Report:
    '''
    Funzione per l'aggiunta di report per una certa localita
    Utilizzo di uuid per fake id
    '''
    now = datetime.datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        localita=localita,
        descrizione=descrizione,
        data_creazione=now)

    # Simula il salvataggio su DB ... manca questa parte per mantenere tutto semplice
    # Dovrebbe esserci una chiamata asincrona qui per scrivere sul DB...
    __reports.append(report)
    # Ordina per data creazione decrescente
    __reports.sort(key=lambda r: r.data_creazione, reverse=True)

    return report