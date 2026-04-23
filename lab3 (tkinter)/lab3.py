import random
import string
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
WINDOW_TITLE = "Game KeyGen"

BG_IMAGE_PATH = "background.jpg"
MUSIC_PATH = "background_music.mp3"
MUSIC_VOLUME = 0.1

LETTERS = string.ascii_uppercase
ANIMATION_CHARS = string.ascii_uppercase + string.digits

INPUT_WIDTH = 200
OUTPUT_WIDTH = 300

BLOCK_LETTERS_COUNT = 2
SUM_BLOCK_DIGITS = 4

TITLE_FONT = ("Arial Black", 22)
LABEL_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 14)
OUTPUT_FONT = ("Consolas", 16)
BUTTON_FONT = LABEL_FONT
MUSIC_BTN_FONT = ("Arial", 10)

TITLE_FG_COLOR = "yellow"
TITLE_BLINK_COLOR = "white"
TITLE_BG_COLOR = "#2d3436"

BUTTON_BG_COLOR = "#74b9ff"
BUTTON_PULSE_COLOR = "#a0c4ff"
MUSIC_BTN_COLOR = "#55efc4"
LABEL_BG_COLOR = "#dfe6e9"

INPUT_PROMPT = "Введите 6-значное число:"
OUTPUT_PROMPT = "Ваш ключ:"
ERROR_MSG = "Введите корректное 6-значное число (6 цифр)."
ERROR_TITLE = "Ошибка"

ANCHOR_CENTER = "center"
STATE_NORMAL = "normal"
STATE_READONLY = "readonly"

ANIMATION_DELAY = 50
TITLE_BLINK_DELAY = 500
PULSE_DELAY = 400

window = tk.Tk()
window.title(WINDOW_TITLE)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)

bg_image = Image.open(BG_IMAGE_PATH).resize((WINDOW_WIDTH, WINDOW_HEIGHT))
bg_photo = ImageTk.PhotoImage(bg_image)
tk.Label(window, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(
    window,
    text="GAME KEYGEN",
    font=TITLE_FONT,
    fg=TITLE_FG_COLOR,
    bg=TITLE_BG_COLOR,
)
title_label.place(relx=0.5, y=20, anchor=ANCHOR_CENTER)

input_label = tk.Label(
    window,
    text=INPUT_PROMPT,
    font=LABEL_FONT,
    bg=LABEL_BG_COLOR,
)
input_label.place(relx=0.5, y=70, anchor=ANCHOR_CENTER)

input_entry = tk.Entry(window, font=ENTRY_FONT, justify="center")
input_entry.place(relx=0.5, y=100, anchor=ANCHOR_CENTER, width=INPUT_WIDTH)

output_label = tk.Label(
    window,
    text=OUTPUT_PROMPT,
    font=LABEL_FONT,
    bg=LABEL_BG_COLOR,
)
output_label.place(relx=0.5, y=150, anchor=ANCHOR_CENTER)

output_entry = tk.Entry(
    window, font=OUTPUT_FONT, justify="center", state=STATE_READONLY
)
output_entry.place(relx=0.5, y=180, anchor=ANCHOR_CENTER, width=OUTPUT_WIDTH)


def blink():
    current_fg = title_label.cget("fg")
    title_label.config(
        fg=TITLE_FG_COLOR if current_fg == TITLE_BLINK_COLOR else TITLE_BLINK_COLOR
    )
    window.after(TITLE_BLINK_DELAY, blink)


def animate_key(key):
    output_entry.config(state=STATE_NORMAL)
    output_entry.delete(0, tk.END)
    output_entry.insert(0, " " * len(key))
    output_entry.config(state=STATE_READONLY)

    current_chars = [" "] * len(key)

    def update_char(index=0):
        if index >= len(key):
            return

        target_char = key[index]

        if target_char == "-":
            current_chars[index] = "-"
            output_entry.config(state=STATE_NORMAL)
            output_entry.delete(0, tk.END)
            output_entry.insert(0, "".join(current_chars))
            output_entry.config(state=STATE_READONLY)
            window.after(ANIMATION_DELAY, lambda: update_char(index + 1))
            return

        trial = random.choice(ANIMATION_CHARS)
        current_chars[index] = trial
        output_entry.config(state=STATE_NORMAL)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, "".join(current_chars))
        output_entry.config(state=STATE_READONLY)

        if trial != target_char:
            window.after(ANIMATION_DELAY, lambda: update_char(index))
        else:
            window.after(ANIMATION_DELAY, lambda: update_char(index + 1))

    update_char()


def generate_key():
    num = input_entry.get().strip()
    if not (num.isdigit() and len(num) == 6):
        messagebox.showerror(ERROR_TITLE, ERROR_MSG)
        return

    digits_1 = list(num[3:])
    digits_2 = list(num[:3])
    random.shuffle(digits_1)
    random.shuffle(digits_2)
    part1_digits = "".join(digits_1)
    part2_digits = "".join(digits_2)

    block1 = part1_digits + "".join(
        random.choice(LETTERS) for _ in range(BLOCK_LETTERS_COUNT)
    )
    block2 = part2_digits + "".join(
        random.choice(LETTERS) for _ in range(BLOCK_LETTERS_COUNT)
    )
    block3 = str(int(part1_digits) + int(part2_digits)).zfill(SUM_BLOCK_DIGITS)

    key = f"{block1}-{block2}-{block3}"
    animate_key(key)


def toggle_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def pulse_button_effect(button, growing=True):
    new_bg = BUTTON_PULSE_COLOR if growing else BUTTON_BG_COLOR
    button.config(bg=new_bg)
    window.after(PULSE_DELAY, lambda: pulse_button_effect(button, not growing))


generate_btn = tk.Button(
    window,
    text="Сгенерировать ключ",
    font=BUTTON_FONT,
    bg=BUTTON_BG_COLOR,
    command=generate_key,
)
generate_btn.place(relx=0.5, y=250, anchor=ANCHOR_CENTER)
pulse_button_effect(generate_btn)

music_btn = tk.Button(
    window,
    text="🎵 Вкл/Выкл музыку",
    font=MUSIC_BTN_FONT,
    bg=MUSIC_BTN_COLOR,
    command=toggle_music,
)
music_btn.place(relx=0.5, y=310, anchor=ANCHOR_CENTER)

pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

blink()
window.mainloop()
pygame.mixer.music.stop()
