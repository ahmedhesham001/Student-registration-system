import tkinter as tk
from tkinter import messagebox

class AdminPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Welcome Admin!", font=("Arial", 24)).pack(pady=20)
        
        tk.Button(self, text="Manage Students", command=lambda: self.master.show_frame("ManageStudentsPage")).pack(pady=10)
        tk.Button(self, text="Manage Courses", command=lambda: self.master.show_frame("ManageCoursesPage")).pack(pady=10)
        tk.Button(self, text="Manage Enrollment", command=lambda: self.master.show_frame("ManageEnrollmentsPage")).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=20)

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if confirm:
            self.master.show_frame("LoginPage")