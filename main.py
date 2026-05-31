import sys
import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog, messagebox
from ctypes import windll
from PIL import Image, ImageDraw, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
TkClass = TkinterDnD.Tk


class DrawingApp(TkClass):
    def __init__(self):
        super().__init__()
        self.title("Drawing Board")
        self.resizable(False, False)
        self.line_width = 5
        self.current_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.current_tool = "pen"
        self.last_x = None
        self.last_y = None
        self.WIDTH, self.HEIGHT = 400, 400

        self.image = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.bg_color)
        self.draw_context = ImageDraw.Draw(self.image)

        self.display_label = tk.Label(self)
        self.display_label.pack()

        self.display_label.bind("<Button-1>", self.start_drawing)
        self.display_label.bind("<B1-Motion>", self.draw)

        self.setup_menu()
        self.update_display()
        self.set_tool("pen")

        if hasattr(self, 'drop_target_register'):
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.handle_drop)

        if len(sys.argv) > 1:
            self.load_image(sys.argv[1])

    def setup_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset", command=self.reset_board)
        file_menu.add_command(label="Resize", command=self.resize_board)
        file_menu.add_separator()
        file_menu.add_command(label="Import", command=self.import_image)
        file_menu.add_command(label="Export", command=self.export_image)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        for tool in ["pen", "paint_bucket", "color_picker", "eraser"]:
            label_name = tool.replace("_", " ").title()
            tools_menu.add_command(label=label_name, command=lambda t=tool: self.set_tool(t))

        menu_bar.add_command(label="Color", command=self.set_color)

    def update_display(self):
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.display_label.config(image=self.photo_image)

    def load_image(self, path):
        try:
            if path.startswith('{') and path.endswith('}'):
                path = path[1:-1]
            img = Image.open(path).convert("RGB")
            self.image = img
            self.draw_context = ImageDraw.Draw(self.image)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def handle_drop(self, event):
        self.load_image(event.data)

    def import_image(self):
        path = filedialog.askopenfilename(
            defaultextension=".png",
            filetypes=[
                ("Image File", "*.png"),
                ("Image File", "*.jpg"),
                ("Image File", "*.jpeg"),
                ("Image File", "*.webp"),
                ("Image File", "*.bmp"),
                ("All Files", "*.*")
            ]
        )
        if path:
            self.load_image(path)

    def export_image(self):
        path = filedialog.asksaveasfilename(
            initialfile=simpledialog.askstring("Export", "Enter name", initialvalue="drawing"),
            defaultextension=".png",
            filetypes=[
                ("Image File", "*.png"),
                ("Image File", "*.jpg"),
                ("Image File", "*.jpeg"),
                ("Image File", "*.webp"),
                ("Image File", "*.bmp"),
                ("All Files", "*.*")
            ]
        )
        if path:
            try:
                self.image.save(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def start_drawing(self, event):
        if self.current_tool == "paint_bucket":
            self.flood_fill(event.x, event.y)
        elif self.current_tool == "color_picker":
            self.pick_color(event.x, event.y)
        else:
            self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.current_tool in ("pen", "eraser") and self.last_x is not None:
            color = self.bg_color if self.current_tool == "eraser" else self.current_color
            width = self.line_width * 3 if self.current_tool == "eraser" else self.line_width
            self.draw_context.line(
                [(self.last_x, self.last_y), (event.x, event.y)],
                joint="round", fill=color, width=width
            )
            self.update_display()
            self.last_x, self.last_y = event.x, event.y

    def pick_color(self, x, y):
        try:
            rgb = self.image.getpixel((x, y))
            self.current_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
            self.set_tool("pen")
        except IndexError:
            pass

    def flood_fill(self, x, y):
        fill_rgb = tuple(int(self.current_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        try:
            if self.image.getpixel((x, y)) != fill_rgb:
                ImageDraw.floodfill(self.image, (x, y), fill_rgb, thresh=0)
                self.update_display()
        except IndexError:
            pass

    def set_color(self):
        color = colorchooser.askcolor(self.current_color)[1]
        if color:
            self.current_color = color

    def set_tool(self, tool_name):
        self.current_tool = tool_name
        cursors = {
            "pen": "pencil",
            "paint_bucket": "crosshair",
            "eraser": "dotbox",
            "color_picker": "tcross"
        }
        self.config(cursor=cursors.get(tool_name, "arrow"))

    def resize_board(self):
        new_width = simpledialog.askinteger("Resize", "Enter new width:", initialvalue=400)
        if new_width:
            ratio = new_width / self.image.width
            new_height = int(self.image.height * ratio)
            self.image = self.image.resize((new_width, new_height))
            self.WIDTH, self.HEIGHT = new_width, new_height
            self.draw_context = ImageDraw.Draw(self.image)
            self.update_display()

    def reset_board(self):
        self.image = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.bg_color)
        self.draw_context = ImageDraw.Draw(self.image)
        self.update_display()


if __name__ == "__main__":
    windll.shcore.SetProcessDpiAwareness(1)
    app = DrawingApp()
    app.mainloop()