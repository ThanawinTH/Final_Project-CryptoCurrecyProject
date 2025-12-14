# ui/tabs/asset_tab.py
import customtkinter as ctk
from ui.widgets.price_widget import PriceWidget
from ui.widgets.volume_24h_widget import Volume24hWidget
from ui.widgets.recent_trade_widget import RecentTradeWidget
from ui.panels.realtime_chart_panel import RealtimeChartPanel

class AssetTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        RealtimeChartPanel(self).grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10)
        PriceWidget(self, controller).grid(row=0, column=1, sticky="n", pady=10)
        Volume24hWidget(self, controller).grid(row=1, column=1, sticky="n")
        RecentTradeWidget(self, controller).grid(row=2, column=1, sticky="nsew")
