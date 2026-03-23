# src/scraper_series.py - Consulta APIs Skandia
import requests
from config import API_BASE, PERIODS

def get_series(idp, period="P4"):
    try:
        url = f"{API_BASE}/OM.Rentabilidades.PL/Skandia/GetSeries/{idp}/{period}/0"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("Series", [])
    except Exception as e:
        print(f"Error {idp}: {e}")
    return []

def get_all_series(period="P4"):
    from config import FONDOS
    results = {}
    for idp in FONDOS:
        series = get_series(idp, period)
        if series:
            results[idp] = series
            print(f"OK {idp}: {len(series)} puntos")
        else:
            print(f"FAIL {idp}")
    return results

def get_excel():
    try:
        url = f"{API_BASE}/om.rentabilidades.pl/Skandia/GetExcel/0"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            with open("data/fondos.xlsx", "wb") as f:
                f.write(resp.content)
            print("Excel descargado: data/fondos.xlsx")
    except Exception as e:
        print(f"Error Excel: {e}")
