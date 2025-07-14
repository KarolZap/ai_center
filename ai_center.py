from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
import logging
import json
import os

# === KONFIGURACJA EMAIL (z ENV Variables na Renderze) ===
EMAIL = os.environ.get("EMAIL")
EMAIL_HASLO = os.environ.get("EMAIL_HASLO")
EMAIL_ODB = os.environ.get("EMAIL_ODB")

# === GODZINY HANDLU ===
GODZINY_OD = 6
GODZINY_DO = 23

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

# === ENDPOINT GET – żeby strona działała normalnie ===
@app.route("/", methods=["GET"])
def index():
    return "✅ AI Center działa!", 200

# === ENDPOINT POST – główny webhook od TradingView ===
@app.route("/", methods=["POST"])
def webhook():
    teraz = datetime.now(timezone.utc)
    godzina = teraz.hour

    if godzina < GODZINY_OD or godzina >= GODZINY_DO:
        print(f"⏰ Poza godzinami handlu ({GODZINY_OD}-{GODZINY_DO})")
        logging.info(f"{teraz} - Poza godzinami handlu")
        return "Poza godzinami handlu", 200

    dane = request.get_json()
    if not dane:
        return "Brak danych JSON", 400
print("EMAIL:", EMAIL)
print("EMAIL_HASLO:", EMAIL_HASLO)
print("EMAIL_ODB:", EMAIL_ODB)

    signal = dane.get("signal")
