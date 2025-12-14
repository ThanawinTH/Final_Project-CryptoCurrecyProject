import customtkinter as ctk
from datetime import datetime
from config.config import BG_CARD, TEXT_MAIN, TEXT_MUTED, GREEN, RED


class RecentTradeWidget(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=18)

        self.controller = controller
        controller.add_listener(self)

        # ---------- title ----------
        ctk.CTkLabel(
            self,
            text="Recent Trade",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_MAIN
        ).pack(anchor="w", padx=18, pady=(14, 8))

        # ---------- main row ----------
        self.row = ctk.CTkFrame(self, fg_color="transparent")
        self.row.pack(fill="x", padx=18, pady=(0, 16))

        # BUY / SELL
        self.side = ctk.CTkLabel(
            self.row,
            width=64,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.side.pack(side="left")

        # PRICE (hero)
        self.price = ctk.CTkLabel(
            self.row,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.price.pack(side="left", padx=(10, 14))

        # Qty (secondary)
        self.qty = ctk.CTkLabel(
            self.row,
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED
        )
        self.qty.pack(side="left")

        # Time (right aligned)
        self.time = ctk.CTkLabel(
            self.row,
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        self.time.pack(side="right")

    # ==================================================
    # Realtime update
    # ==================================================
    def on_market_update(self):
        trade = getattr(self.controller, "last_trade", None)
        if not trade:
            return

        color = GREEN if trade["side"] == "buy" else RED

        self.side.configure(
            text=trade["side"].upper(),
            text_color=color
        )

        self.price.configure(
            text=f"{trade['price']:,.2f}",
            text_color=color
        )

        self.qty.configure(
            text=f"Qty {trade['qty']:.4f}"
        )

        ts = datetime.fromtimestamp(trade["ts"]).strftime("%H:%M:%S")
        self.time.configure(text=ts)
