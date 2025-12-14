# ui/components/title_bar.py
import customtkinter as ctk

class TitleBar(ctk.CTkFrame):
    def __init__(self, parent, text):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=10, pady=10)
