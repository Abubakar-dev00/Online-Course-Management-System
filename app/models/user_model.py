class User:
    def __init__(self, user_id, username, role, password=None):
        self.id = user_id
        self.username = username
        self.role = role
        self.password = password

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
