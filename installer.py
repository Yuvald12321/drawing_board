from tkinter import filedialog, messagebox
from ctypes import windll
from pathlib import Path
import shutil
windll.shcore.SetProcessDpiAwareness(1)
if messagebox.askyesno("installer", "do you want to install\ndrawing board.exe?"):
    try:
        src = Path(__file__).parent / "drawing board.exe"
        dest = filedialog.askdirectory(initialdir=(Path.home() / "desktop"))
        shutil.copy(src, dest)
        messagebox.showinfo("success", "downloading complete")
    except Exception as e:
        messagebox.showerror("Error", str(e))