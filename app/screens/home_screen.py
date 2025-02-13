from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, switch_to_login, switch_to_space, user_session, user_model):
        super().__init__()
        self.setWindowTitle("Home Screen")
        self.resize(600, 400)

        # Callback for switching screens
        self.switch_to_login = switch_to_login
        self.switch_to_space = switch_to_space

        self.user_model = user_model
        self.user_session = user_session

        # Welcome label and spaces label
        self.welcome_label = QLabel(f"Sports spaces")
        self.welcome_label.setStyleSheet("font-size: 20px;")

        # Layout
        layout = QVBoxLayout()

        # Scrollable area for buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)

        space_infos = self.user_model.get_spaces_info()
        # Add buttons to the scrollable area
        for area_info in space_infos:
            name = area_info["name"]
            event_count = area_info["event_count"]
            latest_report = area_info["latest_report"]
            button_text = f"{name}\nEvents: {event_count} | Latest Congestion: {latest_report}"
            button = QPushButton(button_text)
            button.setFixedHeight(50)
            button.clicked.connect(
                lambda _, area_info=area_info: self.space_selected(area_info)
            )
            scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_content)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)

        layout.addWidget(self.welcome_label)
        layout.addWidget(scroll_area)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def logout(self):
        """Handle logout and switch back to the login screen."""
        self.user_session.clear()
        self.switch_to_login()

    def space_selected(self, area_info):
        """Switch to selected space screen."""
        self.user_session.selected_space["id"] = area_info["id"]
        self.user_session.selected_space["name"] = area_info["name"]
        self.switch_to_space()
