# api/binance_websocket.py

import json
import threading
import time
import websocket


class BinanceWebSocket:
    """
    Production-grade Binance WebSocket client

    - Stream: <symbol>@trade
    - Emits : price only (realtime)
    - Features:
        * auto reconnect
        * background thread
        * safe close
    """

    def __init__(self, symbol: str, on_trade):
        self.symbol = symbol.lower()
        self.on_trade = on_trade

        self._ws = None
        self._thread = None
        self._running = False

        self._reconnect_delay = 3  # seconds

    # ==================================================
    # Public API
    # ==================================================
    def start(self):
        """
        Start websocket connection (non-blocking)
        """
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )
        self._thread.start()

    def stop(self):
        """
        Stop websocket connection gracefully
        """
        self._running = False
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None

    # ==================================================
    # Internal loop
    # ==================================================
    def _run(self):
        """
        Reconnect loop
        """
        while self._running:
            try:
                self._connect()
            except Exception as e:
                print(f"[WS] Fatal error: {e}")

            if self._running:
                print(f"[WS] Reconnecting in {self._reconnect_delay}s...")
                time.sleep(self._reconnect_delay)

    def _connect(self):
        url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"

        self._ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

        # ping_interval สำคัญมากสำหรับ connection ยาว ๆ
        self._ws.run_forever(
            ping_interval=20,
            ping_timeout=10
        )

    # ==================================================
    # WebSocket callbacks
    # ==================================================
    def _on_open(self, ws):
        print(f"[WS] Connected: {self.symbol}")

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)

            trade = {
                "price": float(data["p"]),
                "qty": float(data["q"]),
                "side": "sell" if data["m"] else "buy",
                "ts": time.time(),
            }

            if callable(self.on_trade):
                self.on_trade(trade)

        except Exception as e:
            print(f"[WS] Parse error: {e}")

    def _on_error(self, ws, error):
        if self._running:
            print(f"[WS] Error: {error}")

    def _on_close(self, ws, *args):
        if self._running:
            print(f"[WS] Connection closed")
