# app.py
from ui.dashboard import Dashboard
from config.config import APP_TITLE, WINDOW_SIZE


def main():
    app = Dashboard()
    app.title(APP_TITLE)
    app.geometry(WINDOW_SIZE)
    app.mainloop()


if __name__ == "__main__":
    main()
