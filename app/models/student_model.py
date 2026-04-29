class Student:
    def __init__(self, student_id, name, email, user_id):
        self.id = student_id
        self.name = name
        self.email = email
        self.user_id = user_id

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}', user_id={self.user_id})>"
