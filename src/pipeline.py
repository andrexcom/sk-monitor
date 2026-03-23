# src/pipeline.py - Skandia Monitor v3.0 MAIN
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import FONDOS
from scraper_series import get_series
from analytics import calc_rent, calc_volatilidad, calc_sharpe, check_alertas, top_fondos
from db import init_db, save_data, save_metricas, save_alerta
from notificaciones import send_email, formato_reporte

def run_diario():
    print("=== Skandia Monitor Iniciando ===")
    init_db()

    data = {}
    for idp in FONDOS:
        print(f"Fetching {idp}...")
        series_365 = get_series(idp, "P4")
        series_30  = get_series(idp, "P2")

        if series_365:
            rent365 = calc_rent(series_365)
            rent30  = calc_rent(series_30) if series_30 else 0
            sharpe  = calc_sharpe(series_365)
            vol     = calc_volatilidad(series_365)

            data[idp] = {
                "rent365": rent365,
                "rent30":  rent30,
                "sharpe":  sharpe,
                "vol":     vol
            }
            save_data(idp, series_365, "P4")
            save_metricas(idp, rent365, rent30, sharpe, vol)
            print(f"  {idp}: {rent365:.1f}% | Sharpe {sharpe:.2f}")
        else:
            print(f"  {idp}: sin datos")

    alertas = check_alertas(data)
    top = top_fondos(data, n=5)

    for a in alertas:
        save_alerta("", "auto", a)
        print(a)

    reporte = formato_reporte(data, alertas, top)
    print("\n" + reporte)
    send_email(reporte)
    print("=== Completado ===")

def run_mis_fondos(ids):
    init_db()
    for idp in ids:
        series = get_series(idp, "P4")
        if series:
            r = calc_rent(series)
            s = calc_sharpe(series)
            print(f"{idp}: Rent365={r:.1f}% | Sharpe={s:.2f}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "diario"
    if mode == "diario":
        run_diario()
    elif mode == "mis_fondos":
        ids = sys.argv[2:] if len(sys.argv) > 2 else list(FONDOS.keys())
        run_mis_fondos(ids)
    else:
        print(f"Modo desconocido: {mode}")
        print("Uso: python pipeline.py diario|mis_fondos [idp1 idp2...]")
