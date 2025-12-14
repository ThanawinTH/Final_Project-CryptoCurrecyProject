import threading
import time
from collections import deque

from api.binance_rest import get_24h_ticker
from api.binance_websocket import BinanceWebSocket


class MarketController:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()

        # ---- market state ----
        self.last_price = None
        self.price_change_24h = None
        self.change_percent_24h = None
        self.high_24h = None
        self.low_24h = None
        self.volume_24h = None

        # ---- recent trades ----
        self.recent_trades = deque(maxlen=20)

        # ---- observers ----
        self._listeners = []

        # ---- lifecycle ----
        self._stopped = False
        self._snapshot_running = False

        # ---- websocket ----
        self._ws = BinanceWebSocket(
            symbol=self.symbol,
            on_trade=self._on_trade
        )

    # ==================================================
    # Observer
    # ==================================================
    def add_listener(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def _notify(self):
        if self._stopped:
            return

        alive = []
        for l in self._listeners:
            try:
                if hasattr(l, "winfo_exists") and not l.winfo_exists():
                    continue
                if hasattr(l, "on_market_update"):
                    l.on_market_update()
                alive.append(l)
            except Exception:
                continue

        self._listeners = alive

    # ==================================================
    # Snapshot
    # ==================================================
    def load_snapshot(self):
        if self._stopped:
            return

        data = get_24h_ticker(self.symbol)
        self.last_price = float(data["lastPrice"])
        self.price_change_24h = float(data["priceChange"])
        self.change_percent_24h = float(data["priceChangePercent"])
        self.high_24h = float(data["highPrice"])
        self.low_24h = float(data["lowPrice"])
        self.volume_24h = float(data["quoteVolume"])
        self._notify()

    def start_snapshot_refresh(self, interval=30):
        if self._snapshot_running or self._stopped:
            return

        self._snapshot_running = True

        def loop():
            while self._snapshot_running and not self._stopped:
                self.load_snapshot()
                time.sleep(interval)

        threading.Thread(target=loop, daemon=True).start()

    # ==================================================
    # WebSocket
    # ==================================================
    def start_realtime(self):
        if not self._stopped:
            self._ws.start()

    def _on_trade(self, trade):
        """
        Called by websocket on every trade
        """
        if self._stopped:
            return

        self.last_price = trade["price"]

        self.last_trade = {
            "price": trade["price"],
            "qty": trade["qty"],
            "side": trade["side"],
            "ts": time.time(),
        }

        self._notify()



    # ==================================================
    # Stop
    # ==================================================
    def stop(self):
        if self._stopped:
            return

        self._stopped = True
        self._snapshot_running = False

        try:
            self._ws.stop()
        except Exception:
            pass

        self._listeners.clear()
