import customtkinter as ctk
from config.config import BG_MAIN, BG_CARD, TEXT_MAIN, TEXT_MUTED


class LoadingOverlay(ctk.CTkFrame):
    def __init__(self, parent, text="Loading"):
        super().__init__(parent, fg_color=BG_MAIN)

        self.base_text = text
        self._dots = 0
        self._running = False

        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        box = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=18)
        box.place(relx=0.5, rely=0.5, anchor="center")

        self.bar = ctk.CTkProgressBar(box, mode="indeterminate", width=160)
        self.bar.pack(padx=30, pady=(24, 10))

        self.label = ctk.CTkLabel(
            box, text=text, font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_MAIN
        )
        self.label.pack()

        self.sub = ctk.CTkLabel(
            box, text="Fetching market data",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        self.sub.pack(pady=(4, 20))

        self.hide()

    def show(self):
        self._running = True
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()
        self.bar.start()
        self._animate_text()

    def hide(self):
        self._running = False
        self.bar.stop()
        self.place_forget()

    def _animate_text(self):
        if not self._running:
            return
        self._dots = (self._dots + 1) % 4
        self.label.configure(text=self.base_text + "." * self._dots)
        self.after(350, self._animate_text)
