import tkinter as tk
from admin import AdminPage
from login import LoginPage
from manage_students import ManageStudentsPage
from manage_courses import ManageCoursesPage
from manage_enrollments import ManageEnrollmentsPage

class App(tk.Tk):
    def __init__(self):
        Pages = [AdminPage, LoginPage, ManageStudentsPage, ManageCoursesPage, ManageEnrollmentsPage]
        super().__init__()
        self.title('Registration System')
        self.geometry('800x800')
        self.frames = {}
        for Page in Pages:
            frame = Page(self)
            self.frames[Page.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == '__main__':
    App().mainloop()

