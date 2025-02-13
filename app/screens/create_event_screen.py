from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QLineEdit,
    QPushButton, QScrollArea, QHBoxLayout, QDateTimeEdit
)
from PyQt5.QtCore import QDateTime

class CreateEventScreen(QWidget):
    def __init__(self, switch_to_space, user_session, user_model):
        super().__init__()
        self.setWindowTitle("Space Screen")
        self.resize(600, 400)

        self.user_session = user_session
        self.user_model = user_model

        layout = QVBoxLayout()

        # Callback for switching screens
        self.switch_to_space = switch_to_space

        # Notification Label
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")  # Default style for errors

        # UI Components
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")

        start_time_label = QLabel("Start Time:")
        start_time_label.setFixedWidth(100)

        end_time_label = QLabel("End Time:")
        end_time_label.setFixedWidth(100)

        # Create horizontal layouts
        start_time_layout = QHBoxLayout()
        end_time_layout = QHBoxLayout()

        # Create QDateTimeEdit widgets
        self.start_time_edit = QDateTimeEdit()
        self.start_time_edit.setCalendarPopup(True)  # Enable calendar popup
        self.start_time_edit.setDateTime(QDateTime.currentDateTime())  # Set default date and time

        self.end_time_edit = QDateTimeEdit()
        self.end_time_edit.setCalendarPopup(True)
        self.end_time_edit.setDateTime(QDateTime.currentDateTime())

        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.start_time_edit)
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(self.end_time_edit)

        # Create event button
        create_button = QPushButton("Create Event")
        create_button.clicked.connect(self.create_event)

        # Create back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_space)

        layout.addWidget(QLabel("Create Event"))
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_input)
        layout.addLayout(start_time_layout)
        layout.addLayout(end_time_layout)
        layout.addWidget(self.message_label)
        layout.addWidget(create_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def create_event(self):
        """Create an event and update the inline notification label."""
        space_id = self.user_session.selected_space["id"]
        organizer_id = self.user_session.user_id
        title = self.title_input.text()
        description = self.description_input.text()
        start_time = self.start_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss.zzz000")
        end_time = self.start_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss.zzz000")

        if not title or not start_time or not end_time:
            self.message_label.setText("Title, start time and end time are required.")
        elif self.user_model.create_event(space_id, organizer_id, title, description,
                                          start_time, end_time):
            self.message_label.setStyleSheet("color: green;")  # Success message in green
            self.message_label.setText("Event created successfully!")
            self.clear_inputs()
        else:
            self.message_label.setStyleSheet("color: red;")
            self.message_label.setText("Failed to create event. Please try again.")

    def clear_inputs(self):
        """Clear input fields after successful event creation."""
        self.title_input.clear()
        self.description_input.clear()
