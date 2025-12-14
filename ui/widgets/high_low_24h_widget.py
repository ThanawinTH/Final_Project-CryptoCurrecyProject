# ui/widgets/high_low_24h_widget.py

import customtkinter as ctk
from config.config import (
    BG_CARD,
    TEXT_MAIN,
    TEXT_MUTED,
)


class HighLow24hWidget(ctk.CTkFrame):
    """
    24h High / Low widget
    - subscribes to MarketController
    - shows high & low prices
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=18)

        self.controller = controller
        self.controller.add_listener(self)

        # ---- UI ----
        self.title_label = ctk.CTkLabel(
            self,
            text="24h High / Low",
            text_color=TEXT_MUTED,
        )

        self.high_label = ctk.CTkLabel(
            self,
            text="High: --",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_MAIN,
        )

        self.low_label = ctk.CTkLabel(
            self,
            text="Low: --",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_MAIN,
        )

        self.title_label.pack(anchor="w", padx=16, pady=(14, 6))
        self.high_label.pack(anchor="w", padx=16)
        self.low_label.pack(anchor="w", padx=16, pady=(0, 14))

    # ==================================================
    # Observer callback
    # ==================================================
    def on_market_update(self):
        high = self.controller.high_24h
        low = self.controller.low_24h

        if high is not None:
            self.high_label.configure(
                text=f"High: {high:,.2f}"
            )

        if low is not None:
            self.low_label.configure(
                text=f"Low: {low:,.2f}"
            )
