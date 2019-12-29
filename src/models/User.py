class User:

    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = email
        self.is_authenticated = False

    def get_email(self):
        return self.email

    def get_user_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.is_authenticated

    # There's no way this is the correct way to do this
    def authenticate(self):
        self.is_authenticated = True
