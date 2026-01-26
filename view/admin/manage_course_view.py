import tkinter as tk
from config.app_config import APP_TITLE, APP_WIDTH, APP_HEIGHT, BG_COLOR

root = tk.Tk()
root.title(APP_TITLE)
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.configure(bg=BG_COLOR)

root.mainloop()

