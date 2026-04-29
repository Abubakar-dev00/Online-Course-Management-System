import tkinter as tk
from tkinter import messagebox, ttk
from app.utils.db import get_db_connection
from app.utils.logger import get_logger
from app.utils.styles import COLORS, FONTS
import datetime

logger = get_logger("announcements_view")

class AnnouncementsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
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
        tk.Label(header, text="Announcements", font=FONTS["h2"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)
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
        tk.Button(top_bar, text="View Announcements", command=self.load_announcements).pack(side=tk.LEFT, padx=5)

        columns = ("id", "date", "message")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("message", text="Message")
        self.tree.pack(fill=tk.BOTH, expand=True)

        if user.role in ["Teacher", "Admin"]:
            form_frame = tk.Frame(content, bg=COLORS["surface"], padx=20, pady=20)
            form_frame.pack(side=tk.RIGHT, fill=tk.Y)

            tk.Label(form_frame, text="Post Announcement", font=FONTS["h2"], bg=COLORS["surface"]).pack(pady=(0, 20))

            tk.Label(form_frame, text="Message", bg=COLORS["surface"]).pack(anchor="w")
            self.message_text = tk.Text(form_frame, width=30, height=5)
            self.message_text.pack(pady=(0, 20))

            tk.Button(form_frame, text="Post", command=self.post_announcement, bg=COLORS["success"], fg=COLORS["text_light"]).pack(fill=tk.X, pady=5)

    def load_announcements(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        course_id = self.course_filter_var.get()
        if not course_id:
            return
        conn = get_db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM announcements WHERE course_id = %s ORDER BY date DESC", (course_id,))
            for a in cursor.fetchall():
                self.tree.insert("", tk.END, values=(a['id'], a['date'], a['message']))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()

    def post_announcement(self):
        course_id = self.course_filter_var.get()
        message = self.message_text.get('1.0', tk.END).strip()
        if not course_id or not message:
            return messagebox.showwarning("Warning", "Please specify a Course ID and Message.")
        
        conn = get_db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            
            # Check if course exists
            cursor.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"Course with ID {course_id} does not exist.")
                return

            date = datetime.date.today().isoformat()
            cursor.execute("INSERT INTO announcements (course_id, message, date) VALUES (%s, %s, %s)", (course_id, message, date))
            conn.commit()
            messagebox.showinfo("Success", "Announcement posted.")
            self.message_text.delete('1.0', tk.END)
            self.load_announcements()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
