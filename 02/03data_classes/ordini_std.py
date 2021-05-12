import datetime
from typing import List

from dateutil.parser import parse

ordine_json = {
    'elemento_id': '123',
    'data_creazione': '2002-11-24 12:22',
    'pagine_visitate': [1, 2, '3'],
    'prezzo': 17.22
}


class Ordine:

    def __init__(self, elemento_id: int, data_creazione: datetime.datetime,
                 pagine_visitate: List[int], prezzo: float):
        self.elemento_id = elemento_id
        self.data_creazione = data_creazione
        self.pagine_visitate = pagine_visitate
        self.prezzo = prezzo

    def __str__(self):
        return str(self.__dict__)

# class Ordine:

#     def __init__(self, elemento_id: int, data_creazione: datetime.datetime, prezzo: float, pagine_visitate=None):
#         if pagine_visitate is None:
#             pagine_visitate = []

#         try:
#             self.elemento_id = int(elemento_id)
#         except ValueError:
#             raise Exception("elemento_id non valido, deve essere un intero.")

#         try:
#             self.data_creazione = parse(data_creazione)
#         except:
#             raise Exception("data_creazione non valida, deve essere datetime.")

#         try:
#             self.prezzo = float(prezzo)
#         except ValueError:
#             raise Exception("prezzo non valido, deve essere float.")

#         try:
#             self.pagine_visitate = [int(p) for p in pagine_visitate]
#         except:
#             raise Exception("pagine_visitate non valida, deve essere iterable con solo interi.")

#     def __str__(self):
#         return f'elemento_id={self.elemento_id}, data_creazione={repr(self.data_creazione)}, ' \
#                f'prezzo={self.prezzo}, pagine_visitate={self.pagine_visitate}'

#     def __eq__(self, other):
#         return isinstance(other, Ordine) and self.__dict__ == other.__dict__

#     def __ne__(self, other):
#         return isinstance(other, Ordine) and self.__dict__ == other.__dict__


o = Ordine(**ordine_json)
print(o)