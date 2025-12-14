import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

DB_FILE = "automation_backlog.db"

# ---------------- Backlog Utilities (SQLite) ----------------

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS backlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            frequency TEXT,
            score INTEGER,
            decision TEXT,
            interfaces TEXT,
            timestamp TEXT,
            status TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_to_backlog(entry):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO backlog (task, frequency, score, decision, interfaces, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry["task"],
            entry["frequency"],
            entry["score"],
            entry["decision"],
            ",".join(entry["interfaces"]),
            entry["timestamp"],
            entry["status"],
        ),
    )
    conn.commit()
    conn.close()


# ---------------- Decision Logic ----------------

def compute_decision(score):
    if score >= 4:
        return "Automate Now"
    elif score >= 2:
        return "Semi-Automate"
    return "Defer"


class ExplorerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Automation Backlog")
        self.geometry("720x400")

        self.tree = ttk.Treeview(self, columns=("task", "decision", "score", "frequency", "timestamp"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT task, decision, score, frequency, timestamp FROM backlog ORDER BY id DESC")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------------- GUI App ----------------

class AutomationTriageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automation Task Triage")
        self.geometry("500x600")
        self.resizable(False, False)

        self.task_name = tk.StringVar()
        self.frequency = tk.StringVar(value="Daily")
        self.score_vars = []
        self.interface_vars = {}

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Task Name").pack(anchor="w", padx=20, pady=(15, 0))
        ttk.Entry(self, textvariable=self.task_name).pack(fill="x", padx=20)

        ttk.Label(self, text="Frequency").pack(anchor="w", padx=20, pady=(15, 0))
        ttk.Combobox(self, textvariable=self.frequency,
                     values=["Daily", "Weekly", "Monthly", "Ad-hoc"], state="readonly").pack(fill="x", padx=20)

        ttk.Label(self, text="Automation Feasibility").pack(anchor="w", padx=20, pady=(20, 5))

        questions = [
            "Is the task repetitive?",
            "Are inputs structured?",
            "Is the output predictable?",
            "Can rules be clearly defined?",
            "Low human judgment required?"
        ]

        for q in questions:
            var = tk.IntVar()
            ttk.Checkbutton(self, text=q, variable=var).pack(anchor="w", padx=40)
            self.score_vars.append(var)

        ttk.Label(self, text="Interfaces Involved").pack(anchor="w", padx=20, pady=(20, 5))

        interfaces = ["File", "API", "Email", "Database", "Web UI"]
        for i in interfaces:
            var = tk.BooleanVar()
            ttk.Checkbutton(self, text=i, variable=var).pack(anchor="w", padx=40)
            self.interface_vars[i] = var

        ttk.Button(self, text="Evaluate & Save", command=self.evaluate).pack(pady=(20, 10))
        ttk.Button(self, text="Explore Backlog", command=self.open_explorer).pack()

    def open_explorer(self):
        ExplorerWindow(self)

    def evaluate(self):
        if not self.task_name.get().strip():
            messagebox.showerror("Error", "Task name is required")
            return

        score = sum(v.get() for v in self.score_vars)
        decision = compute_decision(score)
        interfaces = [k for k, v in self.interface_vars.items() if v.get()]

        entry = {
            "task": self.task_name.get(),
            "frequency": self.frequency.get(),
            "score": score,
            "decision": decision,
            "interfaces": interfaces,
            "timestamp": datetime.now().isoformat(),
            "status": "new"
        }

        save_to_backlog(entry)

        messagebox.showinfo("Result",
                            f"Decision: {decision}\nScore: {score}\nSaved to backlog")
        self.reset()

    def reset(self):
        self.task_name.set("")
        self.frequency.set("Daily")
        for v in self.score_vars:
            v.set(0)
        for v in self.interface_vars.values():
            v.set(False)

init_db()

if __name__ == "__main__":
    app = AutomationTriageApp()
    app.mainloop()
