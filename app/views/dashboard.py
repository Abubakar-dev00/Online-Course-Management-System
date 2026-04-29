import tkinter as tk
from app.utils.styles import COLORS, FONTS, PAD

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["background"])
        
        # We'll create widgets when the frame is shown because it depends on the logged-in user
        
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh()

    def refresh(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        if not user:
            return

        # Header
        header = tk.Frame(self, bg=COLORS["primary"], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"Welcome, {user.username} ({user.role})", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Button(header, text="Logout", font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], command=self.logout).pack(side=tk.RIGHT, padx=20, pady=15)

        # Content area
        content = tk.Frame(self, bg=COLORS["background"])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Build menu based on role
        if user.role == "Admin":
            self.create_menu_button(content, "Manage Courses", "CourseView")
            self.create_menu_button(content, "Manage Enrollments", "EnrollmentView")
        elif user.role == "Teacher":
            self.create_menu_button(content, "My Courses", "CourseView")
            self.create_menu_button(content, "Manage Assignments", "AssignmentView")
            self.create_menu_button(content, "Grade Students", "GradingView")
            self.create_menu_button(content, "Announcements", "AnnouncementsView")
        elif user.role == "Student":
            self.create_menu_button(content, "My Enrollments", "EnrollmentView")
            self.create_menu_button(content, "My Progress", "ProgressView")
            self.create_menu_button(content, "Announcements", "AnnouncementsView")

    def create_menu_button(self, parent, text, view_name):
        btn = tk.Button(parent, text=text, font=FONTS["h2"], bg=COLORS["surface"], fg=COLORS["primary"], 
                        command=lambda: self.controller.show_frame(view_name), width=20, height=2, relief=tk.RAISED)
        btn.pack(pady=10)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")
