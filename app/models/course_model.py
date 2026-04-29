class Course:
    def __init__(self, course_id, title, description, teacher_id):
        self.id = course_id
        self.title = title
        self.description = description
        self.teacher_id = teacher_id

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', teacher_id={self.teacher_id})>"
