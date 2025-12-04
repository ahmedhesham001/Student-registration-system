import tkinter as tk
from tkinter import ttk
from db_connection import get_db_connection

class ManageEnrollmentsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        tk.Label(self, text="Manage Enrollments", font=("Arial", 24)).pack(pady=20)
        
        # Treeview Frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tree_scroll.config(command=self.tree.yview)
        
        # Define Columns
        self.tree['columns'] = ("ID","Student Name", "Course Code", "Enrollment Date","Grade", "Semester")
        
        # Format Columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Student Name", anchor=tk.W, width=50)
        self.tree.column("Course Code", anchor=tk.W, width=150)
        self.tree.column("Enrollment Date", anchor=tk.W, width=100)
        self.tree.column("Grade", anchor=tk.W, width=50)
        self.tree.column("Semester", anchor=tk.W, width=50)
        
        # Create Headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Student Name", text="Student Name", anchor=tk.W)
        self.tree.heading("Course Code", text="Course Code", anchor=tk.W)
        self.tree.heading("Enrollment Date", text="Enrollment Date", anchor=tk.W)
        self.tree.heading("Grade", text="Grade", anchor=tk.W)
        self.tree.heading("Semester", text="Semester", anchor=tk.W)
        
        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Student ID").grid(row=0, column=2, padx=5)
        self.student_id_entry = tk.Entry(input_frame)
        self.student_id_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Course ID").grid(row=0, column=4, padx=5)
        self.course_id_entry = tk.Entry(input_frame)
        self.course_id_entry.grid(row=0, column=5, padx=5)
        
        tk.Label(input_frame, text="Enrollment Date").grid(row=1, column=2, padx=5, pady=10)
        self.enrollment_date_entry = tk.Entry(input_frame)
        self.enrollment_date_entry.grid(row=1, column=3, padx=5, pady=10)
        
        tk.Label(input_frame, text="Semester").grid(row=1, column=4, padx=5, pady=10)
        self.semester_entry = tk.Entry(input_frame)
        self.semester_entry.grid(row=1, column=5, padx=5, pady=10)
        
        tk.Button(input_frame, text="Add Enrollment", command=self.add_enrollment).grid(row=2, column=2, padx=5, pady=10)
        tk.Button(input_frame, text="Add Grade", command=self.add_grade).grid(row=2, column=3, padx=5, pady=10)
        tk.Button(input_frame, text="Update Enrollment", command=self.update_enrollment).grid(row=2, column=4, padx=5, pady=10)
        tk.Button(input_frame, text="Delete Enrollment", command=self.delete_enrollment).grid(row=2, column=5, padx=5, pady=10)
        
        # Back Button
        tk.Button(self, text="Back", command=self.go_back).pack(pady=0)

    def go_back(self):
        # Clear entries
        self.student_id_entry.delete(0, tk.END)
        self.course_id_entry.delete(0, tk.END)
        self.enrollment_date_entry.delete(0, tk.END)
        
        self.master.show_frame("AdminPage")

    def delete_enrollment(self):
        from tkinter import simpledialog, messagebox
        
        student_id = simpledialog.askstring("Delete Enrollment", "Enter Student ID to delete:")
        
        if not student_id:
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete enrollment with ID {student_id}?")

        if not student_id:
            from tkinter import messagebox
            messagebox.showerror("Error", "Please enter the Student ID to delete enrollment")
            return
            
        from tkinter import messagebox
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete enrollment with ID {student_id}?")
        
        if confirm:
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM enrollments WHERE id = %s", (student_id,))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Enrollment deleted successfully")
                        self.load_data()
                        # Clear entries
                        self.student_id_entry.delete(0, tk.END)
                        self.course_id_entry.delete(0, tk.END)
                        self.enrollment_date_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", "Enrollment ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting enrollment: {e}")
                finally:
                    conn.close()

    def update_enrollment(self):
        from tkinter import simpledialog, messagebox
        
        enrollment_id = simpledialog.askstring("Update Enrollment", "Enter Enrollment ID to update:")
        
        if not enrollment_id:
            return
            
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, course_id, enrollment_date, semester 
            FROM enrollments 
            WHERE id=%s
        """, (enrollment_id,))
        data = cursor.fetchone()

        if not data:
            messagebox.showerror("Error", "Enrollment ID not found")
            conn.close()
            return

        old_student_id, old_course_id, old_enrollment_date, old_semester = data

        # Create custom dialog
        dialog = tk.Toplevel(self)
        dialog.title("Update Enrollment")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text=f"Updating Enrollment ID: {enrollment_id}").pack(pady=10)
        tk.Label(dialog, text="Leave fields empty to keep current value").pack(pady=5)
        
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
        student_id_entry = tk.Entry(input_frame)
        student_id_entry.insert(0, old_student_id)
        student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Course ID").grid(row=1, column=0, padx=5, pady=5)
        course_id_entry = tk.Entry(input_frame)
        course_id_entry.insert(0, old_course_id)
        course_id_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Enrollment Date").grid(row=2, column=0, padx=5, pady=5)
        enrollment_date_entry = tk.Entry(input_frame)
        enrollment_date_entry.insert(0, old_enrollment_date)
        enrollment_date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Semester").grid(row=3, column=0, padx=5, pady=5)
        semester_entry = tk.Entry(input_frame)
        semester_entry.insert(0, old_semester)
        semester_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def submit():
            updates = []
            values = []
            
            if student_id_entry.get():
                updates.append("student_id = %s")
                values.append(student_id_entry.get())
                
            if course_id_entry.get():
                updates.append("course_id = %s")
                values.append(course_id_entry.get())
                
            if enrollment_date_entry.get():
                updates.append("enrollment_date = %s")
                values.append(enrollment_date_entry.get())
                
            if semester_entry.get():
                updates.append("semester = %s")
                values.append(semester_entry.get())
                
            if not updates:
                messagebox.showinfo("Info", "No changes made")
                return
                
            values.append(enrollment_id)
            
            query = f"UPDATE enrollments SET {', '.join(updates)} WHERE id = %s"
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Enrollment updated successfully")
                        self.load_data()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Enrollment ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating enrollment: {e}")
                finally:
                    conn.close()
        
        tk.Button(dialog, text="Update", command=submit).pack(pady=20)

    def add_enrollment(self):
        student_id = self.student_id_entry.get()
        course_id = self.course_id_entry.get()
        enrollment_date = self.enrollment_date_entry.get()
        semester = self.semester_entry.get()
        
        if not (student_id and course_id and enrollment_date and semester):
            from tkinter import messagebox
            messagebox.showerror("Error", "All fields are required")
            return
            
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO enrollments (student_id, course_id, enrollment_date, semester) VALUES (%s, %s, %s, %s)",
                    (student_id, course_id, enrollment_date, semester)
                )
                conn.commit()
                self.load_data()
                
                # Clear entries
                self.student_id_entry.delete(0, tk.END)
                self.course_id_entry.delete(0, tk.END)
                self.enrollment_date_entry.delete(0, tk.END)
                self.semester_entry.delete(0, tk.END)
                
                from tkinter import messagebox
                messagebox.showinfo("Success", "Enrollment added successfully")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Error", f"Error adding enrollment: {e}")
            finally:
                conn.close()
        
        # Load Data
        self.load_data()

    def add_grade(self):
        # Create custom dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add Grade")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Enrollment ID:").pack(pady=5)
        id_entry = tk.Entry(dialog)
        id_entry.pack(pady=5)
        
        tk.Label(dialog, text="Grade (GPA):").pack(pady=5)
        grade_entry = tk.Entry(dialog)
        grade_entry.pack(pady=5)
        
        def submit():
            enrollment_id = id_entry.get()
            grade = grade_entry.get()
            
            if not (enrollment_id and grade):
                from tkinter import messagebox
                messagebox.showerror("Error", "Both fields are required")
                return
                
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE enrollments SET gpa = %s WHERE id = %s", (grade, enrollment_id))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        from tkinter import messagebox
                        messagebox.showinfo("Success", "Grade added successfully")
                        self.load_data()
                        dialog.destroy()
                    else:
                        from tkinter import messagebox
                        messagebox.showerror("Error", "Enrollment ID not found")
                except Exception as e:
                    from tkinter import messagebox
                    messagebox.showerror("Error", f"Error adding grade: {e}")
                finally:
                    conn.close()
        
        tk.Button(dialog, text="Submit", command=submit).pack(pady=10)
    def load_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT e.id, s.first_name, s.last_name, c.code, e.enrollment_date, e.gpa, e.semester FROM enrollments e, students s, courses c WHERE e.student_id = s.id AND e.course_id = c.id")
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=(row[0], row[1] + " " + row[2], row[3], row[4], row[5], row[6]))
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                conn.close()
    
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_data()
