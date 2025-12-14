# ui/widgets/volume_24h_widget.py

import customtkinter as ctk
from config.config import (
    BG_CARD,
    TEXT_MAIN,
    TEXT_MUTED,
)


def format_volume(value: float) -> str:
    """
    Format volume nicely: K / M / B
    """
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f} K"
    else:
        return f"{value:.2f}"


class Volume24hWidget(ctk.CTkFrame):
    """
    24h Volume widget
    - subscribes to MarketController
    - shows quoteVolume (USDT)
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=18)

        self.controller = controller
        self.controller.add_listener(self)

        self.title_label = ctk.CTkLabel(
            self,
            text="Volume",
            text_color=TEXT_MUTED,
        )

        self.value_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_MAIN,
        )

        self.unit_label = ctk.CTkLabel(
            self,
            text="USDT (24h)",
            text_color=TEXT_MUTED,
        )

        self.title_label.pack(anchor="w", padx=16, pady=(14, 2))
        self.value_label.pack(anchor="w", padx=16)
        self.unit_label.pack(anchor="w", padx=16, pady=(0, 14))

    # ==================================================
    # Observer callback
    # ==================================================
    def on_market_update(self):
        volume = self.controller.volume_24h

        if volume is not None:
            self.value_label.configure(
                text=format_volume(volume)
            )
