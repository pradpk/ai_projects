import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Guess the Magic Number!")
root.geometry("600x700")
root.config(bg="#FFFAE6")

secret_number = 0
attempts = 0
start_time = None
guess_history = []
difficulty_range = 100
timer_running = False
celebrating = False


def reset_game():
    global secret_number, attempts, guess_history, celebrating
    celebrating = False

    secret_number = random.randint(1, difficulty_range)
    attempts = 0
    guess_history = []

    message_label.config(text=f"I’m thinking of a number 1–{difficulty_range}!", fg="#333")
    hint_label.config(text="")
    attempts_label.config(text="🔢 Attempts: 0")
    entry.delete(0, tk.END)
    history_list.delete(0, tk.END)


def update_timer():
    if timer_running and start_time is not None:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"⏱ Time: {elapsed} sec")
    root.after(1000, update_timer)


def blink_message():
    original_color = message_label.cget("fg")
    message_label.config(fg="white")
    root.after(150, lambda: message_label.config(fg=original_color))


def give_hint(last_guess=None):
    if attempts == 5:
        hint_label.config(text=f"Hint: The number is {'even' if secret_number % 2 == 0 else 'odd'}!")
    elif attempts == 10:
        hint_label.config(text="Hint: The number is in the upper half!"
        if secret_number > difficulty_range // 2
        else "Hint: The number is in the lower half!")
    elif attempts == 15 and last_guess is not None:
        if abs(secret_number - last_guess) <= 10:
            hint_label.config(text="Hint: You are VERY close!")
        else:
            hint_label.config(text="Hint: You are more than 10 away!")


# -----------------------------
# Celebration: Continuous Color Flash
# -----------------------------
celebration_colors = ["red", "orange", "yellow", "green", "blue", "purple"]

def flash_celebration(index=0):
    if not celebrating:
        return

    color = celebration_colors[index % len(celebration_colors)]
    message_label.config(fg=color)

    root.after(120, lambda: flash_celebration(index + 1))


def celebrate():
    global celebrating
    celebrating = True
    flash_celebration()


# -----------------------------
# Check Guess
# -----------------------------
def check_guess():
    global attempts, timer_running, celebrating
    blink_message()
    attempts += 1
    attempts_label.config(text=f"🔢 Attempts: {attempts}")

    try:
        guess = int(entry.get())
    except ValueError:
        message_label.config(text="Please enter a number!", fg="red")
        return

    entry.delete(0, tk.END)

    guess_history.append(guess)
    history_list.insert(tk.END, f"Guess {attempts}: {guess}")

    give_hint(guess)

    if guess < secret_number:
        message_label.config(text="Too LOW! Try again 😊", fg="#0077CC")
    elif guess > secret_number:
        message_label.config(text="Too HIGH! Try again 😄", fg="#CC5500")
    else:
        elapsed = int(time.time() - start_time)
        timer_running = False  # STOP TIMER

        message_label.config(
            text=f"🎉 You got it in {attempts} attempts and {elapsed} seconds! 🎉",
            fg="green"
        )

        celebrate()


# -----------------------------
# Difficulty Selector
# -----------------------------
def set_difficulty(level):
    global difficulty_range, start_time, timer_running, celebrating

    celebrating = False

    if level == "Easy":
        difficulty_range = 50
    elif level == "Medium":
        difficulty_range = 100
    else:
        difficulty_range = 500

    start_time = time.time()
    timer_running = True

    reset_game()


# -----------------------------
# UI ELEMENTS
# -----------------------------
title_label = tk.Label(
    root,
    text="🎈 Guess the Magic Number! 🎈",
    font=("Comic Sans MS", 22, "bold"),
    bg="#FFFAE6",
    fg="#FF5733"
)
title_label.pack(pady=20)

difficulty_frame = tk.Frame(root, bg="#FFFAE6")
difficulty_frame.pack()

tk.Button(difficulty_frame, text="Easy", font=("Comic Sans MS", 14),
          bg="#A3E4D7", command=lambda: set_difficulty("Easy")).grid(row=0, column=0, padx=10)

tk.Button(difficulty_frame, text="Medium", font=("Comic Sans MS", 14),
          bg="#F9E79F", command=lambda: set_difficulty("Medium")).grid(row=0, column=1, padx=10)

tk.Button(difficulty_frame, text="Hard", font=("Comic Sans MS", 14),
          bg="#F5B7B1", command=lambda: set_difficulty("Hard")).grid(row=0, column=2, padx=10)

stats_frame = tk.Frame(root, bg="#FFFAE6")
stats_frame.pack()

timer_label = tk.Label(stats_frame, text="⏱ Time: 0 sec", font=("Comic Sans MS", 16), bg="#FFFAE6")
timer_label.grid(row=0, column=0, padx=20)

attempts_label = tk.Label(stats_frame, text="🔢 Attempts: 0", font=("Comic Sans MS", 16), bg="#FFFAE6")
attempts_label.grid(row=0, column=1, padx=20)

entry = tk.Entry(root, font=("Comic Sans MS", 18), justify="center")
entry.pack(pady=10)

tk.Button(
    root,
    text="Guess!",
    font=("Comic Sans MS", 18, "bold"),
    bg="#FFD700",
    fg="#333",
    command=check_guess
).pack(pady=10)

message_label = tk.Label(
    root,
    text="Select a difficulty to begin!",
    font=("Comic Sans MS", 16),
    bg="#FFFAE6",
    fg="#333"
)
message_label.pack(pady=20)

hint_label = tk.Label(
    root,
    text="",
    font=("Comic Sans MS", 14),
    bg="#FFFAE6",
    fg="#AA00AA"
)
hint_label.pack(pady=10)

tk.Button(
    root,
    text="Reset Game",
    font=("Comic Sans MS", 14),
    bg="#FF6F61",
    fg="white",
    command=reset_game
).pack(pady=10)

history_label = tk.Label(
    root,
    text="📜 Your Guesses:",
    font=("Comic Sans MS", 16),
    bg="#FFFAE6",
    fg="#444"
)
history_label.pack(pady=5)

history_frame = tk.Frame(root)
history_frame.pack()

history_list = tk.Listbox(
    history_frame,
    width=30,
    height=10,
    font=("Comic Sans MS", 14),
    bg="#FFF3C4"
)
history_list.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_list.yview)

update_timer()
root.mainloop()