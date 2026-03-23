# src/notificaciones.py - Gmail SMTP reportes MD
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(report, subject=None):
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASS")

    if not user or not password:
        print("Sin credenciales Gmail, saltando email")
        return

    if not subject:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        subject = f"📊 Skandia Monitor - {fecha} COT"

    msg = MIMEMultipart("alternative")
    msg["From"] = user
    msg["To"] = user
    msg["Subject"] = subject

    parte_texto = MIMEText(report, "plain", "utf-8")
    msg.attach(parte_texto)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(user, user, msg.as_string())
        server.quit()
        print(f"Email enviado a {user}")
    except Exception as e:
        print(f"Error email: {e}")

def formato_reporte(data, alertas, top):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Skandia Monitor Diario",
        f"**Fecha:** {fecha} COT",
        "",
        "## 🚨 Alertas",
    ]
    if alertas:
        for a in alertas:
            lines.append(f"- {a}")
    else:
        lines.append("- Sin alertas activas ✅")

    lines += ["", "## 🏆 Top 5 Fondos (365d)", "| Fondo | Nombre | Rent365 | Sharpe |", "|-------|--------|---------|--------|"]
    from config import FONDOS
    for idp, vals in top:
        nombre = FONDOS.get(idp, {}).get("nombre", idp)
        lines.append(f"| {idp} | {nombre} | {vals.get('rent365', 0):.1f}% | {vals.get('sharpe', 0):.2f} |")

    lines += ["", "---", "Skandia Monitor v3.0 | GitHub Actions"]
    return "\n".join(lines)
