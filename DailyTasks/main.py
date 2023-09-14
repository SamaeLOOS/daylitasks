import tkinter as tk
import sqlite3

"""Здесь создается соединение с базой данных SQLite с именем "todo.db". 
Если таблица "todo" не существует, она создается с двумя полями: 
"id" (уникальный идентификатор задачи) и "task" (текст задачи)."""

conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT
                )''')
conn.commit()


def add_list():
    """Получение текста задачи из виджета ввода (Entry)"""
    task = entry.get()
    if task:
        task_list.append(task)
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        conn.commit()
        """Очистка виджета ввода и обновление отображения списка задач"""
        entry.delete(0, "end")
        update_list_label()


def delete_last():
    """Удаление последней добавленной задачи из списка и из базы данных."""
    if task_list:
        task_list.pop()
        cursor.execute('DELETE FROM tasks WHERE id = (SELECT MAX(id) FROM tasks)')
        conn.commit()
        update_list_label()


def update_list_label():
    """ Обновляет отображение списка задач в виджете Text.
    Она извлекает все задачи из базы данных,
    формирует текстовую строку и обновляет содержимое виджета Text,
    отключая его для редактирования."""
    cursor.execute('SELECT task FROM tasks')
    task_list = [row[0] for row in cursor.fetchall()]
    list_text = "\n".join(task_list)
    list_title.config(state=tk.NORMAL)
    list_title.delete(1.0, tk.END)
    list_title.insert(tk.END, list_text)
    list_title.config(state=tk.DISABLED)


root = tk.Tk()
h = 600
w = 600

root.title('Daily Tasks for Thimble — digital-агентство')
root.config(bg='#050D7C')

photo = tk.PhotoImage(file='logo.png')
root.iconphoto(False, photo)

root.geometry(f'{h}x{w}+200+200')
root.maxsize(800, 800)
root.minsize(600, 600)
root.resizable(True, True)

title_1 = tk.Label(root, text='Daily Tasks',
                   bg='#050D7C',
                   fg='white',
                   font=('Arial', 25, 'bold')
                   )
title_1.place(x=235, y=100)

entry = tk.Entry(root, width=37,
                 bg='#31323A',
                 fg='white',
                 insertbackground='#888995',
                 borderwidth=2,
                 relief='solid',
                 highlightthickness=2,
                 highlightcolor='#6F6F79',

                 )
entry.place(x=132, y=220)

list_title = tk.Text(root, width=45, height=10, state=tk.DISABLED, wrap=tk.WORD)
list_title.place(x=135, y=250)

scrollbar = tk.Scrollbar(root, command=list_title.yview,
                         bg='#6F6F79')
scrollbar.place(x=459, y=250, height=138)

list_title.config(yscrollcommand=scrollbar.set)

btn_add = tk.Button(root, text='Add',
                    command=add_list,
                    width=35,
                    highlightbackground='#050D7C',
                    bg='#050D7C',
                    fg='black',

                    )
btn_add.place(x=130, y=410)

btn_delete = tk.Button(root, text='Delete',
                       command=delete_last,
                       width=35,
                       highlightbackground='#050D7C',
                       bg='#6B74F0',
                       fg='black',
                       )
btn_delete.place(x=130, y=450)


def on_closing():
    conn.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

cursor.execute('SELECT task FROM tasks')
task_list = [row[0] for row in cursor.fetchall()]
update_list_label()

root.mainloop()
