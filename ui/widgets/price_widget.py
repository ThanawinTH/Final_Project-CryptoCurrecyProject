# ui/widgets/price_widget.py

import customtkinter as ctk
from config.config import (
    BG_CARD,
    TEXT_MAIN,
    TEXT_MUTED,
    GREEN,
    RED,
)


class PriceWidget(ctk.CTkFrame):
    """
    Realtime price widget
    - subscribes to MarketController
    - shows last price
    - shows 24h change (value + percent)
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=18)

        self.controller = controller
        self.controller.add_listener(self)

        # -------------------------
        # UI elements
        # -------------------------
        self.symbol_label = ctk.CTkLabel(
            self,
            text=controller.symbol,
            text_color=TEXT_MUTED,
        )

        self.price_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=TEXT_MAIN,
        )

        self.change_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_MUTED,
        )

        self.symbol_label.pack(anchor="w", padx=16, pady=(14, 2))
        self.price_label.pack(anchor="w", padx=16)
        self.change_label.pack(anchor="w", padx=16, pady=(0, 14))

    # ==================================================
    # Observer callback
    # ==================================================
    def on_market_update(self):
        price = self.controller.last_price
        change_val = self.controller.price_change_24h
        change_pct = self.controller.change_percent_24h

        # ----- Last price -----
        if price is not None:
            self.price_label.configure(
                text=f"{price:,.2f}"
            )

        # ----- 24h change (VALUE + %) -----
        if change_val is not None and change_pct is not None:
            color = GREEN if change_val >= 0 else RED
            sign = "+" if change_val >= 0 else ""

            self.change_label.configure(
                text=f"{sign}{change_val:,.2f} USDT  ({sign}{change_pct:.2f}%)",
                text_color=color
            )
