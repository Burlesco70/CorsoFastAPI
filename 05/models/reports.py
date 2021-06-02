import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from models.localita import Localita


class ReportUtente(BaseModel):
    '''
    Dataclass Pydantic con campi inseriti dall'utente
    '''
    descrizione: str
    localita: Localita


class Report(ReportUtente):
    '''
    Classe interna per DB con campi calcolati, estensione di ReportUtente
    '''
    id: str
    data_creazione: Optional[datetime.datetime]