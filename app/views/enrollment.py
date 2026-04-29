import tkinter as tk
from tkinter import messagebox, ttk
from app.services.enrollment_service import EnrollmentService
from app.utils.styles import COLORS, FONTS

class EnrollmentView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.enrollment_service = EnrollmentService()
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
        title_text = "Manage Enrollments" if user.role == "Admin" else "My Enrollments"
        tk.Label(header, text=title_text, font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        tk.Button(header, text="Back to Dashboard", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        list_frame = tk.Frame(content, bg=COLORS["surface"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        if user.role == "Student":
            columns = ("id", "course_id", "course_title", "date")
            self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
            self.tree.heading("id", text="ID")
            self.tree.heading("course_id", text="Course ID")
            self.tree.heading("course_title", text="Course Title")
            self.tree.heading("date", text="Enrollment Date")
            self.tree.pack(fill=tk.BOTH, expand=True)
            self.load_student_enrollments()
        else:
            # For admin, we could have a more complex view (filter by course, enroll students)
            # Keeping it simple: Input Course ID to see enrollments
            top_bar = tk.Frame(list_frame, bg=COLORS["surface"], pady=10)
            top_bar.pack(fill=tk.X)
            tk.Label(top_bar, text="Course ID:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=5)
            self.course_filter_var = tk.StringVar()
            tk.Entry(top_bar, textvariable=self.course_filter_var).pack(side=tk.LEFT, padx=5)
            tk.Button(top_bar, text="View Enrollments", command=self.load_course_enrollments).pack(side=tk.LEFT, padx=5)

            columns = ("id", "student_id", "student_name", "date")
            self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
            self.tree.heading("id", text="Enrollment ID")
            self.tree.heading("student_id", text="Student ID")
            self.tree.heading("student_name", text="Student Name")
            self.tree.heading("date", text="Enrollment Date")
            self.tree.pack(fill=tk.BOTH, expand=True)
            
            # Form for adding enrollment
            form_frame = tk.Frame(content, bg=COLORS["surface"], padx=20, pady=20)
            form_frame.pack(side=tk.RIGHT, fill=tk.Y)

            tk.Label(form_frame, text="Enroll Student", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(0, 20))
            tk.Label(form_frame, text="Student ID", bg=COLORS["surface"]).pack(anchor="w")
            self.student_id_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.student_id_var).pack(pady=(0, 10))

            tk.Label(form_frame, text="Course ID", bg=COLORS["surface"]).pack(anchor="w")
            self.course_id_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.course_id_var).pack(pady=(0, 20))
            
            tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg=COLORS["surface"]).pack(anchor="w")
            self.date_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.date_var).pack(pady=(0, 20))

            tk.Button(form_frame, text="Enroll", command=self.enroll_student, bg=COLORS["success"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)
            
            tk.Button(form_frame, text="Remove Selected", command=self.remove_enrollment, bg=COLORS["error"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)

    def load_student_enrollments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            enrollments = self.enrollment_service.get_enrollments_for_student(self.controller.current_user.id)
            for e in enrollments:
                self.tree.insert("", tk.END, values=(e['enrollment_id'], e['course_id'], e['course_title'], e['date']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_course_enrollments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        course_id = self.course_filter_var.get()
        if not course_id:
            return
        try:
            enrollments = self.enrollment_service.get_enrollments_for_course(course_id)
            for e in enrollments:
                self.tree.insert("", tk.END, values=(e['enrollment_id'], e['student_id'], e['student_name'], e['date']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def enroll_student(self):
        try:
            self.enrollment_service.enroll_student(self.student_id_var.get(), self.course_id_var.get(), self.date_var.get())
            messagebox.showinfo("Success", "Student enrolled successfully")
            self.load_course_enrollments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_enrollment(self):
        selection = self.tree.selection()
        if not selection:
            return messagebox.showwarning("Warning", "Select an enrollment to remove")
        if messagebox.askyesno("Confirm", "Remove this enrollment?"):
            item = self.tree.item(selection[0])
            enrollment_id = item['values'][0]
            try:
                self.enrollment_service.remove_enrollment(enrollment_id)
                messagebox.showinfo("Success", "Enrollment removed")
                self.load_course_enrollments()
            except Exception as e:
                messagebox.showerror("Error", str(e))
