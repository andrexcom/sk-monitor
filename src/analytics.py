# src/analytics.py - Sharpe, Volatilidad, Alertas
import numpy as np
from config import IBR, ALERTAS_REGLAS

def calc_rent(series):
    if len(series) < 2:
        return 0
    values = [float(s["Value"]) for s in series]
    return (values[-1] / values[0] - 1) * 100

def calc_volatilidad(series):
    if len(series) < 2:
        return 0
    values = np.array([float(s["Value"]) for s in series])
    returns = np.diff(values) / values[:-1]
    return float(np.std(returns) * np.sqrt(252))

def calc_sharpe(series):
    if len(series) < 2:
        return 0
    rent = calc_rent(series) / 100
    vol = calc_volatilidad(series)
    return round((rent - IBR) / vol, 2) if vol > 0 else 0

def calc_vf(vp, rent_ea, dias):
    return vp * (1 + rent_ea) ** (dias / 365)

def calc_tir_real(tir_nominal, ipc):
    from config import IPC
    ipc = ipc or IPC
    return ((1 + tir_nominal) / (1 + ipc)) - 1

def check_alertas(data):
    alertas = []
    for idp, vals in data.items():
        r = vals.get("rent365", 0)
        s = vals.get("sharpe", 0)
        r30 = vals.get("rent30", 0)

        if r30 < ALERTAS_REGLAS["critica_severa_30d"]:
            alertas.append(f"🔴 CRÍTICA {idp}: rent30d={r30:.1f}%")
        elif r30 < ALERTAS_REGLAS["critica_30d"]:
            alertas.append(f"🔴 ALERTA {idp}: rent30d={r30:.1f}%")
        elif s > ALERTAS_REGLAS["oportunidad_sharpe"]:
            alertas.append(f"🟢 OPORTUNIDAD {idp}: Sharpe={s:.2f}")

    return alertas

def top_fondos(data, n=5):
    return sorted(data.items(), key=lambda x: x[1].get("rent365", 0), reverse=True)[:n]
