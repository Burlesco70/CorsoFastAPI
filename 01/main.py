from typing import Optional

import fastapi
# Per avere un server
import uvicorn

# Flask-style
api = fastapi.FastAPI()

# Flask-style
# E' sempre consigliabile avere una home di dominio API
@api.get('/')
# Per ora senza Jinja
def index():
    body = "<html>" \
           "<body style='padding: 10px;'>" \
           "<h1>Benvenuti su FastAPI</h1>" \
           "<div>" \
           "Try it: <a href='/api/calcola?x=7&y=11'>/api/calcola?x=7&y=11</a>" \
           "</div>" \
           "</body>" \
           "</html>"

    return fastapi.responses.HTMLResponse(content=body)

# Flask-style
# Altro modo di passare i dati
# @api.get('/api/calcola/{x}/{y}')
@api.get('/api/calcola')
# Senza type hints, x, y, z sono considerate stringhe
def calcola(x: int, y: int, z: Optional[int] = None):
    if z == 0:
        # Usando l'oggetto response restituisco anche lo status_code invece di Internal server 
        return fastapi.responses.JSONResponse(
            content={"error": "ERRORE: il terzo parametro opzionale Z non può essere zero."},
            status_code=400)

    value = x + y

    if z is not None:
        value /= z
    # Data structure
    return {
        'x': x,
        'y': y,
        'z': z,
        'value': value
    }

uvicorn.run(api, port=8000, host="127.0.0.1")    