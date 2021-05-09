import datetime

import requests
import bs4
from colorama import Fore


def get_html(num_episodio: int) -> str:
    print(Fore.YELLOW + f"Getting HTML dell'episodio {num_episodio}", flush=True)

    url = f'https://talkpython.fm/{num_episodio}'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text


def get_titolo(html: str, num_episodio: int) -> str:
    print(Fore.CYAN + f"Getting TITOLO dell'episodio {num_episodio}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


def main():
    t0 = datetime.datetime.now()
    get_range_titoli()
    dt = datetime.datetime.now() - t0
    print(f"Eseguito in {dt.total_seconds():.2f} sec.")


def get_range_titoli():
    # Mantenere range piccolo per eviatare DDoS del sito
    for n in range(270, 280):
        html = get_html(n)
        title = get_titolo(html, n)
        print(Fore.WHITE + f"Titolo trovato: {title}", flush=True)


if __name__ == '__main__':
    main()