from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class LoginScreen(QWidget):
    def __init__(self, switch_to_profile_creation, switch_to_home_screen,
                 user_session, user_model):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(600, 400)

        # Callbacks for switching screens
        self.switch_to_profile_creation = switch_to_profile_creation
        self.switch_to_home_screen = switch_to_home_screen

        self.user_model = user_model
        self.user_session = user_session

        # Layout
        layout = QVBoxLayout()

        # Notification Label
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")  # Default style for errors

        # UI Components
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        create_profile_button = QPushButton("Create Profile")
        create_profile_button.clicked.connect(self.switch_to_profile_creation)

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.message_label)
        layout.addWidget(login_button)
        layout.addWidget(create_profile_button)

        self.setLayout(layout)

    def login(self):
        """Authenticate the user and update the inline notification label."""
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            self.message_label.setText("Email and password are required.")

        user_info = self.user_model.get_user_info(email, password)
        if user_info:
            self.message_label.setText("")
            self.user_session.set_user(user_info["user_id"], email, user_info["name"])
            self.switch_to_home_screen()
        else:
            self.message_label.setText("Invalid email or password.")
