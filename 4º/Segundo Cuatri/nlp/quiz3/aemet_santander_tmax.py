import re
import requests
from bs4 import BeautifulSoup

URL = "http://www.aemet.es/es/eltiempo/prediccion/municipios/santander-id39075"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_today_top_temperature() -> int:
    session = requests.Session()
    # Evita proxies rotos definidos en variables de entorno
    session.trust_env = False

    response = session.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Captura la pareja min/max tras el literal de AEMET
    match = re.search(
        r"Temperatura\s+m[ií]nima\s+y\s+m[aá]xima\s*\(°?C\)\s*(-?\d+)\s*/\s*(-?\d+)",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        raise ValueError("No se pudo extraer la temperatura maxima de hoy")

    tmax_today = int(match.group(2))
    return tmax_today


if __name__ == "__main__":
    print(get_today_top_temperature())
