from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
import logging
import json
import os

# === KONFIGURACJA EMAIL (z REPLIT SECRETS) ===
EMAIL = os.environ.get("EMAIL")
EMAIL_HASLO = os.environ.get("EMAIL_HASLO")
EMAIL_ODB = os.environ.get("EMAIL_ODB")

# === GODZINY HANDLU ===
GODZINY_OD = 9
GODZINY_DO = 19

# === PRZYGOTUJ FOLDER Z LOGAMI ===
os.makedirs("logs", exist_ok=True)

# === KONFIGURACJA SERWERA ===
app = Flask(__name__)
logging.basicConfig(filename="logs/signals.log", level=logging.INFO)

# === FUNKCJA WYSYŁANIA EMAILA ===
def wyslij_maila(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL_ODB

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, EMAIL_HASLO)
            smtp.send_message(msg)
        print(f"✅ Email wysłany: {subject}")
        logging.info(f"{datetime.now()} - Email: {subject}")
    except Exception as e:
        print("❌ Błąd maila:", e)
        logging.error(f"{datetime.now()} - Błąd: {e}")

# === GŁÓWNY ENDPOINT ===
@app.route("/", methods=["POST"])
def webhook():
    teraz = datetime.utcnow()
    godzina = teraz.hour

    if godzina < GODZINY_OD or godzina >= GODZINY_DO:
        print(f"⏰ Poza godzinami handlu ({GODZINY_OD}-{GODZINY_DO})")
        logging.info(f"{teraz} - Poza godzinami handlu")
        return "Poza godzinami handlu", 200

    dane = request.get_json()
    if not dane:
        return "Brak danych JSON", 400

    signal = dane.get("signal", "").upper()
    if signal not in ["BUY", "SELL"]:
        return f"Nieznany sygnał: {signal}", 400

    # Przygotuj treść emaila z dodatkowymi informacjami
    tresc = f"""
📈 Otrzymano sygnał: {signal}

📌 Coin: {dane.get('coin', 'Nieznany')}
💬 Notka: {dane.get('note', 'Brak notki')}
🎯 Ticker: {dane.get('ticker', 'Brak tikera')}

Pełne dane:
{json.dumps(dane, indent=2)}
""".strip()

    temat = f"🔔 AI Sygnał: {signal} ({dane.get('coin', 'Krypto')})"

    wyslij_maila(temat, tresc)
    return f"OK – Odebrano sygnał: {signal}", 200

# === START ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
