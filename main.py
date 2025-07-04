import tkinter as tk
from PIL import Image, ImageTk
import os, random

# --- Configuration ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TOP_BUN_PATH = os.path.join("image", "top_buns.png")
BOTTOM_BUN_PATH = os.path.join("image", "bottom_buns.png")
FRAME_DELAY = 16  # ~60 FPS

class BouncingBurgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Burger Bounce")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        self.load_and_combine_images()

        self.x = 200
        self.y = 200
        self.dx = 5
        self.dy = 4
        self.paused = False
        self.name_text = "loenora romero"
        self.name_font = ("Arial", 16, "bold")

        self.draw_burger()
        self.create_pause_overlay()

        self.root.bind("<space>", self.toggle_pause)
        self.animate()

    def load_and_combine_images(self):
        def trim_transparent(img):
            bbox = img.getbbox()
            return img.crop(bbox) if bbox else img

        top = Image.open(TOP_BUN_PATH).convert("RGBA")
        bottom = Image.open(BOTTOM_BUN_PATH).convert("RGBA")
        top = trim_transparent(top)
        bottom = trim_transparent(bottom)

        self.gap_top = 10
        self.gap_bottom = 10
        self.text_height = 25

        self.burger_width = max(top.width, bottom.width)
        self.top_height = top.height
        self.bottom_height = bottom.height
        total_height = (
            self.top_height +
            self.gap_top +
            self.text_height +
            self.gap_bottom +
            self.bottom_height
        )
        self.burger_height = total_height

        self.burger_img_pil = Image.new("RGBA", (self.burger_width, total_height), (0, 0, 0, 0))

        top_x = (self.burger_width - top.width) // 2
        bottom_x = (self.burger_width - bottom.width) // 2
        self.burger_img_pil.paste(top, (top_x, 0), top)
        bottom_y = self.top_height + self.gap_top + self.text_height + self.gap_bottom
        self.burger_img_pil.paste(bottom, (bottom_x, bottom_y), bottom)

        self.burger_img_tk = ImageTk.PhotoImage(self.burger_img_pil)

        self.text_offset_y = (
            -self.burger_height // 2 +
            self.top_height +
            self.gap_top +
            self.text_height // 2
        )

    def draw_burger(self):
        self.image_item = self.canvas.create_image(
            self.x, self.y, image=self.burger_img_tk
        )

        self.name_item = self.canvas.create_text(
            self.x,
            self.y + self.text_offset_y,
            text=self.name_text,
            fill="black",
            font=self.name_font
        )

    def create_pause_overlay(self):
        # Overlay rectangle (hidden initially)
        self.pause_overlay = self.canvas.create_rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            fill='black', stipple='gray50', state='hidden'
        )

        self.pause_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            text="PAUSED",
            fill="white",
            font=("Arial", 48, "bold"),
            state='hidden'
        )

    def show_pause_overlay(self):
        self.canvas.itemconfig(self.pause_overlay, state='normal')
        self.canvas.itemconfig(self.pause_text, state='normal')

    def hide_pause_overlay(self):
        self.canvas.itemconfig(self.pause_overlay, state='hidden')
        self.canvas.itemconfig(self.pause_text, state='hidden')

    def random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

    def is_bright(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness > 128

    def toggle_pause(self, event=None):
        self.paused = not self.paused
        if self.paused:
            self.show_pause_overlay()
        else:
            self.hide_pause_overlay()

    def animate(self):
        if not self.paused:
            self.move_burger()
        self.root.after(FRAME_DELAY, self.animate)

    def move_burger(self):
        self.x += self.dx
        self.y += self.dy
        hit_edge = False

        if self.x <= self.burger_width // 2:
            self.x = self.burger_width // 2
            self.dx *= -1
            hit_edge = True
        elif self.x >= WINDOW_WIDTH - self.burger_width // 2:
            self.x = WINDOW_WIDTH - self.burger_width // 2
            self.dx *= -1
            hit_edge = True

        if self.y <= self.burger_height // 2:
            self.y = self.burger_height // 2
            self.dy *= -1
            hit_edge = True
        elif self.y >= WINDOW_HEIGHT - self.burger_height // 2:
            self.y = WINDOW_HEIGHT - self.burger_height // 2
            self.dy *= -1
            hit_edge = True

        if hit_edge:
            bg_color = self.random_color()
            text_color = "black" if self.is_bright(bg_color) else "white"
            self.canvas.config(bg=bg_color)
            self.canvas.itemconfig(self.name_item, fill=text_color)

        self.canvas.coords(self.image_item, self.x, self.y)
        self.canvas.coords(self.name_item, self.x, self.y + self.text_offset_y)

# --- Run the app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBurgerApp(root)
    root.mainloop()