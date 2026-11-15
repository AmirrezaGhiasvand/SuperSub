"""Separate process keeps the Windows folder dialog off server threads."""
import json
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
try:
    path = filedialog.askdirectory(title='SuperSub — select local Whisper model folder', mustexist=True, parent=root)
    print(json.dumps({'path': path}))
finally:
    root.destroy()
