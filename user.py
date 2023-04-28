from flask_login import UserMixin

class User (UserMixin):
    def __init__ (self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__ (self):
        return f"User('{self.name}', '{self.email}', '{self.password}')"
    
    def is_authenticated (self):
        return True
    
    def get_id(self):
        return self.email
    
