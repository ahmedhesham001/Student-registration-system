USE student_registration_system;

-- Insert data into departments
INSERT INTO departments (name) VALUES
('Computer Science'),
('Electrical Engineering'),
('Civil Engineering'),
('Mechanical Engineering'),
('Software Engineering');

-- Insert data into instructors
INSERT INTO instructors (first_name, last_name, phone, email, department_id) VALUES
('John', 'Doe', '1234567890', 'john.doe@example.com', 1),
('Jane', 'Smith', '1234567891', 'jane.smith@example.com', 2),
('Alice', 'Johnson', '1234567892', 'alice.johnson@example.com', 3),
('Bob', 'Brown', '1234567893', 'bob.brown@example.com', 4),
('Charlie', 'Davis', '1234567894', 'charlie.davis@example.com', 5);

-- Insert data into courses
INSERT INTO courses (code, name, credit, instructor_id) VALUES
('CS101', 'Introduction to Computer Science', 3, 11001),
('EE101', 'Introduction to Electrical Engineering', 3, 11002),
('CE101', 'Introduction to Civil Engineering', 3, 11003),
('ME101', 'Introduction to Mechanical Engineering', 3, 11004),
('SE101', 'Introduction to Software Engineering', 3, 11005);

-- Insert data into students
INSERT INTO students (first_name, last_name, phone, email, academic_year, department_id) VALUES
('John', 'Doe', '1234567890', 'john.doe@example.com', 2022, 1),
('Jane', 'Smith', '1234567891', 'jane.smith@example.com', 2022, 2),
('Alice', 'Johnson', '1234567892', 'alice.johnson@example.com', 2022, 3),
('Bob', 'Brown', '1234567893', 'bob.brown@example.com', 2022, 4),
('Charlie', 'Davis', '1234567894', 'charlie.davis@example.com', 2022, 5);

-- Insert data into enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, gpa, semester) VALUES
(10001, 101, '2022-01-15', 4.0, 'Fall'),
(10002, 102, '2022-02-20', 3.5, 'Spring'),
(10003, 103, '2022-03-10', 3.0, 'Summer'),
(10004, 104, '2022-04-05', 2.5, 'Fall'),
(10005, 105, '2022-05-25', 2.0, 'Spring');
