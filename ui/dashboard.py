import time
import threading
import customtkinter as ctk

from config.config import (
    BG_MAIN,
    BG_PANEL,
    BG_CARD,
    TEXT_MAIN,
    TEXT_MUTED,
    ACCENT,
    WINDOW_SIZE
)

from controllers.market_controller import MarketController

from ui.widgets.price_widget import PriceWidget
from ui.widgets.volume_24h_widget import Volume24hWidget
from ui.widgets.high_low_24h_widget import HighLow24hWidget
from ui.widgets.recent_trade_widget import RecentTradeWidget
from ui.panels.realtime_chart_panel import RealtimeChartPanel
from ui.components.loading_overlay import LoadingOverlay


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configure(fg_color=BG_MAIN)
        self.geometry(WINDOW_SIZE)
        self.title("Crypto Dashboard")

        self.market: MarketController | None = None
        self._loading_start_ts = 0.0

        # layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

        self.after(150, lambda: self._switch_symbol("BTCUSDT"))

    # ==================================================
    # Sidebar
    # ==================================================
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_PANEL, width=210)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_MAIN,
        ).pack(pady=(20, 24))

        for sym in ["BTC", "ETH", "SOL", "BNB", "XRP"]:
            ctk.CTkButton(
                self.sidebar,
                text=f"  {sym}",
                width=170,
                height=44,
                fg_color=BG_CARD,
                hover_color=ACCENT,
                corner_radius=14,
                command=lambda s=sym: self._switch_symbol(f"{s}USDT"),
            ).pack(padx=16, pady=6)

    # ==================================================
    # Main
    # ==================================================
    def _build_main(self):
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=0)  
        self.main.grid_rowconfigure(1, weight=1)   
        self.main.grid_rowconfigure(2, weight=0)  

        self.loading = LoadingOverlay(self.main, text="Loading market...")
        self.loading.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading.hide()


    # ==================================================
    # Switch Symbol
    # ==================================================
    def _switch_symbol(self, symbol: str):
        self._loading_start_ts = time.time()
        self.loading.show()
        self.after(120, lambda: self._load_market(symbol))

    def _load_market(self, symbol: str):
        if self.market:
            self.market.stop()

        for child in self.main.winfo_children():
            if child is not self.loading:
                child.destroy()

        self.market = MarketController(symbol)

        threading.Thread(
            target=self._load_market_bg,
            daemon=True
        ).start()

    def _load_market_bg(self):
        self.market.load_snapshot()
        self.market.start_realtime()
        self.market.start_snapshot_refresh(interval=30)
        self.after(0, self._build_after_load)

    def _build_after_load(self):
        self._build_price_strip(self.main)
        self._build_chart(self.main)
        self._build_bottom_panel(self.main)

        elapsed = time.time() - self._loading_start_ts
        delay = max(0, int((0.35 - elapsed) * 1000))
        self.after(delay, self.loading.hide)

    # ==================================================
    # Price Strip
    # ==================================================
    def _build_price_strip(self, parent):
        strip = ctk.CTkFrame(parent, fg_color="transparent")
        strip.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        strip.grid_columnconfigure((0, 1, 2), weight=1)

        PriceWidget(strip, self.market).grid(row=0, column=0, sticky="ew", padx=8)
        HighLow24hWidget(strip, self.market).grid(row=0, column=1, sticky="ew", padx=8)
        Volume24hWidget(strip, self.market).grid(row=0, column=2, sticky="ew", padx=8)

    # ==================================================
    # Chart
    # ==================================================
    def _build_chart(self, parent):
        chart = ctk.CTkFrame(parent, fg_color=BG_PANEL, corner_radius=22)
        chart.grid(row=1, column=0, sticky="nsew", pady=(0,0))
        chart.grid_columnconfigure(0, weight=1)
        chart.grid_rowconfigure(0, weight=1)

        body = ctk.CTkFrame(chart, fg_color=BG_CARD, corner_radius=16)
        body.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        RealtimeChartPanel(
            body,
            controller=self.market,
            interval="1h",
        ).pack(fill="both", expand=True)

    # ==================================================
    # Bottom Panel (Recent Trades ONLY)
    # ==================================================
    def _build_bottom_panel(self, parent):
        panel = ctk.CTkFrame(
            parent,
            fg_color=BG_PANEL,
            corner_radius=22,
            height=120   
        )
        panel.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        panel.grid_propagate(False)

        panel.grid_columnconfigure(0, weight=1)

        RecentTradeWidget(
            panel,
            controller=self.market,
        ).grid(row=0, column=0, sticky="nsew", padx=20, pady=16)


