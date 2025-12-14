# crypto_Thanawin

## Crypto Dashboard

A **real-time cryptocurrency dashboard** built with **Python**, **CustomTkinter**, **Matplotlib**, and **Binance API**.  
The application provides live prices, 24h statistics, recent trades, and candlestick charts with a clean, professional UI inspired by trading terminals.

---

## ✨ Features

- 📈 **Real-time price updates** via Binance WebSocket
- ⏱ **24h market snapshot** (price change, high, low, volume)
- 🕯 **Candlestick chart + volume** (historical + live price line)
- 🔄 **Auto-reconnect WebSocket** for stability
- 🎨 **Luxury dark UI theme** using CustomTkinter
- 🧭 **Multi-asset support** (BTC, ETH, SOL, BNB, XRP)

---

## 🗂 Project Structure

```
crypto_Thanawin/
│
├── api/
│   ├── binance_rest.py        # Binance REST API (24h stats, klines)
│   └── binance_websocket.py   # Realtime trade WebSocket client
│
├── config/
│   └── config.py              # App settings & theme colors
│
├── controllers/
│   └── market_controller.py   # Market state & observer controller
│
├── ui/
│   ├── dashboard.py           # Main application window
│   ├── components/
│   │   ├── loading_overlay.py # Loading screen overlay
│   │   └── title_bar.py       # Section title component
│   ├── panels/
│   │   └── realtime_chart_panel.py  # Candlestick + volume chart
│   ├── tabs/
│   │   └── asset_tab.py       # Asset tab layout
│   └── widgets/
│       ├── price_widget.py
│       ├── volume_24h_widget.py
│       ├── high_low_24h_widget.py
│       └── recent_trade_widget.py
│
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
└── README.md
```

---

## 🧠 Architecture Overview

### MarketController (Core Logic)

- Central source of truth for market data
- Fetches **24h snapshot** via REST
- Receives **live trades** via WebSocket
- Uses **Observer pattern** to notify UI components

### REST API (`api/binance_rest.py`)

- `get_24h_ticker(symbol)` → 24h statistics
- `get_klines(symbol, interval, limit)` → historical OHLCV data

### WebSocket (`api/binance_websocket.py`)

- Subscribes to `<symbol>@trade`
- Auto-reconnect & background thread
- Emits parsed trade data (price, qty, side)

---

## 🎨 UI Design

- Built with **CustomTkinter** (modern Tkinter)
- Dark professional theme inspired by trading terminals
- Modular UI components (widgets, panels, overlays)
- Loading overlay for smooth symbol switching

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/crypto_Thanawin.git
cd crypto_Thanawin
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
python app.py
```

---

## 📦 Dependencies

- `customtkinter` – modern UI framework
- `matplotlib` – chart rendering
- `requests` – REST API calls
- `websocket-client` – realtime WebSocket connection
- `pandas` – data handling (future extensibility)

---

## ⚠️ Notes & Limitations

- Uses **Binance public API** (no authentication required)
- Subject to Binance rate limits
- Internet connection required
- Designed for **educational & personal projects**, not live trading

---

## 🔮 Future Improvements

- Add technical indicators (MA, RSI, MACD)
- Order book & depth chart
- Multi-timeframe switching
- Save user preferences
- Paper trading simulation

---

## 📜 License

This project is for **learning and educational purposes**.  
Binance API data belongs to Binance.

---

## 👤 Author

**Thanawin**  
Crypto Dashboard Project

---

Happy coding & happy trading 🚀📊
