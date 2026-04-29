import tkinter as tk
from tkinter import messagebox, ttk
from app.services.course_service import CourseService
from app.utils.styles import COLORS, FONTS

class CourseView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.course_service = CourseService()
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
        tk.Label(header, text="Manage Courses" if user.role == "Admin" else "My Courses", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        tk.Button(header, text="Back to Dashboard", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # List of courses
        list_frame = tk.Frame(content, bg=COLORS["surface"])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        columns = ("id", "title", "teacher_id")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("teacher_id", text="Teacher ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.load_courses()

        # Form for Add/Update (Only Admins can add/edit/delete courses in this basic setup)
        if user.role == "Admin":
            form_frame = tk.Frame(content, bg=COLORS["surface"], padx=20, pady=20)
            form_frame.pack(side=tk.RIGHT, fill=tk.Y)

            tk.Label(form_frame, text="Course Details", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(0, 20))

            tk.Label(form_frame, text="Title", bg=COLORS["surface"]).pack(anchor="w")
            self.title_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.title_var, width=30).pack(pady=(0, 10))

            tk.Label(form_frame, text="Description", bg=COLORS["surface"]).pack(anchor="w")
            self.desc_text = tk.Text(form_frame, width=30, height=5)
            self.desc_text.pack(pady=(0, 10))

            tk.Label(form_frame, text="Teacher ID", bg=COLORS["surface"]).pack(anchor="w")
            self.teacher_id_var = tk.StringVar()
            tk.Entry(form_frame, textvariable=self.teacher_id_var, width=30).pack(pady=(0, 20))

            btn_frame = tk.Frame(form_frame, bg=COLORS["surface"])
            btn_frame.pack(fill=tk.X)

            tk.Button(btn_frame, text="Add", command=self.add_course, bg=COLORS["success"], fg=COLORS["text_light"]).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            tk.Button(btn_frame, text="Update", command=self.update_course, bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            tk.Button(btn_frame, text="Delete", command=self.delete_course, bg=COLORS["error"], fg=COLORS["text_light"]).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            tk.Button(btn_frame, text="Clear", command=self.clear_form, bg=COLORS["secondary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

            self.selected_course_id = None

    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            courses = self.course_service.get_all_courses()
            user = self.controller.current_user
            for c in courses:
                if user.role == "Admin" or (user.role == "Teacher" and str(c.teacher_id) == str(user.id)):
                    self.tree.insert("", tk.END, values=(c.id, c.title, c.teacher_id))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(self, event):
        if self.controller.current_user.role != "Admin":
            return
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.selected_course_id = values[0]
            self.title_var.set(values[1])
            self.teacher_id_var.set(values[2])
            # For a full implementation, we'd also fetch description from DB or store it in treeview invisibly.
            # Simplified here for brevity.

    def clear_form(self):
        self.selected_course_id = None
        self.title_var.set("")
        self.teacher_id_var.set("")
        self.desc_text.delete('1.0', tk.END)

    def add_course(self):
        try:
            self.course_service.add_course(self.title_var.get(), self.desc_text.get('1.0', tk.END).strip(), self.teacher_id_var.get() or None)
            messagebox.showinfo("Success", "Course added successfully")
            self.clear_form()
            self.load_courses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_course(self):
        if not self.selected_course_id:
            return messagebox.showwarning("Warning", "Select a course to update")
        try:
            self.course_service.update_course(self.selected_course_id, self.title_var.get(), self.desc_text.get('1.0', tk.END).strip(), self.teacher_id_var.get() or None)
            messagebox.showinfo("Success", "Course updated successfully")
            self.clear_form()
            self.load_courses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_course(self):
        if not self.selected_course_id:
            return messagebox.showwarning("Warning", "Select a course to delete")
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            try:
                self.course_service.delete_course(self.selected_course_id)
                messagebox.showinfo("Success", "Course deleted successfully")
                self.clear_form()
                self.load_courses()
            except Exception as e:
                messagebox.showerror("Error", str(e))
