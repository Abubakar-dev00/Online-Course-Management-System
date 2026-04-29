import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import AuthService
from app.utils.styles import COLORS, FONTS, PAD

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.auth_service = AuthService()
        self.configure(bg=COLORS["background"])
        
        self._create_widgets()

    def _create_widgets(self):
        # Center container
        container = tk.Frame(self, bg=COLORS["surface"], padx=40, pady=40)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="Login", font=FONTS["h1"], bg=COLORS["surface"], fg=COLORS["primary"]).pack(pady=(0, 20))

        # Username
        tk.Label(container, text="Username", font=FONTS["body"], bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w")
        self.username_var = tk.StringVar()
        tk.Entry(container, textvariable=self.username_var, font=FONTS["body"], width=30).pack(pady=(0, 10))

        # Password
        tk.Label(container, text="Password", font=FONTS["body"], bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w")
        self.password_var = tk.StringVar()
        tk.Entry(container, textvariable=self.password_var, show="*", font=FONTS["body"], width=30).pack(pady=(0, 20))

        # Login button
        btn = tk.Button(container, text="Log In", font=FONTS["button"], bg=COLORS["primary"], fg=COLORS["text_light"], 
                        command=self.handle_login, width=25, relief=tk.FLAT)
        btn.pack(pady=PAD["medium"])

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        try:
            user = self.auth_service.login(username, password)
            if user:
                self.controller.current_user = user
                self.controller.show_frame("DashboardView")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
