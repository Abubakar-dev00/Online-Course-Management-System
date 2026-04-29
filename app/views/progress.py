import tkinter as tk
from tkinter import messagebox, ttk
from app.services.grading_service import GradingService
from app.utils.styles import COLORS, FONTS

class ProgressView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grading_service = GradingService()
        self.configure(bg=COLORS["background"])

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        if not user:
            return

        header = tk.Frame(self, bg=COLORS["primary"], height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="My Progress", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        tk.Button(header, text="Back to Dashboard", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        columns = ("id", "course_title", "status")
        self.tree = ttk.Treeview(content, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("course_title", text="Course Title")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_progress()

    def load_progress(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            # Assumes student user ID maps to student ID 1:1 for simplicity in this demo, 
            # ideally would need to fetch actual student.id by user.id
            conn = __import__("app.utils.db").utils.db.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM students WHERE user_id = %s", (self.controller.current_user.id,))
            student_id = cursor.fetchone()
            if student_id:
                progress_records = self.grading_service.get_progress(student_id[0])
                for p in progress_records:
                    self.tree.insert("", tk.END, values=(p['id'], p['course_title'], p['status']))
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
