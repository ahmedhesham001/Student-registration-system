import tkinter as tk
from tkinter import messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent):
        
        super().__init__(parent)
        tk.Label(self, text="Login Page", font=("arial", 18, "bold")).pack(pady=20)
        self.userEntry = tk.Entry(self, width=25)
        self.passEntry = tk.Entry(self, width=25, show="*")
        self.userLabel = tk.Label(self, text="Username:")
        self.passLabel = tk.Label(self, text="Password:")
        self.userLabel.pack()
        self.userEntry.pack(pady=5)
        self.passLabel.pack()
        self.passEntry.pack(pady=5)
        self.userEntry.focus()
        self.userEntry.focus_set()
        
        self.userEntry.bind('<Return>', self.validate_login)
        self.passEntry.bind('<Return>', self.validate_login)
        tk.Button(
            self,
            text="Login",
            command=self.validate_login
        ).pack(pady=10)

    def validate_login(self, event=None):
        username = self.userEntry.get()
        password = self.passEntry.get()

        if username == "admin" and password == "admin123":
            self.master.show_frame("AdminPage")
        else:
            messagebox.showerror("Invalid Login", "Invalid username or password")

        self.userEntry.delete(0, tk.END)
        self.passEntry.delete(0, tk.END)
        self.userEntry.focus()
            
