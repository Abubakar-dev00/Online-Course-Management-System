import tkinter as tk
from tkinter import messagebox, ttk
from app.services.assignment_service import AssignmentService
from app.utils.styles import COLORS, FONTS

class AssignmentView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.assignment_service = AssignmentService()
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
        tk.Label(header, text="Manage Assignments", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        tk.Button(header, text="Back to Dashboard", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        list_frame = tk.Frame(content, bg=COLORS["surface"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        top_bar = tk.Frame(list_frame, bg=COLORS["surface"], pady=10)
        top_bar.pack(fill=tk.X)
        tk.Label(top_bar, text="Course ID:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=5)
        self.course_filter_var = tk.StringVar()
        tk.Entry(top_bar, textvariable=self.course_filter_var).pack(side=tk.LEFT, padx=5)
        tk.Button(top_bar, text="View Assignments", command=self.load_assignments).pack(side=tk.LEFT, padx=5)

        columns = ("id", "title", "due_date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("due_date", text="Due Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        if user.role in ["Teacher", "Admin"]:
            form_frame = tk.Frame(content, bg=COLORS["surface"], padx=20, pady=20)
            form_frame.pack(side=tk.RIGHT, fill=tk.Y)

            tk.Label(form_frame, text="Add/Edit Assignment", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(0, 20))

            tk.Label(form_frame, text="Title", bg=COLORS["surface"]).pack(anchor="w")
            self.title_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.title_var).pack(pady=(0, 10))

            tk.Label(form_frame, text="Due Date (YYYY-MM-DD)", bg=COLORS["surface"]).pack(anchor="w")
            self.due_date_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.due_date_var).pack(pady=(0, 20))

            tk.Button(form_frame, text="Add Assignment", command=self.add_assignment, bg=COLORS["success"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)
            tk.Button(form_frame, text="Delete Selected", command=self.delete_assignment, bg=COLORS["error"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)

    def load_assignments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        course_id = self.course_filter_var.get()
        if not course_id:
            return
        try:
            assignments = self.assignment_service.get_assignments(course_id)
            for a in assignments:
                self.tree.insert("", tk.END, values=(a['id'], a['title'], a['due_date']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_assignment(self):
        course_id = self.course_filter_var.get()
        if not course_id:
            return messagebox.showwarning("Warning", "Please specify a Course ID first to add an assignment.")
        try:
            self.assignment_service.add_assignment(course_id, self.title_var.get(), self.due_date_var.get())
            messagebox.showinfo("Success", "Assignment added")
            self.load_assignments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_assignment(self):
        selection = self.tree.selection()
        if not selection:
            return messagebox.showwarning("Warning", "Select an assignment to delete")
        if messagebox.askyesno("Confirm", "Delete this assignment?"):
            item = self.tree.item(selection[0])
            assignment_id = item['values'][0]
            try:
                self.assignment_service.delete_assignment(assignment_id)
                messagebox.showinfo("Success", "Assignment deleted")
                self.load_assignments()
            except Exception as e:
                messagebox.showerror("Error", str(e))
