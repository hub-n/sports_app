class UserSession:
    def __init__(self):
        self.user_id = None
        self.email = None
        self.name = None
        self.selected_space = {
            "id": None,
            "name": None
        }

    def set_user(self, user_id, email, name):
        """Set the logged-in user details."""
        self.user_id = user_id
        self.email = email
        self.name = name

    def clear(self):
        """Clear the user session on logout."""
        self.user_id = None
        self.email = None
        self.name = None

    def is_logged_in(self):
        """Check if a user is logged in."""
        return self.user_id is not None
