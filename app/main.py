import tkinter as tk
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.views.course import CourseView
from app.views.enrollment import EnrollmentView
from app.views.assignment import AssignmentView
from app.views.progress import ProgressView
from app.views.grading import GradingView
from app.views.announcements import AnnouncementsView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Course Management System")
        self.geometry("800x600")
        self.current_user = None

        # Container for all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Store view classes for lazy loading
        self.view_classes = {
            "LoginView": LoginView,
            "DashboardView": DashboardView,
            "CourseView": CourseView,
            "EnrollmentView": EnrollmentView,
            "AssignmentView": AssignmentView,
            "ProgressView": ProgressView,
            "GradingView": GradingView,
            "AnnouncementsView": AnnouncementsView
        }

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        # Lazy loading implementation
        if page_name not in self.frames:
            if page_name in self.view_classes:
                # Instantiate the frame on demand
                F = self.view_classes[page_name]
                frame = F(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                print(f"View {page_name} not found.")
                return
        
        frame = self.frames[page_name]
        frame.tkraise()

    def add_frame(self, frame_class):
        page_name = frame_class.__name__
        if page_name not in self.frames:
            frame = frame_class(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
