import tkinter as tk
from tkinter import ttk
from db_connection import get_db_connection

class ManageCoursesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        tk.Label(self, text="Manage Courses", font=("Arial", 24)).pack(pady=20)
        
        # Search Frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_courses).pack(side=tk.LEFT, padx=5)
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
        self.tree['columns'] = ("ID", "Code", "Name", "Credit", "Instructor ID")
        
        # Format Columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Code", anchor=tk.W, width=70)
        self.tree.column("Name", anchor=tk.W, width=180)
        self.tree.column("Credit", anchor=tk.W, width=50)
        self.tree.column("Instructor ID", anchor=tk.W, width=200)
        
        # Create Headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Code", text="Code", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Credit", text="Credit", anchor=tk.W)
        self.tree.heading("Instructor ID", text="Instructor ID", anchor=tk.W)
        
        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=20)
                
        tk.Label(input_frame, text="Code").grid(row=0, column=1, padx=5)
        self.code_entry = tk.Entry(input_frame)
        self.code_entry.grid(row=0, column=2, padx=5)
        
        tk.Label(input_frame, text="Name").grid(row=0, column=3, padx=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=4, padx=5)
        
        tk.Label(input_frame, text="Credit").grid(row=1, column=1, padx=5, pady=10)
        self.credit_entry = tk.Entry(input_frame)
        self.credit_entry.grid(row=1, column=2, padx=5, pady=10)
        
        tk.Label(input_frame, text="Instructor ID").grid(row=1, column=3, padx=5, pady=10)
        self.instructor_id_entry = tk.Entry(input_frame)
        self.instructor_id_entry.grid(row=1, column=4, padx=5, pady=10)
        
        tk.Button(input_frame, text="Add Course", command=self.add_course).grid(row=2, column=2, padx=5, pady=10)
        tk.Button(input_frame, text="Update Course", command=self.update_course).grid(row=2, column=3, padx=5, pady=10)
        tk.Button(input_frame, text="Delete Course", command=self.delete_course).grid(row=2, column=4, padx=5, pady=10)
        
        # Back Button
        tk.Button(self, text="Back", command=self.go_back).pack(pady=10)

    def go_back(self):
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.credit_entry.delete(0, tk.END)
        self.instructor_id_entry.delete(0, tk.END)
        
        self.master.show_frame("AdminPage")

    def delete_course(self):
        
        from tkinter import simpledialog, messagebox
        
        course_id = simpledialog.askstring("Delete Course", "Enter Course ID to delete:")
        
        if not course_id:
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete course with ID {course_id}?")
        
        if confirm:
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Course deleted successfully")
                        self.load_data()
                        # Clear entries
                        self.name_entry.delete(0, tk.END)
                        self.code_entry.delete(0, tk.END)
                        self.credit_entry.delete(0, tk.END)
                        self.instructor_id_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", "Course ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting course: {e}")
                finally:
                    conn.close()

    def update_course(self):
        from tkinter import simpledialog, messagebox
        
        course_id = simpledialog.askstring("Update Course", "Enter Course ID to update:")
        
        if not course_id:
            return
            
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, code, credit, instructor_id 
            FROM courses 
            WHERE id=%s
        """, (course_id,))
        data = cursor.fetchone()

        if not data:
            messagebox.showerror("Error", "Course ID not found")
            conn.close()
            return

        old_id, old_name, old_code, old_credit, old_instructor_id = data

        # Create custom dialog
        dialog = tk.Toplevel(self)
        dialog.title("Update Course")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text=f"Updating Course ID: {course_id}").pack(pady=10)
        tk.Label(dialog, text="Leave fields empty to keep current value").pack(pady=5)
        
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(input_frame)
        name_entry.insert(0, old_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Code").grid(row=1, column=0, padx=5, pady=5)
        code_entry = tk.Entry(input_frame)
        code_entry.insert(0, old_code)
        code_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Credit").grid(row=2, column=0, padx=5, pady=5)
        credit_entry = tk.Entry(input_frame)
        credit_entry.insert(0, old_credit)
        credit_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Instructor ID").grid(row=3, column=0, padx=5, pady=5)
        instructor_id_entry = tk.Entry(input_frame)
        instructor_id_entry.insert(0, old_instructor_id)
        instructor_id_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def submit():
            updates = []
            values = []
            
            if name_entry.get():
                updates.append("name = %s")
                values.append(name_entry.get())
                
            if code_entry.get():
                updates.append("code = %s")
                values.append(code_entry.get())
                
            if credit_entry.get():
                updates.append("credit = %s")
                values.append(credit_entry.get())
                
            if instructor_id_entry.get():
                updates.append("instructor_id = %s")
                values.append(instructor_id_entry.get())
                
            if not updates:
                messagebox.showinfo("Info", "No changes made")
                return
                
            values.append(course_id)
            
            query = f"UPDATE courses SET {', '.join(updates)} WHERE id = %s"
            
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Course updated successfully")
                        self.load_data()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Course ID not found")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating course: {e}")
                finally:
                    conn.close()
        
        tk.Button(dialog, text="Update", command=submit).pack(pady=20)

    def add_course(self):
        name = self.name_entry.get()
        code = self.code_entry.get()
        credit = self.credit_entry.get()
        instructor_id = self.instructor_id_entry.get()
        
        if not (name and code and credit and instructor_id):
            from tkinter import messagebox
            messagebox.showerror("Error", "All fields are required")
            return
            
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO courses (name, code, credit, instructor_id) VALUES (%s, %s, %s, %s)",
                    (name, code, credit, instructor_id)
                )
                conn.commit()
                self.load_data()
                
                # Clear entries
                self.name_entry.delete(0, tk.END)
                self.code_entry.delete(0, tk.END)
                self.credit_entry.delete(0, tk.END)
                self.instructor_id_entry.delete(0, tk.END)
                
                from tkinter import messagebox
                messagebox.showinfo("Success", "Course added successfully")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Error", f"Error adding course: {e}")
            finally:
                conn.close()
        
        # Load Data
        self.load_data()

    def search_courses(self):
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
                    query = "SELECT * FROM courses WHERE code LIKE %s "
                    cursor.execute(query, (f"%{search_query}%",))
                else:
                    cursor.execute("SELECT * FROM courses")
                
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                conn.close()
    
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_data()
