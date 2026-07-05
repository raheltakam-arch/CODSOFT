import os
import sys

# Fix Tcl/Tk loading issues on this Windows environment
tcl_dir = r"C:\Users\hussa\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
tk_dir = r"C:\Users\hussa\AppData\Local\Programs\Python\Python313\tcl\tk8.6"
if os.path.exists(tcl_dir):
    os.environ['TCL_LIBRARY'] = tcl_dir
if os.path.exists(tk_dir):
    os.environ['TK_LIBRARY'] = tk_dir

import tkinter as tk
import tkinter.font as tkfont
import random
import threading
import time

# Try to import winsound for retro audio effects on Windows
try:
    import winsound
except ImportError:
    winsound = None

# =====================================================================
# PIXEL ART DATASETS (12-bit / 8-bit color matrices)
# Legend:
# '.' = Transparent
# 'k' = Black outline (#000000)
# 's' = Skin tone (#f5b582)
# 'd' = Dark skin shadow (#d48a55)
# 'w' = White highlight (#ffffff)
# 'g' = Green checkmark (#2ecc71)
# 'r' = Red cross/accent (#e74c3c)
# 'y' = Yellow trophy (#f1c40f)
# 'o' = Orange trophy shading (#d68910)
# =====================================================================

# 1. 16x16 Selection Button Icons (Vertical hands pointing up)
ICON_ROCK = [
    "....kkkkkkkk....",
    "...kssssssssk...",
    "..kssssssssssk..",
    "..ksdksdksdkssk..",
    "..ksdksdksdkssk..",
    "..ksdksdksdkssk..",
    "..kssssssssssk..",
    "...kssssssssk...",
    "...ksdssssdssk..",
    "...ksdssssdssk..",
    "...kssssssssk...",
    "....kssssssk....",
    "....kssssssk....",
    "....kssssssk....",
    "....kssssssk....",
    ".....kkkkkk....."
]

ICON_PAPER = [
    "...kk..kk..kk...",
    "..ksk.ksk.ksk...",
    "..ksk.ksk.ksk...",
    "..ksk.ksk.ksk.kk",
    ".kssssssssssksk",
    "ksddddddddddssk",
    "ksdssssssssdssk",
    "ksdssssssssdssk",
    ".ksdssssssdssk.",
    "..ksdssssdssk..",
    "...ksddddssk...",
    "....kssssssk....",
    "....kssssssk....",
    "....kssssssk....",
    "....kssssssk....",
    ".....kkkkkk....."
]

ICON_SCISSORS = [
    "..kk....kk......",
    ".ksk...ksk......",
    ".ksk...ksk......",
    ".ksk...ksk......",
    ".ksk...ksk..kk..",
    ".ksskkkksskksk..",
    "ksssssssssssksk.",
    "ksddddddddddssk.",
    "ksdssssssssdssk.",
    ".ksdssssssdssk..",
    "..ksddddddssk...",
    "...kssssssk.....",
    "....kssssk......",
    "....kssssk......",
    "....kssssk......",
    "....kkkkkk......"
]

# 2. 24x24 Battle Screen Hands (Angled up-right for player; flipped for computer)
BATTLE_ROCK = [
    "........................",
    "............kkkkkk......",
    "..........kksssssskk....",
    "........kksssssssssskk..",
    "......kkssssssssssssssk.",
    ".....kssssddssddssddsssk",
    "....kssssdssdssdssdssssk",
    "....ksssddssddssddsssssk",
    "....ksssssssssssssssssk.",
    ".....ksssssssssssssssk..",
    "......kkssssssssssssk...",
    "........kksssssssskk....",
    "..........kksssskk......",
    "............kkkk........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................"
]

BATTLE_PAPER = [
    "..................kkkk..",
    "............kkkk.kssskk.",
    "......kkkk.kssskkssskssk",
    ".....kssskksssksssksssk.",
    ".....ksssksssksssksssk..",
    "......ksksssksssksssk...",
    "......kskssskssskssk....",
    ".......kssssssssssk.....",
    "......kssddddddddsk.....",
    ".....kssddsssssssk......",
    "....kssddsssssssk.......",
    "....ksdssssssssk........",
    "....kddsssssssk.........",
    ".....ksssssssk..........",
    "......kkkkkkk...........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................"
]

BATTLE_SCISSORS = [
    "............kkkk..kkkk..",
    "...........ksssk.ksssk..",
    "...........ksssk.ksssk..",
    "...........ksssk.ksssk..",
    "..........kssskk.ksssk..",
    ".........kssskk.ksssk...",
    "........kssskk.ksssk....",
    ".......ksssskkssssk.....",
    "......ksssssssssssk.....",
    ".....kssddddddddssk.....",
    "....kssddssssssssk......",
    "....ksdsssssssssk.......",
    "....kddssssssssk........",
    ".....kssssssssk.........",
    "......kkkkkkkk..........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................"
]

# 3. Score Indicators & Victory Icons
CHECKMARK_MATRIX = [
    "............gg",
    "...........ggg",
    "..........gggg",
    ".........gggg.",
    "..gg....gggg..",
    ".ggg...gggg...",
    "gggg..gggg....",
    ".gggggggg.....",
    "..gggggg......",
    "...gggg.......",
    "....gg........",
    ".............."
]

CROSS_MATRIX = [
    "rr........rr",
    "rrr......rrr",
    ".rrr....rrr.",
    "..rrr..rrr..",
    "...rrrrrr...",
    "....rrrr....",
    "....rrrr....",
    "...rrrrrr...",
    "..rrr..rrr..",
    ".rrr....rrr.",
    "rrr......rrr",
    "rr........rr"
]

EMPTY_BOX_MATRIX = [
    "kkkkkkkkkkkk",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "k..........k",
    "kkkkkkkkkkkk"
]

TROPHY_MATRIX = [
    "........................",
    "......yyyyyyyyyyyy......",
    ".....yyyyyyyyyyyyyy.....",
    "....ykkkkkkkkkkkkkky....",
    "...ykyyyyyyyyyyyyyyky...",
    "..ykyyyyyyyyyyyyyyyyky..",
    "..ykyyyykkkkkkkkyyyyky..",
    "..ykyyykoyyyyyyokyyyky..",
    "..ykyyykoyyyyyyokyyyky..",
    "...ykyykoyyyyyyokyyky...",
    "....ykkkoyyyyyyokkky....",
    ".....yyykoyyyyyokyy.....",
    "......yyykoyyyokyy......",
    ".......yyykkkkyyy.......",
    "........yyyyyyyy........",
    ".........yyyyyy.........",
    "..........yyyy..........",
    ".........yyyyyy.........",
    ".......yyyyyyyyyy.......",
    ".....yyyyyyyyyyyyyy.....",
    "....ykkkkkkkkkkkkkky....",
    "....ykkkkkkkkkkkkkky....",
    ".....yyyyyyyyyyyyyy.....",
    "........................"
]

SKULL_MATRIX = [
    "........................",
    "........kkkkkkkk........",
    "......kkrrrrrrrrkk......",
    "....kkrrrrrrrrrrrrkk....",
    "...krrrrrrrrrrrrrrrrk...",
    "..krrrrrrrrrrrrrrrrrrk..",
    "..krrkkkkrrrrrrkkkkrrk..",
    "..krkkwwkkkrrkkkwwkkrk..",
    "..krkkwwkkkrrkkkwwkkrk..",
    "..krrrkkkkrrrrrrkkkkrrk..",
    "..krrrrrrrrrrrrrrrrrrk..",
    "...krrrrrrrrrrrrrrrrk...",
    "....krrrrrkkkkrrrrrk....",
    ".....krrrkkkkkkrrrk.....",
    "......kkrkrkrkrkrk......",
    "........kkkkkkkk........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................"
]

# Audio Player (Non-blocking using thread)
def play_sound(sound_type):
    if winsound is None:
        return
    def _play():
        try:
            if sound_type == "shake":
                winsound.Beep(400, 70)
            elif sound_type == "tie":
                winsound.Beep(520, 80)
                winsound.Beep(520, 80)
            elif sound_type == "win_round":
                winsound.Beep(587, 80)
                winsound.Beep(659, 80)
                winsound.Beep(880, 150)
            elif sound_type == "lose_round":
                winsound.Beep(349, 100)
                winsound.Beep(294, 150)
            elif sound_type == "match_victory":
                # Upbeat victory fanfare
                for f in [523, 659, 784, 659, 784, 1047]:
                    winsound.Beep(f, 90)
            elif sound_type == "match_defeat":
                # Downbeat funeral march
                for f in [392, 349, 311, 262]:
                    winsound.Beep(f, 180)
            elif sound_type == "click":
                winsound.Beep(600, 50)
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()

# Horizontal mirroring for computer's hand
def mirror_matrix(matrix):
    return [row[::-1] for row in matrix]

# Color mapping table
COLOR_MAP = {
    '.': None,             # Transparent
    'k': "#000000",        # Outline
    's': "#f5b582",        # Skin tone
    'd': "#d48a55",        # Skin shadow
    'w': "#ffffff",        # White highlight
    'g': "#2ecc71",        # Green
    'r': "#e74c3c",        # Red
    'y': "#f1c40f",        # Yellow
    'o': "#d68910",        # Orange shadow
}

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ROCK PAPER SCISSORS - PIXEL BATTLE")
        self.root.geometry("600x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        # Fonts configuration
        self.pixel_font_large = tkfont.Font(family="Fixedsys", size=28, weight="bold")
        self.pixel_font_mid = tkfont.Font(family="Fixedsys", size=18, weight="bold")
        self.pixel_font_small = tkfont.Font(family="Fixedsys", size=10, weight="bold")

        # If Fixedsys is not found, fallback to Consolas
        if "Fixedsys" not in tkfont.families():
            self.pixel_font_large.config(family="Consolas")
            self.pixel_font_mid.config(family="Consolas")
            self.pixel_font_small.config(family="Consolas")

        # Game State Variables
        self.player_score = 0
        self.computer_score = 0
        self.state = "choose" # "choose", "shake", "reveal", "game_over"
        self.player_choice = None
        self.computer_choice = None
        self.shake_frame = 0
        self.result_text = ""
        self.result_color = "#ffffff"
        self.hover_btn = -1  # Index of button hovered: 0=Rock, 1=Paper, 2=Scissors, -1=None
        self.hover_play_again = False

        # Canvas for full-screen pixel layout
        self.canvas = tk.Canvas(root, width=600, height=450, bg="#111827", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Mouse event binds for Custom Buttons
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        # Precompute mirrored computer battle hands
        self.comp_battle_hands = {
            "rock": mirror_matrix(BATTLE_ROCK),
            "paper": mirror_matrix(BATTLE_PAPER),
            "scissors": mirror_matrix(BATTLE_SCISSORS)
        }

        # Initialize View
        self.redraw()

    # Redraw loop
    def redraw(self):
        self.canvas.delete("all")
        W = 600
        H = 450

        # 1. State: GAME OVER SCREEN
        if self.state == "game_over":
            self.draw_game_over(W, H)
            return

        # 2. Main Game Screen Split Background
        # Left polygon (Player Blue)
        self.canvas.create_polygon(0, 0, W * 0.55, 0, W * 0.45, H, 0, H, fill="#4a548c", outline="")
        # Right polygon (Computer Red/Crimson)
        self.canvas.create_polygon(W * 0.55, 0, W, 0, W, H, W * 0.45, H, fill="#8c4a5c", outline="")

        # Draw grid textured pattern
        grid_size = 40
        tile_w = 6
        for x in range(0, W, grid_size):
            for y in range(0, H, grid_size):
                x_split = W * 0.55 - (W * 0.10) * (y / H)
                if x < x_split:
                    # Player side tile
                    self.canvas.create_rectangle(x, y, x + tile_w, y + tile_w, fill="#3e4675", outline="")
                else:
                    # Computer side tile
                    self.canvas.create_rectangle(x, y, x + tile_w, y + tile_w, fill="#753e4c", outline="")

        # 3. Headers & Scores
        # "You" Header
        self.draw_text_with_shadow(80, 30, "YOU", self.pixel_font_mid, "#ffffff")
        # "Computer" Header
        self.draw_text_with_shadow(520, 30, "COMPUTER", self.pixel_font_mid, "#ffffff")

        # Score Boxes (3 boxes for each side)
        for i in range(3):
            # Player score indicator
            px = 50 + i * 30
            py = 50
            if i < self.player_score:
                self.draw_pixel_art(CHECKMARK_MATRIX, px, py, scale=2)
            else:
                self.draw_pixel_art(EMPTY_BOX_MATRIX, px, py, scale=2)

            # Computer score indicator
            cx = 490 + i * 30
            cy = 50
            if i < self.computer_score:
                self.draw_pixel_art(CROSS_MATRIX, cx, cy, scale=2)
            else:
                self.draw_pixel_art(EMPTY_BOX_MATRIX, cx, cy, scale=2)

        # 4. Draw Battle Hands
        self.draw_battle_hands(W, H)

        # 5. Draw Game UI Panels based on State
        if self.state == "choose":
            self.draw_selection_banner(W, H)
        elif self.state == "shake":
            # Show animated beat title in center
            beat_text = "ROCK..."
            if self.shake_frame >= 4 and self.shake_frame < 8:
                beat_text = "PAPER..."
            elif self.shake_frame >= 8 and self.shake_frame < 12:
                beat_text = "SCISSORS..."
            elif self.shake_frame >= 12:
                beat_text = "SHOOT!"
            self.draw_text_with_shadow(300, 110, beat_text, self.pixel_font_large, "#f1c40f")
        elif self.state == "reveal":
            # Display match winner text
            self.draw_text_with_shadow(300, 110, self.result_text, self.pixel_font_large, self.result_color)

    # Drawing pixel matrices on Canvas
    def draw_pixel_art(self, matrix, start_x, start_y, scale=4):
        for r_idx, row in enumerate(matrix):
            for c_idx, char in enumerate(row):
                color = COLOR_MAP.get(char)
                if color is not None:
                    x1 = start_x + c_idx * scale
                    y1 = start_y + r_idx * scale
                    x2 = x1 + scale
                    y2 = y1 + scale
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    # Draw double text layered to create drop shadow effect
    def draw_text_with_shadow(self, x, y, text, font, fill, shadow_color="#000000"):
        self.canvas.create_text(x + 2, y + 2, text=text, font=font, fill=shadow_color, anchor="center")
        self.canvas.create_text(x, y, text=text, font=font, fill=fill, anchor="center")

    # Render dynamic arms and hands
    def draw_battle_hands(self, W, H):
        scale = 5  # 24x24 matrix -> 120x120 pixels

        # Standard resting offsets
        player_offset_x = 0
        player_offset_y = 0
        comp_offset_x = 0
        comp_offset_y = 0

        # Shake Offset Calculation
        if self.state == "shake":
            # Multi-frame bobs along the diagonal 45-degree axis
            frame_cycle = self.shake_frame % 4
            bob_offset = 0
            if frame_cycle == 1:
                bob_offset = 20
            elif frame_cycle == 3:
                bob_offset = -10
            
            # Player hand moves along direction (1, -1)
            player_offset_x = bob_offset
            player_offset_y = -bob_offset
            # Computer hand moves along direction (-1, -1)
            comp_offset_x = -bob_offset
            comp_offset_y = -bob_offset

        # Player Coordinates
        player_x = 80 + player_offset_x
        player_y = 200 + player_offset_y

        # Computer Coordinates
        comp_x = 400 + comp_offset_x
        comp_y = 200 + comp_offset_y

        # Define Wrist attachment points for player's arm
        pw_x1 = player_x + 4 * scale
        pw_y1 = player_y + 16 * scale
        pw_x2 = player_x + 12 * scale
        pw_y2 = player_y + 22 * scale

        # Draw Player arm (flesh colored polygon extending from bottom-left corner to wrist)
        self.canvas.create_polygon(0, H, 0, H - 100, pw_x1, pw_y1, pw_x2, pw_y2, 100, H, fill="#f5b582", outline="")
        self.canvas.create_line(0, H - 100, pw_x1, pw_y1, fill="#000000", width=scale)
        self.canvas.create_line(100, H, pw_x2, pw_y2, fill="#000000", width=scale)

        # Draw Player Hand Matrix
        if self.state == "choose" or self.state == "shake":
            self.draw_pixel_art(BATTLE_ROCK, player_x, player_y, scale)
        else:
            # Reveal actual choice
            hand_matrix = BATTLE_ROCK
            if self.player_choice == "paper":
                hand_matrix = BATTLE_PAPER
            elif self.player_choice == "scissors":
                hand_matrix = BATTLE_SCISSORS
            self.draw_pixel_art(hand_matrix, player_x, player_y, scale)

        # Define Wrist attachment points for computer's arm
        cw_x1 = comp_x + 20 * scale
        cw_y1 = comp_y + 16 * scale
        cw_x2 = comp_x + 12 * scale
        cw_y2 = comp_y + 22 * scale

        # Draw Computer arm (flesh colored polygon extending from bottom-right corner to wrist)
        self.canvas.create_polygon(W, H, W, H - 100, cw_x1, cw_y1, cw_x2, cw_y2, W - 100, H, fill="#f5b582", outline="")
        self.canvas.create_line(W, H - 100, cw_x1, cw_y1, fill="#000000", width=scale)
        self.canvas.create_line(W - 100, H, cw_x2, cw_y2, fill="#000000", width=scale)

        # Draw Computer Hand Matrix (Mirrored)
        if self.state == "choose" or self.state == "shake":
            # Computer always shows fist in shake state
            fist_mirrored = mirror_matrix(BATTLE_ROCK)
            self.draw_pixel_art(fist_mirrored, comp_x, comp_y, scale)
        else:
            # Reveal computer's choice
            self.draw_pixel_art(self.comp_battle_hands[self.computer_choice], comp_x, comp_y, scale)

    # Selection board overlay
    def draw_selection_banner(self, W, H):
        # Dark panel banner spanning bottom width
        self.canvas.create_rectangle(0, 270, W, 420, fill="#1c1917", outline="#ffffff", width=2)

        # Select title
        self.draw_text_with_shadow(W // 2, 295, "SELECT YOUR HAND", self.pixel_font_mid, "#ffffff")

        # Custom buttons (Rock, Paper, Scissors)
        buttons = [
            ("ROCK", ICON_ROCK, 160),
            ("PAPER", ICON_PAPER, 260),
            ("SCISSOR", ICON_SCISSORS, 360)
        ]

        for idx, (label, icon, x_start) in enumerate(buttons):
            y_start = 320
            w_btn = 80
            h_btn = 85

            # Handle Hover translation and highlight
            is_hover = (self.hover_btn == idx)
            btn_bg = "#292524" if not is_hover else "#44403c"
            btn_border = "#ffffff" if not is_hover else "#f1c40f"
            draw_y_offset = 2 if is_hover else 0

            # Draw outer card border
            self.canvas.create_rectangle(x_start, y_start + draw_y_offset, 
                                         x_start + w_btn, y_start + h_btn + draw_y_offset, 
                                         fill=btn_bg, outline=btn_border, width=2)

            # Center and draw 16x16 icon at scale 2
            icon_x = x_start + (w_btn - 32) // 2
            icon_y = y_start + 10 + draw_y_offset
            self.draw_pixel_art(icon, icon_x, icon_y, scale=2)

            # Draw text
            text_x = x_start + w_btn // 2
            text_y = y_start + 65 + draw_y_offset
            self.draw_text_with_shadow(text_x, text_y, label, self.pixel_font_small, "#ffffff")

    # Render Match Finish screens
    def draw_game_over(self, W, H):
        if self.player_score >= 3:
            # Victory screens - gold/yellow background
            self.canvas.create_rectangle(0, 0, W, H, fill="#1e1b4b", outline="")
            # Gold panels
            self.canvas.create_rectangle(50, 40, W - 50, H - 40, fill="#fef08a", outline="#ffffff", width=4)
            # Trophy pixel art
            self.draw_pixel_art(TROPHY_MATRIX, W // 2 - 48, H // 2 - 90, scale=4)
            # Text
            self.draw_text_with_shadow(W // 2, H // 2 + 30, "MATCH VICTORY!", self.pixel_font_large, "#ca8a04")
            self.draw_text_with_shadow(W // 2, H // 2 + 75, f"YOU {self.player_score} - {self.computer_score} COMPUTER", 
                                       self.pixel_font_mid, "#1e1b4b")
        else:
            # Defeat screen - dark red/charcoal
            self.canvas.create_rectangle(0, 0, W, H, fill="#111827", outline="")
            # Red panels
            self.canvas.create_rectangle(50, 40, W - 50, H - 40, fill="#7f1d1d", outline="#ffffff", width=4)
            # Skull pixel art
            self.draw_pixel_art(SKULL_MATRIX, W // 2 - 48, H // 2 - 90, scale=4)
            # Text
            self.draw_text_with_shadow(W // 2, H // 2 + 30, "GAME OVER", self.pixel_font_large, "#ef4444")
            self.draw_text_with_shadow(W // 2, H // 2 + 75, f"YOU {self.player_score} - {self.computer_score} COMPUTER", 
                                       self.pixel_font_mid, "#ffffff")

        # Play Again Button
        bx1 = 220
        by1 = 345
        bx2 = 380
        by2 = 390
        
        btn_bg = "#292524" if not self.hover_play_again else "#44403c"
        btn_border = "#ffffff" if not self.hover_play_again else "#f1c40f"
        draw_y_offset = 2 if self.hover_play_again else 0

        self.canvas.create_rectangle(bx1, by1 + draw_y_offset, bx2, by2 + draw_y_offset, 
                                     fill=btn_bg, outline=btn_border, width=2)
        self.draw_text_with_shadow(300, 365 + draw_y_offset, "PLAY AGAIN", self.pixel_font_small, "#ffffff")

    # Animated Shake Step Loop
    def run_shake_animation(self):
        if self.shake_frame < 12:
            # Trigger shake beeps on beats: frame 0, 4, 8
            if self.shake_frame % 4 == 0:
                play_sound("shake")
            
            self.shake_frame += 1
            self.redraw()
            self.root.after(110, self.run_shake_animation)
        else:
            # Transition to REVEAL state
            self.state = "reveal"
            
            # Determine winner
            p = self.player_choice
            c = self.computer_choice
            
            if p == c:
                self.result_text = "TIE!"
                self.result_color = "#f1c40f" # Yellow
                play_sound("tie")
            elif (p == "rock" and c == "scissors") or \
                 (p == "paper" and c == "rock") or \
                 (p == "scissors" and c == "paper"):
                self.result_text = "YOU WIN!"
                self.result_color = "#2ecc71" # Green
                self.player_score += 1
                play_sound("win_round")
            else:
                self.result_text = "YOU LOSE!"
                self.result_color = "#e74c3c" # Red
                self.computer_score += 1
                play_sound("lose_round")
                
            self.redraw()
            
            # Wait 2 seconds before resetting or ending game
            self.root.after(2000, self.end_round)

    # End round state check
    def end_round(self):
        if self.player_score >= 3 or self.computer_score >= 3:
            self.state = "game_over"
            if self.player_score >= 3:
                play_sound("match_victory")
            else:
                play_sound("match_defeat")
        else:
            self.state = "choose"
            self.player_choice = None
            self.computer_choice = None
            
        self.redraw()

    # Mouse move handler for custom button hover states
    def on_mouse_move(self, event):
        prev_hover_btn = self.hover_btn
        prev_hover_play_again = self.hover_play_again
        
        # 1. State: CHOOSE
        if self.state == "choose":
            self.hover_play_again = False
            # Check button collision
            # btn x: 160-240, 260-340, 360-440
            # btn y: 320-405
            if 320 <= event.y <= 405:
                if 160 <= event.x <= 240:
                    self.hover_btn = 0
                elif 260 <= event.x <= 340:
                    self.hover_btn = 1
                elif 360 <= event.x <= 440:
                    self.hover_btn = 2
                else:
                    self.hover_btn = -1
            else:
                self.hover_btn = -1
                
        # 2. State: GAME OVER
        elif self.state == "game_over":
            self.hover_btn = -1
            # Check "Play Again" button: 220 <= x <= 380, 345 <= y <= 390
            if 220 <= event.x <= 380 and 345 <= event.y <= 390:
                self.hover_play_again = True
            else:
                self.hover_play_again = False
        else:
            self.hover_btn = -1
            self.hover_play_again = False

        # Set mouse cursor
        if self.hover_btn != -1 or self.hover_play_again:
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="")

        # Trigger redraw if hover states changed
        if self.hover_btn != prev_hover_btn or self.hover_play_again != prev_hover_play_again:
            self.redraw()

    # Mouse click event handler
    def on_mouse_click(self, event):
        # 1. State: CHOOSE
        if self.state == "choose" and self.hover_btn != -1:
            play_sound("click")
            choices = ["rock", "paper", "scissors"]
            self.player_choice = choices[self.hover_btn]
            self.computer_choice = random.choice(choices)
            
            # Start shake sequence
            self.state = "shake"
            self.shake_frame = 0
            self.hover_btn = -1
            self.canvas.config(cursor="")
            self.run_shake_animation()
            
        # 2. State: GAME OVER
        elif self.state == "game_over" and self.hover_play_again:
            play_sound("click")
            # Reset Match scores
            self.player_score = 0
            self.computer_score = 0
            self.state = "choose"
            self.player_choice = None
            self.computer_choice = None
            self.hover_play_again = False
            self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGame(root)
    root.mainloop()
