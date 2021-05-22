from typing import Optional

from pydantic import BaseModel


class Localita(BaseModel):
    citta: str
    regione: Optional[str] = None
    nazione: str = 'it'