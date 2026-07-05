import os
import sys

# Ensure TCL/TK libraries can be found on Windows if paths are missing
tcl_path = r"C:\Users\hussa\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
tk_path = r"C:\Users\hussa\AppData\Local\Programs\Python\Python313\tcl\tk8.6"
if os.path.exists(tcl_path):
    os.environ['TCL_LIBRARY'] = tcl_path
if os.path.exists(tk_path):
    os.environ['TK_LIBRARY'] = tk_path

import tkinter as tk
from tkinter import font as tkfont
import math
import random
import time

class HelloKittyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hello Kitty Calculator ✨")
        self.root.geometry("480x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#FFE4E1")

        # Calculator state
        self.expression = ""
        self.result_str = "0"
        self.prev_expression = ""
        self.new_input = True

        # Animation states
        self.particles = []
        self.buttons = {}
        self.pressed_button = None
        self.blink_counter = 0
        self.is_blinking = False
        self.bow_angle = 0
        self.bow_target_angle = 0

        # Colors
        self.BG_COLOR = "#FFF0F5"         # LavenderBlush
        self.BODY_COLOR = "#FF6B8B"       # Hello Kitty Pink Body
        self.BODY_SHADOW = "#D84364"      # Darker pink shadow
        self.FACE_COLOR = "#FFFFFF"       # White kitty face
        self.BOW_COLOR = "#FF2A55"        # Iconic Red/Pink Bow
        self.BOW_SHADOW = "#C71535"
        self.LCD_BG = "#F3F8F2"           # Soft pastel LCD green/gray
        self.LCD_FRAME = "#4A1525"        # Dark berry LCD bezel
        
        # Create Canvas
        self.canvas = tk.Canvas(root, width=480, height=720, bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Initialize particles
        self.init_particles()

        # Build UI layout
        self.draw_calculator_body()
        self.setup_buttons()
        self.draw_lcd()

        # Event Binds
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.root.bind("<Key>", self.on_key_press)

        # Start animation loop
        self.animate()

    def init_particles(self):
        symbols = ['♥', '★', '🎀', '🌸', '✨', '🍒', '🍎']
        colors = ['#FF85A2', '#FFB7C5', '#FF4D6D', '#FFC0CB', '#FF69B4']
        for _ in range(25):
            self.particles.append({
                'x': random.randint(10, 470),
                'y': random.randint(10, 710),
                'size': random.randint(12, 22),
                'symbol': random.choice(symbols),
                'color': random.choice(colors),
                'speed_y': random.uniform(0.4, 1.2),
                'swing_speed': random.uniform(0.02, 0.05),
                'swing_amount': random.uniform(0.5, 1.5),
                'phase': random.uniform(0, 6.28),
                'id': None
            })

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_calculator_body(self):
        # Draw floating background decorative particles first
        for p in self.particles:
            p['id'] = self.canvas.create_text(
                p['x'], p['y'], text=p['symbol'], 
                font=("Arial", p['size']), fill=p['color']
            )

        # Main Calculator Outer Body (3D Shadow)
        self.draw_rounded_rect(35, 125, 445, 695, radius=40, fill=self.BODY_SHADOW, outline="")
        # Main Body Front
        self.body_id = self.draw_rounded_rect(30, 120, 440, 685, radius=40, fill=self.BODY_COLOR, outline="#FFFFFF", width=3)

        # Hello Kitty Head Top Section
        # Kitty Ear Left
        self.canvas.create_polygon(80, 130, 60, 50, 140, 90, smooth=True, fill="#FFFFFF", outline=self.BODY_SHADOW, width=3)
        # Kitty Ear Right
        self.canvas.create_polygon(400, 130, 420, 50, 340, 90, smooth=True, fill="#FFFFFF", outline=self.BODY_SHADOW, width=3)
        # Kitty Head Main Oval
        self.canvas.create_oval(70, 40, 410, 190, fill="#FFFFFF", outline="#4A1525", width=4)

        # Kitty Eyes (Animated)
        self.left_eye = self.canvas.create_oval(160, 110, 176, 132, fill="#222222", outline="")
        self.right_eye = self.canvas.create_oval(304, 110, 320, 132, fill="#222222", outline="")
        # Eye Highlights
        self.left_eye_hl = self.canvas.create_oval(163, 113, 168, 118, fill="#FFFFFF", outline="")
        self.right_eye_hl = self.canvas.create_oval(307, 113, 312, 118, fill="#FFFFFF", outline="")

        # Kitty Nose
        self.canvas.create_oval(232, 125, 248, 137, fill="#FFD700", outline="#4A1525", width=2)

        # Kitty Whiskers (Left)
        self.canvas.create_line(90, 105, 140, 113, width=3, fill="#222222", capstyle="round")
        self.canvas.create_line(85, 122, 138, 124, width=3, fill="#222222", capstyle="round")
        self.canvas.create_line(92, 139, 142, 133, width=3, fill="#222222", capstyle="round")

        # Kitty Whiskers (Right)
        self.canvas.create_line(390, 105, 340, 113, width=3, fill="#222222", capstyle="round")
        self.canvas.create_line(395, 122, 342, 124, width=3, fill="#222222", capstyle="round")
        self.canvas.create_line(388, 139, 338, 133, width=3, fill="#222222", capstyle="round")

        # Red Hello Kitty Bow (Top Right Ear)
        self.draw_bow(330, 65)

        # Bottom "Hello Kitty" Logo Text
        self.canvas.create_text(235, 660, text="Hello Kitty ♡", font=("Comic Sans MS", 22, "bold"), fill="#FFFFFF")
        self.canvas.create_text(235, 659, text="Hello Kitty ♡", font=("Comic Sans MS", 22, "bold"), fill="#FF2A55")

    def draw_bow(self, cx, cy):
        # Draw iconic red bow on ear with knot and lobes
        self.bow_group = []
        # Left lobe
        l_lobe = self.canvas.create_oval(cx-45, cy-25, cx-5, cy+25, fill=self.BOW_COLOR, outline="#4A1525", width=3)
        l_fold = self.canvas.create_arc(cx-40, cy-15, cx-15, cy+15, start=30, extent=120, style="arc", outline="#FFFFFF", width=2)
        # Right lobe
        r_lobe = self.canvas.create_oval(cx+5, cy-25, cx+45, cy+25, fill=self.BOW_COLOR, outline="#4A1525", width=3)
        r_fold = self.canvas.create_arc(cx+15, cy-15, cx+40, cy+15, start=210, extent=120, style="arc", outline="#FFFFFF", width=2)
        # Center Knot
        knot_bg = self.canvas.create_oval(cx-16, cy-16, cx+16, cy+16, fill=self.BOW_SHADOW, outline="")
        knot = self.canvas.create_oval(cx-14, cy-14, cx+14, cy+14, fill=self.BOW_COLOR, outline="#4A1525", width=3)
        knot_hl = self.canvas.create_oval(cx-8, cy-10, cx-2, cy-4, fill="#FFFFFF", outline="")
        
        self.bow_items = [l_lobe, l_fold, r_lobe, r_fold, knot_bg, knot, knot_hl]

    def draw_lcd(self):
        # 3D LCD Outer Bezel
        self.draw_rounded_rect(65, 175, 405, 265, radius=20, fill=self.LCD_FRAME, outline="#FFB7C5", width=2)
        # Inner Screen Surface
        self.draw_rounded_rect(72, 182, 398, 258, radius=15, fill=self.LCD_BG, outline="#A3C9A8", width=2)

        # Upper Expression Text
        self.lcd_expr_id = self.canvas.create_text(
            385, 198, text="", font=("Consolas", 13), fill="#666666", anchor="e"
        )
        # Main Big LCD Result Text
        self.lcd_text_id = self.canvas.create_text(
            385, 232, text="0", font=("Consolas", 26, "bold"), fill="#222222", anchor="e"
        )
        # Small cute Kitty Icon in LCD corner
        self.canvas.create_text(88, 198, text="🐱", font=("Arial", 14))

    def setup_buttons(self):
        button_layout = [
            [("AC", "action"), ("⌫", "action"), ("%", "op"), ("÷", "op")],
            [("7", "num"),    ("8", "num"),    ("9", "num"), ("×", "op")],
            [("4", "num"),    ("5", "num"),    ("6", "num"), ("-", "op")],
            [("1", "num"),    ("2", "num"),    ("3", "num"), ("+", "op")],
            [("0", "num"),    (".", "num"),    ("♡", "cute"),("=", "equals")]
        ]

        start_x = 72
        start_y = 285
        btn_w = 72
        btn_h = 62
        gap_x = 14
        gap_y = 12

        for r, row in enumerate(button_layout):
            for c, (label, btn_type) in enumerate(row):
                x1 = start_x + c * (btn_w + gap_x)
                y1 = start_y + r * (btn_h + gap_y)
                x2 = x1 + btn_w
                y2 = y1 + btn_h

                self.create_3d_button(label, btn_type, x1, y1, x2, y2)

    def create_3d_button(self, label, btn_type, x1, y1, x2, y2):
        if btn_type == "num":
            bg_color = "#FFFFFF"
            shadow_color = "#E0C0C8"
            text_color = "#FF4D6D"
            shape = "kitty_head"
        elif btn_type == "op":
            bg_color = "#82B3F4"
            shadow_color = "#5A93D8"
            text_color = "#FFFFFF"
            shape = "pill"
        elif btn_type == "action":
            bg_color = "#FF7597"
            shadow_color = "#D84A6F"
            text_color = "#FFFFFF"
            shape = "rounded"
        elif btn_type == "cute":
            bg_color = "#FFB7C5"
            shadow_color = "#E08B9D"
            text_color = "#FF2A55"
            shape = "heart"
        elif btn_type == "equals":
            bg_color = "#FF2A55"
            shadow_color = "#C71535"
            text_color = "#FFFFFF"
            shape = "pill"

        btn_data = {
            'label': label,
            'type': btn_type,
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'bg': bg_color, 'shadow': shadow_color, 'text_color': text_color,
            'shape': shape,
            'pressed': False,
            'hover': False,
            'shadow_id': None, 'body_id': None, 'text_id': None, 'decor_ids': []
        }

        self.render_button_graphics(btn_data)
        self.buttons[label] = btn_data

    def render_button_graphics(self, b):
        if b['shadow_id']: self.canvas.delete(b['shadow_id'])
        if b['body_id']: self.canvas.delete(b['body_id'])
        if b['text_id']: self.canvas.delete(b['text_id'])
        for d_id in b['decor_ids']: self.canvas.delete(d_id)
        b['decor_ids'] = []

        offset = 0 if b['pressed'] else 5
        x1, y1, x2, y2 = b['x1'], b['y1'], b['x2'], b['y2']
        
        current_bg = b['bg']
        if b['hover'] and not b['pressed']:
            current_bg = self.lighten_color(b['bg'], 1.15)

        if b['shape'] == "kitty_head":
            b['shadow_id'] = self.draw_rounded_rect(x1, y1+5, x2, y2+5, radius=18, fill=b['shadow'], outline="")
            b['body_id'] = self.draw_rounded_rect(x1, y1+5-offset, x2, y2+5-offset, radius=18, fill=current_bg, outline="#FFB7C5", width=2)
            
            e1 = self.canvas.create_polygon(x1+8, y1+7-offset, x1+18, y1+1-offset, x1+24, y1+10-offset, smooth=True, fill=current_bg, outline="#FFB7C5")
            e2 = self.canvas.create_polygon(x2-8, y1+7-offset, x2-18, y1+1-offset, x2-24, y1+10-offset, smooth=True, fill=current_bg, outline="#FFB7C5")
            bow_dot = self.canvas.create_oval(x2-16, y1+5-offset, x2-10, y1+11-offset, fill="#FF2A55", outline="")
            b['decor_ids'].extend([e1, e2, bow_dot])

        elif b['shape'] == "heart":
            b['shadow_id'] = self.draw_rounded_rect(x1, y1+5, x2, y2+5, radius=20, fill=b['shadow'], outline="")
            b['body_id'] = self.draw_rounded_rect(x1, y1+5-offset, x2, y2+5-offset, radius=20, fill=current_bg, outline="#FFFFFF", width=2)

        else:
            radius = 22 if b['shape'] == "pill" else 16
            b['shadow_id'] = self.draw_rounded_rect(x1, y1+5, x2, y2+5, radius=radius, fill=b['shadow'], outline="")
            b['body_id'] = self.draw_rounded_rect(x1, y1+5-offset, x2, y2+5-offset, radius=radius, fill=current_bg, outline="#FFFFFF", width=2)

        ty = (y1 + y2) / 2 + (5 - offset)
        font_style = ("Comic Sans MS", 18, "bold") if b['type'] != "num" else ("Arial", 20, "bold")
        b['text_id'] = self.canvas.create_text((x1+x2)/2, ty, text=b['label'], font=font_style, fill=b['text_color'])

    def lighten_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        for label, b in self.buttons.items():
            is_inside = (b['x1'] <= x <= b['x2']) and (b['y1'] <= y <= b['y2'])
            if is_inside != b['hover']:
                b['hover'] = is_inside
                self.render_button_graphics(b)
                if is_inside:
                    self.canvas.config(cursor="hand2")
                else:
                    self.canvas.config(cursor="")

    def on_mouse_click(self, event):
        x, y = event.x, event.y
        for label, b in self.buttons.items():
            if (b['x1'] <= x <= b['x2']) and (b['y1'] <= y <= b['y2']):
                b['pressed'] = True
                self.pressed_button = b
                self.render_button_graphics(b)
                self.handle_button_press(label)
                break

    def on_mouse_release(self, event):
        if self.pressed_button:
            self.pressed_button['pressed'] = False
            self.render_button_graphics(self.pressed_button)
            self.pressed_button = None

    def on_key_press(self, event):
        key = event.char
        keysym = event.keysym

        mapping = {
            'Return': '=', 'equal': '=',
            'BackSpace': '⌫',
            'Escape': 'AC',
            'asterisk': '×', 'x': '×', 'X': '×',
            'slash': '÷',
            'plus': '+', 'minus': '-'
        }

        btn_key = mapping.get(keysym, key)
        if btn_key in self.buttons:
            b = self.buttons[btn_key]
            b['pressed'] = True
            self.render_button_graphics(b)
            self.handle_button_press(btn_key)
            self.root.after(150, lambda: self.release_key(b))

    def release_key(self, b):
        b['pressed'] = False
        self.render_button_graphics(b)

    def handle_button_press(self, label):
        self.bow_target_angle = 15

        if label == "AC":
            self.expression = ""
            self.result_str = "0"
            self.prev_expression = ""
            self.new_input = True
        elif label == "⌫":
            if len(self.expression) > 0:
                self.expression = self.expression[:-1]
                self.result_str = self.expression if self.expression else "0"
        elif label == "♡":
            cute_quotes = ["Love You! ♡", "Kawaii! ✨", "Kitty Hug! 🐱", "Super Cute! 🎀", "Purrfect! 🐾"]
            self.result_str = random.choice(cute_quotes)
            self.new_input = True
        elif label == "=":
            self.calculate_result()
        elif label in ["+", "-", "×", "÷", "%"]:
            if self.new_input and self.result_str != "0" and not self.expression:
                self.expression = self.result_str
            self.expression += label
            self.result_str = self.expression
            self.new_input = False
        else:
            if self.new_input:
                self.expression = label if label != "." else "0."
                self.new_input = False
            else:
                self.expression += label
            self.result_str = self.expression

        self.update_lcd()

    def calculate_result(self):
        if not self.expression:
            return

        try:
            eval_exp = self.expression.replace("×", "*").replace("÷", "/")
            eval_exp = eval_exp.replace("%", "/100")
            result = eval(eval_exp)
            
            if isinstance(result, float):
                if result.is_integer():
                    result_formatted = str(int(result))
                else:
                    result_formatted = f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                result_formatted = str(result)

            self.prev_expression = self.expression + " ="
            self.result_str = result_formatted
            self.expression = ""
            self.new_input = True
        except Exception:
            self.prev_expression = self.expression
            self.result_str = "Error ♡"
            self.expression = ""
            self.new_input = True

    def update_lcd(self):
        self.canvas.itemconfig(self.lcd_expr_id, text=self.prev_expression)
        
        display_text = self.result_str
        if len(display_text) > 14:
            font_size = max(14, 26 - (len(display_text) - 14))
        else:
            font_size = 26
        
        self.canvas.itemconfig(self.lcd_text_id, text=display_text, font=("Consolas", font_size, "bold"))

    def animate(self):
        for p in self.particles:
            p['y'] -= p['speed_y']
            p['phase'] += p['swing_speed']
            swing_x = p['x'] + math.sin(p['phase']) * p['swing_amount']
            
            if p['y'] < -20:
                p['y'] = 730
                p['x'] = random.randint(10, 470)

            self.canvas.coords(p['id'], swing_x, p['y'])

        self.blink_counter += 1
        if self.blink_counter > 140:
            self.is_blinking = True
            self.canvas.itemconfig(self.left_eye, state="hidden")
            self.canvas.itemconfig(self.right_eye, state="hidden")
            self.canvas.itemconfig(self.left_eye_hl, state="hidden")
            self.canvas.itemconfig(self.right_eye_hl, state="hidden")
            if self.blink_counter > 148:
                self.blink_counter = 0
                self.is_blinking = False
                self.canvas.itemconfig(self.left_eye, state="normal")
                self.canvas.itemconfig(self.right_eye, state="normal")
                self.canvas.itemconfig(self.left_eye_hl, state="normal")
                self.canvas.itemconfig(self.right_eye_hl, state="normal")

        if self.bow_target_angle != 0:
            self.bow_target_angle *= -0.85
            if abs(self.bow_target_angle) < 0.5:
                self.bow_target_angle = 0

        self.root.after(33, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloKittyCalculator(root)
    root.mainloop()
