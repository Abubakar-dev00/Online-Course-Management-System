import tkinter as tk
from tkinter import messagebox, ttk
from app.services.grading_service import GradingService
from app.utils.styles import COLORS, FONTS

class GradingView(tk.Frame):
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
        tk.Label(header, text="Grade Students", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        tk.Button(header, text="Back to Dashboard", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        list_frame = tk.Frame(content, bg=COLORS["surface"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        top_bar = tk.Frame(list_frame, bg=COLORS["surface"], pady=10)
        top_bar.pack(fill=tk.X)
        tk.Label(top_bar, text="Assignment ID:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=5)
        self.assignment_filter_var = tk.StringVar()
        tk.Entry(top_bar, textvariable=self.assignment_filter_var).pack(side=tk.LEFT, padx=5)
        tk.Button(top_bar, text="View Grades", command=self.load_grades).pack(side=tk.LEFT, padx=5)

        columns = ("id", "student_name", "grade")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="Grade ID")
        self.tree.heading("student_name", text="Student Name")
        self.tree.heading("grade", text="Grade")
        self.tree.pack(fill=tk.BOTH, expand=True)

        form_frame = tk.Frame(content, bg=COLORS["surface"], padx=20, pady=20)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(form_frame, text="Assign/Update Grade", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(0, 20))

        tk.Label(form_frame, text="Student ID", bg=COLORS["surface"]).pack(anchor="w")
        self.student_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.student_id_var).pack(pady=(0, 10))

        tk.Label(form_frame, text="Grade (e.g. A, B+, 90%)", bg=COLORS["surface"]).pack(anchor="w")
        self.grade_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.grade_var).pack(pady=(0, 20))

        tk.Button(form_frame, text="Submit Grade", command=self.submit_grade, bg=COLORS["success"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)
        
        # Adding a progress tracker section below form
        tk.Label(form_frame, text="Update Progress", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(20, 20))
        tk.Label(form_frame, text="Course ID", bg=COLORS["surface"]).pack(anchor="w")
        self.prog_course_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.prog_course_id_var).pack(pady=(0, 10))
        
        tk.Label(form_frame, text="Status", bg=COLORS["surface"]).pack(anchor="w")
        self.prog_status_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=self.prog_status_var, values=["In Progress", "Completed", "Dropped"]).pack(pady=(0, 20))
        
        tk.Button(form_frame, text="Update Progress", command=self.update_progress, bg=COLORS["primary"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)


    def load_grades(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        assignment_id = self.assignment_filter_var.get()
        if not assignment_id:
            return
        try:
            grades = self.grading_service.get_grades_for_assignment(assignment_id)
            for g in grades:
                self.tree.insert("", tk.END, values=(g['id'], g['student_name'], g['grade']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_grade(self):
        assignment_id = self.assignment_filter_var.get()
        if not assignment_id:
            return messagebox.showwarning("Warning", "Please specify an Assignment ID first.")
        try:
            self.grading_service.add_grade(self.student_id_var.get(), assignment_id, self.grade_var.get())
            messagebox.showinfo("Success", "Grade updated")
            self.load_grades()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def update_progress(self):
        student_id = self.student_id_var.get()
        course_id = self.prog_course_id_var.get()
        status = self.prog_status_var.get()
        if not student_id or not course_id or not status:
            return messagebox.showwarning("Warning", "Please provide Student ID, Course ID and Status.")
        try:
            self.grading_service.update_progress(student_id, course_id, status)
            messagebox.showinfo("Success", "Progress updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
