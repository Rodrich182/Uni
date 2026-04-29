import re
import requests
from bs4 import BeautifulSoup

url = "http://www.aemet.es/es/eltiempo/prediccion/municipios/santander-id39075"
headers = {"User-Agent": "Mozilla/5.0"}


session = requests.Session()
session.trust_env = False
html = session.get(url, headers=headers, timeout=15).text
soup = BeautifulSoup(html, "html.parser")

# Visible page text
txt = soup.get_text(" ", strip=True)


m = re.search(
    r"Temperatura\s+m[ií]nima\s+y\s+m[aá]xima\s*\(°?C\)\s*(-?\d+)\s*/\s*(-?\d+)",
    txt,
    flags=re.IGNORECASE,
)

if not m:
    raise ValueError("No se pudo extraer la temperatura maxima de hoy.")

tmax_hoy = int(m.group(2))
print(tmax_hoy)
