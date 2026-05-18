import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd

# ================= DATABASE =================

conn = sqlite3.connect('resources.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    priority INTEGER,
    resource TEXT,
    progress INTEGER
)
''')

conn.commit()

# ================= FUNCTIONS =================

def add_student():
    name = name_entry.get()
    priority = int(priority_entry.get())
    resource = resource_entry.get()
    progress = int(progress_entry.get())

    cursor.execute('''
    INSERT INTO students(name, priority, resource, progress)
    VALUES (?, ?, ?, ?)
    ''', (name, priority, resource, progress))

    conn.commit()

    messagebox.showinfo("Success", "Student Added Successfully!")

    clear_fields()
    show_students()


def clear_fields():
    name_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    resource_entry.delete(0, tk.END)
    progress_entry.delete(0, tk.END)


def show_students():
    text_area.delete(1.0, tk.END)

    cursor.execute("SELECT * FROM students ORDER BY priority DESC")
    data = cursor.fetchall()

    for row in data:
        text_area.insert(tk.END, f"\nStudent: {row[1]}\n")
        text_area.insert(tk.END, f"Priority: {row[2]}\n")
        text_area.insert(tk.END, f"Allocated Resource: {row[3]}\n")
        text_area.insert(tk.END, f"Progress: {row[4]}%\n")
        text_area.insert(tk.END, "---------------------------\n")


def resource_analysis():
    cursor.execute("SELECT resource FROM students")
    data = cursor.fetchall()

    resources = [row[0] for row in data]

    df = pd.DataFrame(resources, columns=['Resources'])

    result = df['Resources'].value_counts()

    text_area.insert(tk.END, "\nResource Usage Analysis\n\n")
    text_area.insert(tk.END, str(result))


# ================= GUI =================

root = tk.Tk()

root.title("Study Resource Allocator")
root.geometry("850x650")
root.config(bg=\"#f0f0f0\")

heading = tk.Label(
    root,
    text=\"AI-Based Study Resource Allocator\",
    font=(\"Arial\", 20, \"bold\"),
    bg=\"#f0f0f0\",
    fg=\"darkblue\"
)

heading.pack(pady=10)

form_frame = tk.Frame(root, bg=\"#f0f0f0\")
form_frame.pack(pady=10)

labels = [
    \"Student Name\",
    \"Priority Level\",
    \"Allocated Resource\",
    \"Progress %\"
]

entries = []

for i, text in enumerate(labels):
    label = tk.Label(
        form_frame,
        text=text,
        font=(\"Arial\", 12),
        bg=\"#f0f0f0\"
    )

    label.grid(row=i, column=0, padx=10, pady=5)

    entry = tk.Entry(form_frame, width=30)

    entry.grid(row=i, column=1, padx=10, pady=5)

    entries.append(entry)

name_entry = entries[0]
priority_entry = entries[1]
resource_entry = entries[2]
progress_entry = entries[3]

button_frame = tk.Frame(root, bg=\"#f0f0f0\")
button_frame.pack(pady=10)

buttons = [
    (\"Add Student\", add_student),
    (\"Show Students\", show_students),
    (\"Resource Analysis\", resource_analysis)
]

for text, command in buttons:
    btn = tk.Button(
        button_frame,
        text=text,
        command=command,
        width=22,
        bg=\"darkblue\",
        fg=\"white\",
        font=(\"Arial\", 10, \"bold\")
    )

    btn.pack(pady=5)

text_area = tk.Text(root, width=100, height=20)

text_area.pack(pady=20)

root.mainloop()
