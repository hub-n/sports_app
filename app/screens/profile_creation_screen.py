from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class ProfileCreationScreen(QWidget):
    def __init__(self, switch_to_login, user_model):
        super().__init__()
        self.setWindowTitle("Create Profile")
        self.resize(600, 400)

        # Callback for switching screens
        self.switch_to_login = switch_to_login

        self.user_model = user_model

        # Layout
        layout = QVBoxLayout()

        # Notification Label
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")  # Default style for errors

        # UI Components
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.profile_picture_input = QLineEdit()
        self.profile_picture_input.setPlaceholderText("Profile Picture URL")

        self.bio_input = QLineEdit()
        self.bio_input.setPlaceholderText("Bio")

        create_button = QPushButton("Create Profile")
        create_button.clicked.connect(self.create_profile)

        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self.switch_to_login)

        layout.addWidget(QLabel("Create Profile"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.profile_picture_input)
        layout.addWidget(self.bio_input)
        layout.addWidget(self.message_label)
        layout.addWidget(create_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def create_profile(self):
        """Create a user profile and update the inline notification label."""
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        profile_picture_url = self.profile_picture_input.text()
        bio = self.bio_input.text()

        if not name or not email or not password:
            self.message_label.setText("Name, email and password are required.")
        elif self.user_model.create_user(name, email, password, profile_picture_url, bio):
            self.message_label.setStyleSheet("color: green;")  # Success message in green
            self.message_label.setText("Profile created successfully! Please login.")
            self.clear_inputs()
        else:
            self.message_label.setStyleSheet("color: red;")
            self.message_label.setText("Failed to create profile. Please try again.")

    def clear_inputs(self):
        """Clear input fields after successful profile creation."""
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.profile_picture_input.clear()
        self.bio_input.clear()
