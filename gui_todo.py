import json
import os
import sys

# Auto-fix for Tcl/Tk library path initialization on Windows Python installs
possible_bases = [
    os.path.dirname(sys.executable),
    getattr(sys, "base_prefix", sys.prefix),
    r"C:\Users\hussa\AppData\Local\Programs\Python\Python313"
]
for base in possible_bases:
    tcl_path = os.path.join(base, "tcl", "tcl8.6")
    tk_path = os.path.join(base, "tcl", "tk8.6")
    if os.path.exists(os.path.join(tcl_path, "init.tcl")):
        os.environ["TCL_LIBRARY"] = tcl_path
        if os.path.exists(tk_path):
            os.environ["TK_LIBRARY"] = tk_path
        break

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

FILE_NAME = os.path.join(os.path.dirname(__file__), "tasks.json")

# ---------------------------------------------------------
# Data Persistence Functions
# ---------------------------------------------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                # Ensure all tasks have a 'day' field for the weekly layout
                for task in tasks:
                    if "day" not in task:
                        task["day"] = "Notes"
                return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []
    return []

def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        print(f"Error saving tasks: {e}")

# ---------------------------------------------------------
# Custom Canvas Drawings for Cute Pastel Aesthetic
# ---------------------------------------------------------
def draw_sloth(canvas, x, y):
    """Draws a cute sleeping sloth on a pillow (Top Header Motif)"""
    # Pillow (Teal / Mint)
    canvas.create_oval(x-10, y+10, x+90, y+55, fill="#9CD3CE", outline="#6FA8A3", width=2)
    canvas.create_oval(x-5, y+15, x+85, y+50, fill="#B5E4E0", outline="")
    
    # Sloth Body (Soft Pinkish Brown / Pastel Magenta Sloth from reference image!)
    canvas.create_oval(x+10, y, x+75, y+40, fill="#FF9EAA", outline="#D46B7A", width=2)
    # Sloth Head
    canvas.create_oval(x+45, y-15, x+85, y+25, fill="#FFB7C3", outline="#D46B7A", width=2)
    # Sloth Face Mask
    canvas.create_oval(x+55, y-5, x+82, y+18, fill="#FFF0F3", outline="")
    # Eye Patches
    canvas.create_oval(x+58, y, x+68, y+10, fill="#D46B7A", outline="")
    canvas.create_oval(x+70, y, x+80, y+10, fill="#D46B7A", outline="")
    # Sleeping Eyes (^ ^)
    canvas.create_arc(x+60, y+1, x+66, y+8, start=0, extent=180, style=tk.ARC, outline="#4A2E35", width=2)
    canvas.create_arc(x+72, y+1, x+78, y+8, start=0, extent=180, style=tk.ARC, outline="#4A2E35", width=2)
    # Nose & Smile
    canvas.create_oval(x+67, y+8, x+71, y+11, fill="#4A2E35", outline="")
    canvas.create_arc(x+66, y+9, x+72, y+14, start=180, extent=180, style=tk.ARC, outline="#4A2E35", width=1)

def draw_flower(canvas, x, y):
    """Draws cute pink flower 🌸"""
    for angle in [0, 72, 144, 216, 288]:
        import math
        rad = math.radians(angle)
        px = x + 12 * math.cos(rad)
        py = y + 12 * math.sin(rad)
        canvas.create_oval(px-8, py-8, px+8, py+8, fill="#FFB7C3", outline="#E88A99", width=1.5)
    canvas.create_oval(x-7, y-7, x+7, y+7, fill="#FFE5A3", outline="#E8B949", width=1.5)
    # Face on flower
    canvas.create_oval(x-3, y-2, x-1, y, fill="#4A2E35")
    canvas.create_oval(x+1, y-2, x+3, y, fill="#4A2E35")
    canvas.create_arc(x-3, y-1, x+3, y+4, start=180, extent=180, style=tk.ARC, outline="#4A2E35", width=1)

def draw_butterfly(canvas, x, y):
    """Draws cute butterfly 🦋"""
    # Wings
    canvas.create_oval(x-18, y-14, x-2, y+2, fill="#FFB7C3", outline="#D46B7A", width=1.5)
    canvas.create_oval(x+2, y-14, x+18, y+2, fill="#FFB7C3", outline="#D46B7A", width=1.5)
    canvas.create_oval(x-14, y, x-2, y+12, fill="#F7C8E0", outline="#D46B7A", width=1.5)
    canvas.create_oval(x+2, y, x+14, y+12, fill="#F7C8E0", outline="#D46B7A", width=1.5)
    # Body
    canvas.create_oval(x-3, y-12, x+3, y+10, fill="#5C4B51", outline="")
    # Antennae
    canvas.create_line(x-1, y-12, x-6, y-18, fill="#5C4B51", width=1.5)
    canvas.create_line(x+1, y-12, x+6, y-18, fill="#5C4B51", width=1.5)

def draw_turtle(canvas, x, y):
    """Draws cute green turtle 🐢"""
    # Shell
    canvas.create_oval(x-15, y-12, x+15, y+8, fill="#88C0AD", outline="#4B7E6E", width=1.5)
    # Head
    canvas.create_oval(x+10, y-6, x+24, y+6, fill="#BCE3C5", outline="#4B7E6E", width=1.5)
    canvas.create_oval(x+18, y-3, x+20, y-1, fill="#2D4A3E") # Eye
    # Legs
    canvas.create_oval(x-14, y+4, x-6, y+12, fill="#BCE3C5", outline="#4B7E6E", width=1.5)
    canvas.create_oval(x+4, y+4, x+12, y+12, fill="#BCE3C5", outline="#4B7E6E", width=1.5)

def draw_star(canvas, x, y):
    """Draws cute star 🌟"""
    points = []
    import math
    for i in range(10):
        r = 14 if i % 2 == 0 else 6
        angle = i * 36 - 90
        rad = math.radians(angle)
        points.append(x + r * math.cos(rad))
        points.append(y + r * math.sin(rad))
    canvas.create_polygon(points, fill="#FFDE7D", outline="#E6B800", width=1.5)
    # Cute face
    canvas.create_oval(x-4, y-2, x-2, y, fill="#4A2E35")
    canvas.create_oval(x+2, y-2, x+4, y, fill="#4A2E35")
    canvas.create_arc(x-3, y-1, x+3, y+3, start=180, extent=180, style=tk.ARC, outline="#4A2E35", width=1)

def draw_snail(canvas, x, y):
    """Draws cute snail 🐌"""
    # Shell
    canvas.create_oval(x-16, y-16, x+8, y+8, fill="#FFC0D3", outline="#D46B7A", width=1.5)
    canvas.create_arc(x-10, y-10, x+2, y+2, start=0, extent=270, style=tk.ARC, outline="#D46B7A", width=1.5)
    # Body
    canvas.create_oval(x-12, y+2, x+20, y+12, fill="#FFE5D9", outline="#D46B7A", width=1.5)
    # Eye stalks
    canvas.create_line(x+14, y+2, x+14, y-6, fill="#D46B7A", width=1.5)
    canvas.create_line(x+18, y+2, x+18, y-6, fill="#D46B7A", width=1.5)
    canvas.create_oval(x+12, y-9, x+16, y-5, fill="#D46B7A")
    canvas.create_oval(x+16, y-9, x+20, y-5, fill="#D46B7A")

# ---------------------------------------------------------
# Main GUI Application
# ---------------------------------------------------------
class WeeklyToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly To-Do List 2026 🌸")
        self.root.geometry("1050x780")
        self.root.minsize(980, 720)
        self.root.configure(bg="#FCE4EC") # Soft pastel pink outer margin

        self.tasks = load_tasks()
        self.search_query = ""

        # Main Scrollable / Padded Container
        self.setup_ui()
        self.refresh_tasks()

    def setup_ui(self):
        # Outer Scalloped Canvas / Border Simulation Frame
        self.main_border = tk.Frame(self.root, bg="#FFB6C1", bd=0, padx=12, pady=12)
        self.main_border.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.canvas_bg = tk.Frame(self.main_border, bg="#FFFDF7", bd=0, padx=15, pady=15)
        self.canvas_bg.pack(fill=tk.BOTH, expand=True)

        # ---------------------------------------------------------
        # Header Section
        # ---------------------------------------------------------
        header_frame = tk.Frame(self.canvas_bg, bg="#FFFDF7")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Title Left Block
        title_box = tk.Frame(header_frame, bg="#FFFDF7")
        title_box.pack(side=tk.LEFT, align="w" if hasattr(tk, "align") else None)

        title_label = tk.Label(
            title_box,
            text="Weekly to do list",
            font=("Comic Sans MS", 28, "bold"),
            fg="#7C5C9B",
            bg="#FFFDF7"
        )
        title_label.pack(side=tk.LEFT, padx=(0, 10))

        badge = tk.Label(
            title_box,
            text="2026",
            font=("Comic Sans MS", 14, "bold"),
            fg="white",
            bg="#FF8EA3",
            padx=10,
            pady=2
        )
        badge.pack(side=tk.LEFT)

        # Cute Header Canvas (Sloth Motif)
        header_canvas = tk.Canvas(header_frame, width=120, height=65, bg="#FFFDF7", highlightthickness=0)
        header_canvas.pack(side=tk.RIGHT, padx=10)
        draw_sloth(header_canvas, 15, 10)

        # ---------------------------------------------------------
        # Controls Bar (Add Task, Search, Stats)
        # ---------------------------------------------------------
        control_bar = tk.Frame(self.canvas_bg, bg="#FFFDF7")
        control_bar.pack(fill=tk.X, pady=(0, 15))

        # Add Task Button
        add_btn = tk.Button(
            control_bar,
            text="➕ Add New Task",
            font=("Comic Sans MS", 11, "bold"),
            bg="#FFB7C3",
            fg="#4A2E35",
            activebackground="#FF9EAA",
            activeforeground="#4A2E35",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.open_add_dialog
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 15))

        # Search Box
        search_lbl = tk.Label(control_bar, text="🔍 Search:", font=("Comic Sans MS", 11, "bold"), fg="#7C5C9B", bg="#FFFDF7")
        search_lbl.pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        search_entry = tk.Entry(
            control_bar,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg="#F3E8F4",
            fg="#4A2E35",
            bd=1,
            relief=tk.SOLID
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=False, ipadx=5, ipady=3)

        # Stats Button
        stats_btn = tk.Button(
            control_bar,
            text="📊 Statistics",
            font=("Comic Sans MS", 11, "bold"),
            bg="#9CD3CE",
            fg="#1F4E4A",
            activebackground="#88C0AD",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.show_statistics
        )
        stats_btn.pack(side=tk.RIGHT)

        # ---------------------------------------------------------
        # Grid Cards Section (8 Cards: Mon-Sun + Notes)
        # ---------------------------------------------------------
        self.grid_frame = tk.Frame(self.canvas_bg, bg="#FFFDF7")
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        # Configure 4 columns, 2 rows
        for col in range(4):
            self.grid_frame.columnconfigure(col, weight=1, uniform="col")
        for row in range(2):
            self.grid_frame.rowconfigure(row, weight=1, uniform="row")

        # Define Day Card Configurations inspired by user's theme image
        self.card_configs = [
            {"day": "Monday", "bg": "#FBE8EE", "border": "#F3C5D4", "title_color": "#B84A67", "draw": draw_flower, "grid": (0, 0)},
            {"day": "Tuesday", "bg": "#F3E8F4", "border": "#D8B4E2", "title_color": "#7C5C9B", "bullet": "💜", "grid": (0, 1)},
            {"day": "Wednesday", "bg": "#F8E8EE", "border": "#F3C5D4", "title_color": "#B84A67", "draw": draw_butterfly, "grid": (0, 2)},
            {"day": "Thursday", "bg": "#FFF8E7", "border": "#FCE5B2", "title_color": "#9C7A2B", "draw": draw_turtle, "grid": (0, 3)},
            {"day": "Friday", "bg": "#FCEEEF", "border": "#F9C6CB", "title_color": "#C24D5A", "bullet": "💖", "grid": (1, 0)},
            {"day": "Saturday", "bg": "#FFF7E6", "border": "#FFE2B3", "title_color": "#A86B13", "draw": draw_star, "grid": (1, 1)},
            {"day": "Sunday", "bg": "#F4F9F2", "border": "#C7E5C3", "title_color": "#4A7C45", "bullet": "💚", "grid": (1, 2)},
            {"day": "Notes", "bg": "#FDEEF4", "border": "#F8C4DC", "title_color": "#A84B78", "draw": draw_snail, "grid": (1, 3)},
        ]

        self.card_frames = {}

        for cfg in self.card_configs:
            r, c = cfg["grid"]
            day_name = cfg["day"]

            # Card outer box
            card = tk.Frame(
                self.grid_frame,
                bg=cfg["bg"],
                highlightbackground=cfg["border"],
                highlightthickness=2,
                bd=0,
                padx=8,
                pady=6
            )
            card.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

            # Card Header Frame
            card_hdr = tk.Frame(card, bg=cfg["bg"])
            card_hdr.pack(fill=tk.X, pady=(0, 4))

            title_lbl = tk.Label(
                card_hdr,
                text=day_name,
                font=("Comic Sans MS", 13, "bold"),
                fg=cfg["title_color"],
                bg=cfg["bg"]
            )
            title_lbl.pack(side=tk.TOP, anchor="center")

            # Mini Canvas for illustration if specified
            if "draw" in cfg:
                icon_canvas = tk.Canvas(card_hdr, width=40, height=30, bg=cfg["bg"], highlightthickness=0)
                icon_canvas.pack(side=tk.TOP, anchor="center")
                cfg["draw"](icon_canvas, 20, 15)

            # Scrollable / List Container for tasks in this day card
            list_canvas = tk.Canvas(card, bg=cfg["bg"], highlightthickness=0)
            scrollbar = tk.Scrollbar(card, orient="vertical", command=list_canvas.yview)
            task_list_inner = tk.Frame(list_canvas, bg=cfg["bg"])

            task_list_inner.bind(
                "<Configure>",
                lambda e, canvas=list_canvas: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            list_canvas.create_window((0, 0), window=task_list_inner, anchor="nw")
            list_canvas.configure(yscrollcommand=scrollbar.set)

            list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Save references
            self.card_frames[day_name] = {
                "container": task_list_inner,
                "config": cfg
            }

    def refresh_tasks(self):
        """Clears and re-populates all task rows across day cards based on search filter."""
        for day, data in self.card_frames.items():
            for widget in data["container"].winfo_children():
                widget.destroy()

        query = self.search_query.lower().strip()

        for idx, task_data in enumerate(self.tasks):
            task_text = task_data.get("task", "")
            if query and query not in task_text.lower():
                continue

            day = task_data.get("day", "Notes")
            if day not in self.card_frames:
                day = "Notes"

            parent_frame = self.card_frames[day]["container"]
            cfg = self.card_frames[day]["config"]

            # Create Task Row Frame
            row = tk.Frame(parent_frame, bg=cfg["bg"], pady=3)
            row.pack(fill=tk.X, expand=True, anchor="w")

            # Checkbox Button (Cute toggle)
            is_completed = task_data.get("completed", False)
            chk_symbol = "☑" if is_completed else "☐"
            chk_color = "#4CAF50" if is_completed else "#888888"

            chk_btn = tk.Label(
                row,
                text=chk_symbol,
                font=("Segoe UI", 12, "bold"),
                fg=chk_color,
                bg=cfg["bg"],
                cursor="hand2"
            )
            chk_btn.pack(side=tk.LEFT, padx=(0, 4))
            chk_btn.bind("<Button-1>", lambda e, i=idx: self.toggle_complete(i))

            # Task Label (Strikethrough if done)
            fg_color = "#888888" if is_completed else "#2C3E50"
            font_style = ("Segoe UI", 10, "overstrike") if is_completed else ("Segoe UI", 10, "bold")

            lbl = tk.Label(
                row,
                text=task_text,
                font=font_style,
                fg=fg_color,
                bg=cfg["bg"],
                anchor="w",
                justify=tk.LEFT,
                wraplength=130
            )
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Action Buttons Frame (Edit & Delete)
            act_frame = tk.Frame(row, bg=cfg["bg"])
            act_frame.pack(side=tk.RIGHT, padx=(2, 0))

            edit_btn = tk.Label(
                act_frame, text="✏️", font=("Segoe UI", 9), bg=cfg["bg"], cursor="hand2"
            )
            edit_btn.pack(side=tk.LEFT, padx=1)
            edit_btn.bind("<Button-1>", lambda e, i=idx: self.open_edit_dialog(i))

            del_btn = tk.Label(
                act_frame, text="🗑️", font=("Segoe UI", 9), bg=cfg["bg"], cursor="hand2"
            )
            del_btn.pack(side=tk.LEFT, padx=1)
            del_btn.bind("<Button-1>", lambda e, i=idx: self.delete_task(i))

    def on_search_change(self, *args):
        self.search_query = self.search_var.get()
        self.refresh_tasks()

    def toggle_complete(self, idx):
        self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
        save_tasks(self.tasks)
        self.refresh_tasks()

    def delete_task(self, idx):
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_tasks()

    def open_add_dialog(self):
        TaskDialog(self.root, "Add New Task", on_save=self.add_task_callback)

    def add_task_callback(self, task_data):
        self.tasks.append(task_data)
        save_tasks(self.tasks)
        self.refresh_tasks()

    def open_edit_dialog(self, idx):
        TaskDialog(self.root, "Edit Task", task_data=self.tasks[idx], on_save=lambda data: self.edit_task_callback(idx, data))

    def edit_task_callback(self, idx, updated_data):
        self.tasks[idx] = updated_data
        save_tasks(self.tasks)
        self.refresh_tasks()

    def show_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("completed", False))
        pending = total - completed
        percent = int((completed / total) * 100) if total > 0 else 0

        msg = f"🌸 Task Statistics 🌸\n\n" \
              f"📋 Total Tasks: {total}\n" \
              f"✅ Completed: {completed}\n" \
              f"⏳ Pending: {pending}\n" \
              f"📈 Progress: {percent}% Finished!"
        messagebox.showinfo("Statistics", msg)


# ---------------------------------------------------------
# Add / Edit Task Dialog Window
# ---------------------------------------------------------
class TaskDialog(tk.Toplevel):
    def __init__(self, parent, title, task_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("380x360")
        self.resizable(False, False)
        self.configure(bg="#FFFDF7")
        self.transient(parent)
        self.grab_set()

        self.on_save = on_save
        self.task_data = task_data or {}

        self.setup_ui()

    def setup_ui(self):
        # Header
        hdr = tk.Label(
            self,
            text=self.title(),
            font=("Comic Sans MS", 16, "bold"),
            fg="#7C5C9B",
            bg="#FFFDF7",
            pady=10
        )
        hdr.pack(fill=tk.X)

        form = tk.Frame(self, bg="#FFFDF7", padx=20)
        form.pack(fill=tk.BOTH, expand=True)

        # Task Input
        tk.Label(form, text="Task Name:", font=("Comic Sans MS", 10, "bold"), fg="#4A2E35", bg="#FFFDF7").pack(anchor="w", pady=(5, 2))
        self.task_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#F3E8F4", fg="#2C3E50", bd=1)
        self.task_entry.pack(fill=tk.X, ipady=3)
        self.task_entry.insert(0, self.task_data.get("task", ""))

        # Day Selection
        tk.Label(form, text="Assign to Day / Section:", font=("Comic Sans MS", 10, "bold"), fg="#4A2E35", bg="#FFFDF7").pack(anchor="w", pady=(10, 2))
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Notes"]
        self.day_var = tk.StringVar(value=self.task_data.get("day", "Monday"))
        day_cb = ttk.Combobox(form, textvariable=self.day_var, values=days, state="readonly", font=("Segoe UI", 10))
        day_cb.pack(fill=tk.X, ipady=2)

        # Priority Selection
        tk.Label(form, text="Priority:", font=("Comic Sans MS", 10, "bold"), fg="#4A2E35", bg="#FFFDF7").pack(anchor="w", pady=(10, 2))
        priorities = ["Low", "Medium", "High"]
        self.priority_var = tk.StringVar(value=self.task_data.get("priority", "Medium"))
        prio_cb = ttk.Combobox(form, textvariable=self.priority_var, values=priorities, state="readonly", font=("Segoe UI", 10))
        prio_cb.pack(fill=tk.X, ipady=2)

        # Due Date Input
        tk.Label(form, text="Due Date (DD-MM-YYYY):", font=("Comic Sans MS", 10, "bold"), fg="#4A2E35", bg="#FFFDF7").pack(anchor="w", pady=(10, 2))
        self.due_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#F3E8F4", fg="#2C3E50", bd=1)
        self.due_entry.pack(fill=tk.X, ipady=3)
        today_str = datetime.now().strftime("%d-%m-%Y")
        self.due_entry.insert(0, self.task_data.get("due", today_str))

        # Save Button
        save_btn = tk.Button(
            self,
            text="🌸 Save Task 🌸",
            font=("Comic Sans MS", 11, "bold"),
            bg="#FFB7C3",
            fg="#4A2E35",
            activebackground="#FF9EAA",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.save
        )
        save_btn.pack(fill=tk.X, padx=20, pady=15)

    def save(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Task name cannot be empty!", parent=self)
            return

        new_data = {
            "task": text,
            "day": self.day_var.get(),
            "priority": self.priority_var.get(),
            "due": self.due_entry.get().strip(),
            "completed": self.task_data.get("completed", False)
        }

        if self.on_save:
            self.on_save(new_data)
        self.destroy()


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyToDoApp(root)
    root.mainloop()
