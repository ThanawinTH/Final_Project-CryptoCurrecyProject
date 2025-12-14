import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from datetime import datetime

from api.binance_rest import get_klines


# ===== Light theme colors =====
BG_AX = "#ffffff"
GRID = "#e6e6e6"
TEXT = "#333333"
BULL = "#16a34a"
BEAR = "#dc2626"
PRICE_LINE = "#2563eb"


class RealtimeChartPanel(ctk.CTkFrame):
    """
    Candlestick + Volume chart (LIGHT THEME)

    - Price : Volume = 3 : 1
    - X-axis shown ONLY on volume
    - Realtime last price tick (no redraw)
    """

    def __init__(self, parent, controller, interval="1h", limit=24):
        super().__init__(parent, fg_color="transparent")

        # =========================
        # Controller (realtime)
        # =========================
        self.controller = controller
        self.controller.add_listener(self)

        self.symbol = controller.symbol
        self.interval = interval
        self.limit = limit

        # =========================
        # Data buffers
        # =========================
        self.timestamps = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []

        # =========================
        # Header (title above chart)
        # =========================
        self.header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.header.pack(fill="x", padx=6, pady=(4, 2))

        self.title_label = ctk.CTkLabel(
            self.header,
            text=f"{self.symbol} · 24H Chart ( TF : {self.interval} )",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
        )
        self.title_label.pack(anchor="w")

        # =========================
        # Figure + GridSpec (3:1)
        # =========================
        self.fig = Figure(figsize=(7, 4), dpi=95, facecolor=BG_AX)
        gs = GridSpec(
            4,
            1,
            height_ratios=[3, 0.02, 1, 0.02],
            hspace=0.0,
        )

        self.ax_price = self.fig.add_subplot(gs[0])
        self.ax_volume = self.fig.add_subplot(gs[2], sharex=self.ax_price)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # draw
        self._load_history()
        self._draw_chart()

    # ==================================================
    # Data
    # ==================================================
    def _load_history(self):
        klines = get_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=self.limit,
        )

        self.timestamps.clear()
        self.opens.clear()
        self.highs.clear()
        self.lows.clear()
        self.closes.clear()
        self.volumes.clear()

        for k in klines:
            self.timestamps.append(datetime.fromtimestamp(k[0] / 1000))
            self.opens.append(float(k[1]))
            self.highs.append(float(k[2]))
            self.lows.append(float(k[3]))
            self.closes.append(float(k[4]))
            self.volumes.append(float(k[5]))  # base asset volume

    # ==================================================
    # Styling
    # ==================================================
    def _style_axes(self):
        for ax in (self.ax_price, self.ax_volume):
            ax.set_facecolor(BG_AX)
            ax.grid(True, color=GRID, linewidth=0.8)
            ax.tick_params(colors=TEXT, labelsize=10)
            for spine in ax.spines.values():
                spine.set_visible(False)

        # ----- PRICE AXIS -----
        self.ax_price.yaxis.tick_left()
        # self.ax_price.tick_params(labelleft=False)
        self.ax_price.set_ylabel("")

        self.ax_price.tick_params(
            axis="x",
            which="both",
            bottom=False,
            labelbottom=False,
        )

        # ----- VOLUME AXIS -----
        self.ax_volume.set_ylabel("Volume", fontsize=10, color=TEXT)
        self.ax_volume.xaxis.set_major_formatter(
            mdates.DateFormatter("%m-%d %H:%M")
        )

    # ==================================================
    # Initial draw
    # ==================================================
    def _draw_chart(self):
        # safety guard
        if not self.closes:
            return

        self.ax_price.clear()
        self.ax_volume.clear()
        self._style_axes()

        dates = mdates.date2num(self.timestamps)
        candle_width = (dates[1] - dates[0]) * 0.7

        for i, date in enumerate(dates):
            o = self.opens[i]
            h = self.highs[i]
            l = self.lows[i]
            c = self.closes[i]
            v = self.volumes[i]

            color = BULL if c >= o else BEAR

            # Wick
            self.ax_price.plot(
                [date, date],
                [l, h],
                color=color,
                linewidth=1.2,
            )

            # Body
            self.ax_price.add_patch(
                Rectangle(
                    (date - candle_width / 2, min(o, c)),
                    candle_width,
                    abs(c - o),
                    facecolor=color,
                    edgecolor=color,
                )
            )

            # Volume
            self.ax_volume.bar(
                date,
                v,
                width=candle_width,
                color=color,
                alpha=0.9,
            )

        # =========================
        # Last price (initial)
        # =========================
        last_price = self.closes[-1]

        self.last_price_line = self.ax_price.axhline(
            last_price,
            color=PRICE_LINE,
            linestyle="--",
            linewidth=1.4,
            alpha=0.9,
        )

        self.last_price_label = self.ax_price.text(
            1.005,
            last_price,
            f"{last_price:,.2f}",
            transform=self.ax_price.get_yaxis_transform(),
            color="white",
            fontsize=11,
            fontweight="bold",
            va="center",
            ha="left",
            bbox=dict(
                facecolor=PRICE_LINE,
                edgecolor=PRICE_LINE,
                boxstyle="round,pad=0.25",
            ),
        )

        self.ax_price.set_xlim(
            dates[0] - candle_width,
            dates[-1] + candle_width,
        )

        self.fig.subplots_adjust(
            left=0.06,
            right=0.94,
            top=0.96,
            bottom=0.10,
        )

        self.canvas.draw_idle()

    # ==================================================
    # Realtime update (NO redraw)
    # ==================================================
    def on_market_update(self):
        price = self.controller.last_price
        if price is None:
            return

        self.last_price_line.set_ydata([price, price])
        self.last_price_label.set_y(price)
        self.last_price_label.set_text(f"{price:,.2f}")

        self.canvas.draw_idle()
