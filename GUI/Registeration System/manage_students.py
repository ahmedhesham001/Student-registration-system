import tkinter as tk
from tkinter import ttk
from db_connection import get_db_connection

class ManageStudentsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        tk.Label(self, text="Manage Students", font=("Arial", 24)).pack(pady=20)
        
        # Search Frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_students).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_data).pack(side=tk.LEFT, padx=5)
        
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
        self.tree['columns'] = ("ID", "Name", "Phone", "Email", "Academic Year", "Department")
        
        # Format Columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Name", anchor=tk.W, width=150)
        self.tree.column("Phone", anchor=tk.W, width=100)
        self.tree.column("Email", anchor=tk.W, width=200)
        self.tree.column("Academic Year", anchor=tk.W, width=100)
        self.tree.column("Department", anchor=tk.W, width=100)
        
        # Create Headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Phone", text="Phone", anchor=tk.W)
        self.tree.heading("Email", text="Email", anchor=tk.W)
        self.tree.heading("Academic Year", text="Academic Year", anchor=tk.W)
        self.tree.heading("Department", text="Department", anchor=tk.W)
        
        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Phone").grid(row=0, column=2, padx=5)
        self.phone_entry = tk.Entry(input_frame)
        self.phone_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Email").grid(row=1, column=0, padx=5, pady=10)
        self.email_entry = tk.Entry(input_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=10)
        
        tk.Label(input_frame, text="Academic Year").grid(row=1, column=2, padx=5, pady=10)
        self.academic_year_entry = tk.Entry(input_frame)
        self.academic_year_entry.grid(row=1, column=3, padx=5, pady=10)
        
        tk.Label(input_frame, text="Department").grid(row=0, column=4, padx=5, pady=10)
        self.department_entry = tk.Entry(input_frame)
        self.department_entry.grid(row=0, column=5, padx=5, pady=10)
        
        tk.Button(input_frame, text="Add Student", command=self.add_student).grid(row=2, column=2, padx=5, pady=10)
        tk.Button(input_frame, text="Update Student", command=self.update_student).grid(row=2, column=3, padx=5, pady=10)
        tk.Button(input_frame, text="Delete Student", command=self.delete_student).grid(row=2, column=4, padx=5, pady=10)
        
        # Back Button
        tk.Button(self, text="Back", command=self.go_back).pack(pady=0)

    def go_back(self):
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.academic_year_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        
        self.master.show_frame("AdminPage")

    def delete_student(self):
        from tkinter import simpledialog, messagebox
        
        student_id = simpledialog.askstring("Delete Student", "Enter Student ID to delete:")
        
        if not student_id:
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with ID {student_id}?")
        
        if confirm:
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Student deleted successfully")
                        self.load_data()
                        # Clear entries
                        self.name_entry.delete(0, tk.END)
                        self.phone_entry.delete(0, tk.END)
                        self.email_entry.delete(0, tk.END)
                        self.academic_year_entry.delete(0, tk.END)
                        self.department_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", "Student ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting student: {e}")
                finally:
                    conn.close()

    def update_student(self):
        from tkinter import simpledialog, messagebox
        
        student_id = simpledialog.askstring("Update Student", "Enter Student ID to update:")
        
        if not student_id:
            return
            
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT first_name, last_name, phone, email, academic_year, department_id 
        FROM students 
        WHERE id=%s
        """, (student_id,))
        data = cursor.fetchone()

        if not data:
            messagebox.showerror("Error", "Student ID not found")
            conn.close()
        
        old_first, old_last, old_phone, old_email, old_year, old_dept = data

        # Create custom dialog
        dialog = tk.Toplevel(self)
        dialog.title("Update Student")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text=f"Updating Student ID: {student_id}").pack(pady=10)
        tk.Label(dialog, text="Leave fields empty to keep current value").pack(pady=5)
        
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(input_frame)
        name_entry.insert(0, old_first + " " + old_last)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Phone").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(input_frame)
        phone_entry.insert(0, old_phone)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Email").grid(row=2, column=0, padx=5, pady=5)
        email_entry = tk.Entry(input_frame)
        email_entry.insert(0, old_email)
        email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Academic Year").grid(row=3, column=0, padx=5, pady=5)
        academic_year_entry = tk.Entry(input_frame)
        academic_year_entry.insert(0, old_year)
        academic_year_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Department ID").grid(row=4, column=0, padx=5, pady=5)
        department_entry = tk.Entry(input_frame)
        department_entry.insert(0, old_dept)
        department_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def submit():
            updates = []
            values = []
            
            name = name_entry.get()
            if name:
                name_parts = name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""
                updates.append("first_name = %s")
                values.append(first_name)
                updates.append("last_name = %s")
                values.append(last_name)
                
            if phone_entry.get():
                updates.append("phone = %s")
                values.append(phone_entry.get())
                
            if email_entry.get():
                updates.append("email = %s")
                values.append(email_entry.get())
                
            if academic_year_entry.get():
                updates.append("academic_year = %s")
                values.append(academic_year_entry.get())
                
            if department_entry.get():
                updates.append("department_id = %s")
                values.append(department_entry.get())
                
            if not updates:
                messagebox.showinfo("Info", "No changes made")
                return
                
            values.append(student_id)
            
            query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Student updated successfully")
                        self.load_data()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Student ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating student: {e}")
                finally:
                    conn.close()
        
        tk.Button(dialog, text="Update", command=submit).pack(pady=20)

    def add_student(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        academic_year = self.academic_year_entry.get()
        department = self.department_entry.get()
        
        if not (name and phone and email and academic_year and department):
            from tkinter import messagebox
            messagebox.showerror("Error", "All fields are required")
            return
            
        # Split name into first and last name for the database
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (first_name, last_name, phone, email, academic_year, department_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, phone, email, academic_year, department)
                )
                conn.commit()
                self.load_data()
                
                # Clear entries
                self.name_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.academic_year_entry.delete(0, tk.END)
                self.department_entry.delete(0, tk.END)
                
                from tkinter import messagebox
                messagebox.showinfo("Success", "Student added successfully")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Error", f"Error adding student: {e}")
            finally:
                conn.close()
        
        # Load Data
        self.load_data()

    def search_students(self):
        query = self.search_entry.get()
        self.load_data(query)
        self.search_entry.delete(0, tk.END)

    def load_data(self, search_query=None):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if search_query:
                    query = """
                        SELECT s.id, s.first_name, s.last_name, s.phone, s.email, s.academic_year, d.name 
                        FROM students s 
                        JOIN departments d ON s.department_id = d.id 
                        WHERE s.id LIKE %s
                    """
                    cursor.execute(query, (f"%{search_query}%",))
                else:
                    cursor.execute("SELECT s.id, s.first_name, s.last_name, s.phone, s.email, s.academic_year, d.name FROM students s JOIN departments d ON s.department_id = d.id")
                
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=(row[0], row[1]+" "+row[2], row[3], row[4], row[5], row[6]))
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                conn.close()
    
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_data()
