import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class Task:
    def __init__(self, description, priority='Medium', due_date=None, category=None, status='Pending'):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.status = status
        self.created_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at
        }

class ToDoList:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            priority TEXT,
            due_date TEXT,
            category TEXT,
            status TEXT,
            created_at TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, task):
        query = """
        INSERT INTO tasks (description, priority, due_date, category, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (
            task.description, task.priority, task.due_date, task.category, task.status, task.created_at
        ))
        self.conn.commit()

    def update_task(self, task_id, **kwargs):
        columns = ', '.join(f"{key} = ?" for key in kwargs)
        query = f"UPDATE tasks SET {columns} WHERE id = ?"
        self.conn.execute(query, (*kwargs.values(), task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()

    def get_tasks(self, filter_by=None):
        query = "SELECT * FROM tasks"
        if filter_by:
            conditions = " AND ".join(f"{key} = ?" for key in filter_by)
            query += f" WHERE {conditions}"
            result = self.conn.execute(query, tuple(filter_by.values()))
        else:
            result = self.conn.execute(query)
        return result.fetchall()

    def get_task_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE id = ?"
        result = self.conn.execute(query, (task_id,))
        return result.fetchone()

    def close(self):
        self.conn.close()

def add_task():
    task_description = entry_description.get()
    due_date = entry_due_date.get()
    category = entry_category.get()
    priority = priority_combobox.get()

    if task_description:
        task = Task(
            description=task_description,
            priority=priority,
            due_date=due_date,
            category=category
        )
        todo_list.add_task(task)
        update_listbox()
        entry_description.delete(0, tk.END)
        entry_due_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task description cannot be empty!")

def delete_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        task_id = listbox.get(selected_task_index).split(' - ')[0]
        todo_list.delete_task(int(task_id))
        update_listbox()
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

def mark_as_done():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        task_id = listbox.get(selected_task_index).split(' - ')[0]
        todo_list.update_task(int(task_id), status='Completed')
        update_listbox()
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

def show_task_details():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        task_id = listbox.get(selected_task_index).split(' - ')[0]
        task = todo_list.get_task_by_id(int(task_id))
        if task:
            details = (
                f"Description: {task[1]}\n"
                f"Priority: {task[2]}\n"
                f"Due Date: {task[3] if task[3] else 'N/A'}\n"
                f"Category: {task[4]}\n"
                f"Status: {task[5]}\n"
                f"Created At: {task[6]}"
            )
            messagebox.showinfo("Task Details", details)
        else:
            messagebox.showwarning("Error", "Task not found!")
    else:
        messagebox.showwarning("Selection Error", "No task selected!")

def update_listbox(status=None):
    listbox.delete(0, tk.END)
    filter_by = {'status': status} if status else None
    tasks = todo_list.get_tasks(filter_by=filter_by)
    for task in tasks:
        task_display = (
            f"{task[0]} - {task[1]} - {task[2]} - "
            f"{task[3] if task[3] else 'N/A'} - "
            f"{task[4]} - {task[5]} - {task[6]}"
        )
        listbox.insert(tk.END, task_display)

def show_pending():
    update_listbox('Pending')

def show_completed():
    update_listbox('Completed')

root = tk.Tk()
root.title("To-Do List")

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

input_frame = tk.Frame(main_frame)
input_frame.pack()

tk.Label(input_frame, text="Description:").pack(side=tk.LEFT, padx=5)
entry_description = tk.Entry(input_frame, width=50)
entry_description.pack(side=tk.LEFT, padx=10)

tk.Label(input_frame, text="Priority:").pack(side=tk.LEFT, padx=5)
priority_combobox = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], width=10, state="readonly")
priority_combobox.set("Medium")
priority_combobox.pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Due Date (dd-mm-yyyy):").pack(side=tk.LEFT, padx=5)
entry_due_date = tk.Entry(input_frame, width=15)
entry_due_date.pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Category:").pack(side=tk.LEFT, padx=5)
entry_category = tk.Entry(input_frame, width=15)
entry_category.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

tab_frame = tk.Frame(main_frame)
tab_frame.pack(pady=10)

pending_button = tk.Button(tab_frame, text="Show Pending", command=show_pending)
pending_button.pack(side=tk.LEFT, padx=5)

completed_button = tk.Button(tab_frame, text="Show Completed", command=show_completed)
completed_button.pack(side=tk.LEFT, padx=5)

listbox = tk.Listbox(root, height=15, width=100)
listbox.pack(pady=10)

action_frame = tk.Frame(root)
action_frame.pack(pady=5)

delete_button = tk.Button(action_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

mark_done_button = tk.Button(action_frame, text="Mark as Done", command=mark_as_done)
mark_done_button.pack(side=tk.LEFT, padx=5)

show_details_button = tk.Button(action_frame, text="Show Details", command=show_task_details)
show_details_button.pack(side=tk.LEFT, padx=5)

todo_list = ToDoList()
update_listbox('Pending')

root.mainloop()

todo_list.close()