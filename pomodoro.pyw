# --- Pomodoro Counter --- #

# Imports #

from pathlib import Path
from tkinter import TclError, messagebox

import customtkinter as ctk
from PIL import Image

# Configuração Global do Tema Dark #
ctk.set_appearance_mode("Dark")

# Main Window #
window = ctk.CTk()
window.title("Pomodori Clock")
window.geometry("300x500")
window.configure(fg_color="#212126")

# Font #
FONT_FAMILY = "Gill Sans Nova"

# Image & Icon #
BASE_DIR = Path(__file__).parent
IMAGE_PATH = BASE_DIR / "pomodoro.png"

try:
    icon_ico_path = BASE_DIR / "pomodoro.ico"
    
    # Se o arquivo .ico ainda não existir na pasta, gera automaticamente a partir do PNG
    if not icon_ico_path.exists():
        img = Image.open(IMAGE_PATH)
        img.save(icon_ico_path, format="ICO", sizes=[(32, 32)])
    
    # Define o ícone nativo do Windows
    window.iconbitmap(icon_ico_path)
except (OSError, TclError) as e:
    print(f"Erro ao carregar o ícone: {e}")

# Carrega e redimensiona a imagem de forma precisa
pomodoro_pil = Image.open(IMAGE_PATH)
pomodoro_img = ctk.CTkImage(light_image=pomodoro_pil, dark_image=pomodoro_pil, size=(120, 120))

# Global Variables #
total_sessions = 0
timer_id = None
is_paused = False
current_mode = "work"
paused_second = 0

# Functions #
def show_screen_setup():
    frame_timer.pack_forget()
    frame_setup.pack(pady=(20, 10))

def show_screen_timer():
    frame_setup.pack_forget()
    frame_timer.pack(pady=(20, 10))

def count(actual_second, total_seconds):
    global total_sessions, timer_id, paused_second

    if is_paused:
        return

    paused_second = actual_second

    minutes = actual_second // 60
    seconds = actual_second % 60

    time_format = f"{minutes:02d}:{seconds:02d}"
    label_timer.configure(text=time_format)

    if actual_second < total_seconds:
        timer_id = window.after(1000, count, actual_second + 1, total_seconds)
    else:
        if current_mode == "work":
            total_sessions += 1
            label_counter.configure(text=f"Completed {total_sessions} sessions today!")
            messagebox.showinfo("Pomodori Clock", "Session finished!")
            start_break()
        else:
            messagebox.showinfo("Pomodori Clock", "Rest is Over")
            show_screen_setup()

def start_timer():
    global current_mode, is_paused
    try:
        target_work = int(session_minutes.get())
        target_break = int(break_minutes.get())
        if target_work <= 0 or target_break <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Pomodori Clock", "Digite um valor de minutos válido!")
        return

    current_mode = "work"
    is_paused = False

    label_status.configure(text="Work!", font=(FONT_FAMILY, 13, "bold"), text_color= "#E74C3C")
    btn_pause.configure(text="⏸ Pause", font=(FONT_FAMILY, 12, "bold"), fg_color="#1E1E22")
    
    show_screen_timer()
    count(0, target_work * 60)

def start_break():
    global current_mode, is_paused
    current_mode = "break"
    is_paused = False

    try:
        target_break = int(break_minutes.get())
    except ValueError:
        target_break = 5

    label_status.configure(text="Break Time!", font=(FONT_FAMILY, 13, "bold"), text_color="#2ECC71")
    btn_pause.configure(text="⏸ Pause", font=(FONT_FAMILY, 12, "bold"), fg_color="#1E1E22")

    count(0, target_break * 60)

def toggle_pause():
    global is_paused, timer_id
    if is_paused:
        is_paused = False
        btn_pause.configure(text="⏸ Pause", font=(FONT_FAMILY, 12, "bold"))

        target_minutes = int(session_minutes.get()) if current_mode == "work" else int(break_minutes.get())
        total_sec = target_minutes * 60
        count(paused_second, total_sec)
    else:
        is_paused = True
        btn_pause.configure(text="▶ Resume", font=(FONT_FAMILY, 12, "bold"))
        if timer_id:
            window.after_cancel(timer_id)
            timer_id = None

def reset_timer():
    global timer_id, is_paused
    is_paused = False
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

    show_screen_setup()

# Setup Screen #
frame_setup = ctk.CTkFrame(window, fg_color="#2A2A30", corner_radius=20, width=260, height=350)
frame_setup.pack_propagate(False) 

label_setup_img = ctk.CTkLabel(frame_setup, image=pomodoro_img, text="")
label_setup_img.pack(pady=(15, 2))

label_instruction = ctk.CTkLabel(
    frame_setup, 
    text="Focus Time (minutes)", 
    font=(FONT_FAMILY, 12, "bold"), 
    text_color="#E0E0E0"
)
label_instruction.pack(pady=(2, 1))

# Inputs #
session_minutes = ctk.CTkEntry(
    frame_setup, 
    width=80, 
    height=32,
    font=(FONT_FAMILY, 15, "bold"), 
    justify="center",
    corner_radius=8,
    fg_color="#1E1E22",
    border_color="#3F3F46",
    text_color="#FFFFFF"
)
session_minutes.pack(pady=2)
session_minutes.insert(0, "25")

# Break #
label_break_instruction = ctk.CTkLabel(
    frame_setup,
    text="Break Time (minutes)",
    font=(FONT_FAMILY, 12, "bold"),
    text_color="#E0E0E0"
)
label_break_instruction.pack(pady=(6, 2))

break_minutes = ctk.CTkEntry(
    frame_setup, 
    width=80, 
    height=32,
    font=(FONT_FAMILY, 15, "bold"), 
    justify="center",
    corner_radius=8,
    fg_color="#1E1E22",
    border_color="#3F3F46",
    text_color="#FFFFFF"
)
break_minutes.pack(pady=2)
break_minutes.insert(0, "5")

# Buttons Setup #

# Start Button #
start_button = ctk.CTkButton(
    frame_setup, 
    text="Start Session", 
    font=(FONT_FAMILY, 14, "bold"), 
    fg_color="#E74C3C", 
    hover_color="#C0392B", 
    text_color="#FFFFFF", 
    corner_radius=18, 
    width=150, 
    height=38, 
    command=start_timer
)
start_button.pack(pady=(15, 10))

# Timer Screen #
frame_timer = ctk.CTkFrame(window, fg_color="#2A2A30", corner_radius=20, width=260, height=350)
frame_timer.pack_propagate(False)

label_pomodoro = ctk.CTkLabel(frame_timer, image=pomodoro_img, text="")
label_pomodoro.pack(pady=(20, 5))

label_timer = ctk.CTkLabel(
    frame_timer, text="00:00", font=(FONT_FAMILY, 42, "bold"), text_color="#D0D0D0"
)
label_timer.pack(pady=2)

label_status = ctk.CTkLabel(
    frame_timer, text="Work!", font=(FONT_FAMILY, 13, "bold"), text_color="#E74C3C"
)
label_status.pack(pady=2)

# Buttons Timer #
frame_buttons = ctk.CTkFrame(frame_timer, fg_color="transparent")
frame_buttons.pack(pady=(15, 10))

btn_pause = ctk.CTkButton(
    frame_buttons,
    text="⏸ Pause",
    font=(FONT_FAMILY, 12, "bold"),
    fg_color="#1E1E22",
    hover_color="#3F3F46",
    text_color="#D0D0D0",
    corner_radius=14,
    width=90,
    height=34,
    command=toggle_pause
)
btn_pause.pack(side="left", padx=5)

btn_stop = ctk.CTkButton(
    frame_buttons,
    text="⏹ Stop",
    font=(FONT_FAMILY, 12, "bold"),
    fg_color="#C0392B",
    hover_color="#962D22",
    text_color="#FFFFFF",
    corner_radius=14,
    width=90,
    height=34,
    command=reset_timer
)
btn_stop.pack(side="left", padx=5)

# Counter Display #
counter_card = ctk.CTkFrame(window, fg_color="#2A2A30", corner_radius=12)
counter_card.pack(side="bottom", pady=25, ipadx=15, ipady=5)

label_counter = ctk.CTkLabel(
    counter_card, 
    text="Completed Today: 0", 
    font=(FONT_FAMILY, 12, "bold"), 
    text_color="#A0A0A0"
)
label_counter.pack()

# Run #
frame_setup.pack(pady=(20, 10))

window.mainloop()