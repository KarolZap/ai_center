# 🧠 AI Center – Crypto Commander

Automatyczny system do odbierania sygnałów BUY/SELL z TradingView i wysyłania ich mailem.  
Dostosowany do BTC/USD, ETH/USD i SOL/USD.

## 🔧 Jak działa?

- Odbiera alerty z TradingView przez webhook (Flask)
- Filtruje godziny handlu (9:00–19:00)
- Wysyła e-mail ze szczegółami sygnału
- Każdy alert logowany do pliku `logs/signals.log`

## 🚀 Uruchomienie lokalne

1. Zainstaluj biblioteki:
   ```
   pip install -r requirements.txt
   ```

2. Uruchom serwer:
   ```
   python ai_center.py
   ```

3. Ustaw webhook w TradingView do `http://localhost:3000/`

## 📬 Alert JSON w TradingView

```json
{
  "signal": "BUY"
}
```

## 📁 Struktura projektu

```
AI_Center/
│
├── ai_center.py        # Główny plik aplikacji
├── requirements.txt    # Lista bibliotek
├── README.md           # Opis projektu
└── logs/               # Pliki logów
```
