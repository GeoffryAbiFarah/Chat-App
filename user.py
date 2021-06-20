from werkzeug.security import check_password_hash
class User:

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def check_password(self, password_input):
        # takes the hash and the input password and return true if they match
        return check_password_hash(self.password, password_input)