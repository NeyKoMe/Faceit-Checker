import tkinter as tk
from tkinter import ttk
from core.checker import check_players

def search_player():
        # Сброс прогресса перед новой проверкой
    progress["value"] = 0
    progress_label.config(text="")


    user_input = input_box.get("1.0", "end-1c").strip()

    if not user_input:
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Введите SteamID или ссылку.")
        return

    inputs = [i.strip() for i in user_input.split("\n") if i.strip()]
    results = []

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "Загрузка...\n")
    root.update()


    total = len(inputs)
    progress["maximum"] = total
    progress["value"] = 0
    results = check_players(inputs)
    # 🔥 обновление прогресса
    progress["value"] = total
    progress_label.config(text="Готово!")
    root.update_idletasks()

    # сортировка
    if sort_var.get():
        results.sort(key=lambda x: x["level"], reverse=True)

    result_box.delete("1.0", tk.END)

    # 🔥 ВАЖНО: этот цикл должен быть внутри функции
    for player in results:
        insert_player(player)

    progress_label.config(text="Готово!")



def insert_player(player):
    level = player["level"]

    if level >= 8:
        color_tag = "red"
    elif level >= 5:
        color_tag = "yellow"
    else:
        color_tag = "green"

    result_box.insert(tk.END, "------------------------------------\n", color_tag)
    result_box.insert(tk.END, f"{player['nickname']} | Level {level}\n", ("title", color_tag))
    result_box.insert(tk.END, f"ELO: {player['elo']}\n", color_tag)
    result_box.insert(tk.END, f"K/D: {player['kd']} | HS: {player['hs']}\n", color_tag)
    result_box.insert(tk.END, f"Matches: {player['matches']}\n", color_tag)
    result_box.insert(tk.END, "------------------------------------\n\n", color_tag)
    result_box.tag_config("red", foreground="red")
    result_box.tag_config("yellow", foreground="orange")
    result_box.tag_config("green", foreground="green")
    result_box.tag_config("title", font=("Consolas", 12, "bold"))
# Создание окна
root = tk.Tk()
root.title("CS2 Faceit Checker")
root.geometry("600x800")
root.resizable(True, True)
root.minsize(400, 500)
root.update_idletasks()

window_width = root.winfo_width()
window_height = root.winfo_height()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"+{x}+{y}")


clipboard_history = []

def paste_with_history():
    try:
        text = root.clipboard_get().strip()
    except:
        return

    if not text:
        return

    # Добавляем в историю
    if text not in clipboard_history:
        clipboard_history.insert(0, text)

    # Ограничение до 5 элементов
    if len(clipboard_history) > 5:
        clipboard_history.pop()

    # Вставляем в поле
    input_box.delete("1.0", "end")
    input_box.insert("1.0", text)

paste_button = tk.Button(root, text="Вставить", command=paste_with_history)
paste_button.pack()

def show_history():
    if not clipboard_history:
        return

    history_window = tk.Toplevel(root)
    history_window.title("История вставки")
    history_window.geometry("400x300")

    for item in clipboard_history:
        btn = tk.Button(
            history_window,
            text=item[:50] + ("..." if len(item) > 50 else ""),
            anchor="w",
            command=lambda t=item: insert_from_history(t, history_window)
        )
        btn.pack(fill="x")


def insert_from_history(text, window):
    input_box.delete("1.0", "end")
    input_box.insert("1.0", text)
    window.destroy()

history_button = tk.Button(root, text="История", command=show_history)
history_button.pack()
# Заголовок
title = tk.Label(root, text="CS2 Faceit Checker", font=("Arial", 24, "bold"))
title.pack(pady=15)

# Поле ввода
# Поле ввода (5 строк)
input_box = tk.Text(root, height=5, font=("Arial", 12))
input_box.pack(padx=20, pady=5, fill="x")

def limit_lines(event):
    lines = input_box.get("1.0", "end-1c").split("\n")
    if len(lines) > 5:
        input_box.delete("6.0", "end")
        return "break"

# Кнопка поиска
button = tk.Button(root, text="Найти", command=search_player, font=("Arial", 12))
button.pack(pady=10)

progress_label = tk.Label(root, text="")
progress_label.pack()

sort_var = tk.BooleanVar(value=True)

sort_checkbox = tk.Checkbutton(
    root,
    text="Сортировать по уровню",
    variable=sort_var
)
sort_checkbox.pack()

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=5)
# Поле вывода
# Контейнер для текста + скролла
frame = tk.Frame(root)
frame.pack(padx=15, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(frame, wrap="word", font=("Consolas", 11), yscrollcommand=scrollbar.set)
result_box.pack(side="left", fill="both", expand=True)

scrollbar.config(command=result_box.yview)

def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"

def handle_ctrl_shortcuts(event):
    # Проверяем, зажат ли Ctrl
    if event.state & 0x4:
        # 65 = A
        if event.keycode == 65:
            event.widget.tag_add("sel", "1.0", "end")
            return "break"

        # 86 = V
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
            return "break"

        # 67 = C
        if event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
            return "break"

        # 88 = X
        if event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
            return "break"

for widget in (input_box, result_box):
    widget.bind("<KeyPress>", handle_ctrl_shortcuts)

def run_app():
    root.mainloop()