# src/config.py 
# Fuente: portal.skandia.com.co

API_BASE = "https://portal.skandia.com.co"
IBR = 0.08
IPC = 0.05
PERIODS = {"P1": "1d", "P2": "30d", "P3": "180d", "P4": "365d"}

FONDOS = {
    "OMBCLM": {"nombre": "FPV Acciones BCLM", "perfil": "Agresivo"},
    "SKACP": {"nombre": "FCP Crédito Impulso", "perfil": "Agresivo"},
    "SKDEC2": {"nombre": "FIC Deuda Emergente", "perfil": "Agresivo"},
    "OMACTE": {"nombre": "FPV Acciones Tecnología", "perfil": "Agresivo"},
    "SKDAPC": {"nombre": "FIC Comprar Arrendar", "perfil": "Moderado"},
    "SKAUSA": {"nombre": "FIC S&P 500", "perfil": "Agresivo"},
    "SKAVAC": {"nombre": "FIC Acciones Colombia", "perfil": "Moderado"},
    "SKEXTP": {"nombre": "Portafolio Extra Plazo", "perfil": "Moderado"},
    "SKACOP": {"nombre": "FIC Corporativo Plus", "perfil": "Moderado"},
    "ICTR12": {"nombre": "FIC Efectivo IBR 12M", "perfil": "Conservador"},
    "SKERFL": {"nombre": "FPV Bonos Colombia Plus", "perfil": "Conservador"},
    "SKAFIJ": {"nombre": "FIC Renta Fija", "perfil": "Conservador"},
    "SKALIQ": {"nombre": "FIC Liquidez Plus", "perfil": "Conservador"},
    "SKACDP": {"nombre": "FIC CDT Colombia", "perfil": "Conservador"},
    "SKABIT": {"nombre": "FIC Bitcoin", "perfil": "Agresivo"},
    "OMREIT": {"nombre": "FIC Real Estate Global", "perfil": "Moderado"},
    "SKAGLO": {"nombre": "FIC Global Diversificado", "perfil": "Agresivo"},
    "SKAEUR": {"nombre": "FIC Estructurado Europa", "perfil": "Agresivo"},
    "OMPP_MOD": {"nombre": "PV Perfil Moderado", "perfil": "Pensiones"},
    "OMPP_AGR": {"nombre": "PV Perfil Agresivo", "perfil": "Pensiones"},
}

ALERTAS_REGLAS = {
    "critica_30d": -1.5,
    "critica_severa_30d": -4.0,
    "oportunidad_sharpe": 2.0,
    "concentracion_max": 0.60,
    "btc_caida_critica": -0.15,
    "btc_caida_moderada": -0.08,
    "sp500_caida": -0.04,
}

COOLDOWNS_HORAS = {
    "critica": 6,
    "moderada": 24,
    "oportunidad": 48,
}

BUFFETT_APRUEBA = ["ICTR12", "SKERFL", "SKAUSA", "SKAFIJ"]
BUFFETT_CAUTELA = ["OMBCLM", "SKACP"]
BUFFETT_CUESTIONA = ["SKABIT"]
