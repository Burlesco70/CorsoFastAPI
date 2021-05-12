import datetime
from typing import List, Optional

from dateutil.parser import parse
from pydantic import BaseModel

ordine_json = {
    'elemento_id': '123',
    'data_creazione': '2002-11-24 12:22',
    'pagine_visitate': [1, 2, '3'],
    'prezzo': 17.22
}


class Ordine(BaseModel):
    elemento_id: int
    data_creazione: Optional[datetime.datetime]
    pagine_visitate: List[int] = []
    prezzo: float


o = Ordine(**ordine_json)
print(o)


# Default for JSON post
# Can be done for others with mods.
def ordine_api(ordine: Ordine):
    pass