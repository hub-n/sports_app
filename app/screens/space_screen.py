from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QScrollArea, QHBoxLayout
)
from functools import partial

class SpaceScreen(QWidget):
    def __init__(self, switch_to_home, switch_to_create_event,
                 user_session, user_model):
        super().__init__()
        self.setWindowTitle("Space Screen")
        self.resize(600, 400)

        # Callback for switching screens
        self.switch_to_home = switch_to_home
        self.switch_to_create_event = switch_to_create_event

        self.user_model = user_model
        self.user_session = user_session
        self.selected_space = self.user_session.selected_space

        self.layout = QVBoxLayout()
        row_layout = QHBoxLayout()

        # Space name label
        space_name_label = QLabel(self.selected_space["name"])
        space_name_label.setStyleSheet("font-size: 20px;")

        # Create event button
        create_event_button = QPushButton("Create Event")
        create_event_button.clicked.connect(self.create_event)
        create_event_button.setFixedWidth(150)

        row_layout.addWidget(space_name_label)
        row_layout.addWidget(create_event_button)

        # Join status label
        self.join_status_label = QLabel("")

        self.scroll_area = self.setup_event_list()

        # Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back)

        self.layout.addLayout(row_layout)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.join_status_label)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

    def setup_event_list(self):
         # Scrollable area for labels and buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)

        # Get info on all events
        events_info = self.user_model.get_events_info(self.selected_space)

        # Add rows with labels and buttons
        for i, event in enumerate(events_info):
            row_layout = QHBoxLayout()

            # Text label
            title = event["title"]
            start_time = event["start_time"]
            end_time = event["end_time"]
            participants = event["participant_names"]
            label_content = f"{title} | {start_time} - {end_time}\n"
            if participants:
                label_content += "Participants:"
                for participant in participants:
                    label_content += f" {participant},"
                label_content = label_content[:-1] + "."
            else:
                label_content += "No participants."
            label = QLabel(label_content)
            row_layout.addWidget(label)

            # Button
            if participants and self.user_session.name in participants:
                button = QPushButton("Quit")
                button.clicked.connect(
                    partial(self.quit_event, event["id"], self.user_session.user_id)
                )
            else:
                button = QPushButton("Join")
                button.clicked.connect(
                    partial(self.join_event, event["id"], self.user_session.user_id)
                )
            button.setFixedWidth(100)
            row_layout.addWidget(button)

            # Add the row layout to the scroll layout
            row_frame = QFrame()
            row_frame.setLayout(row_layout)
            scroll_layout.addWidget(row_frame)

            # Add a separator line
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            scroll_layout.addWidget(separator)

        scroll_area.setWidget(scroll_content)
        return scroll_area

    def join_event(self, event_id, user_id):
        """Add user to event participants."""
        if self.user_model.join_event(event_id, user_id):
            # Remove current scroll area data
            self.layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()

            # Setup an updated scroll area
            self.scroll_area = self.setup_event_list()
            self.layout.insertWidget(1, self.scroll_area)
            self.join_status_label.setText("Event joined.")
        else:
            self.join_status_label.setText("Error while trying to join the event.")

    def quit_event(self, event_id, user_id):
        """Remove user from event participants."""
        if self.user_model.quit_event(event_id, user_id):
            # Remove current scroll area data
            self.layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()

            # Setup an updated scroll area
            self.scroll_area = self.setup_event_list()
            self.layout.insertWidget(1, self.scroll_area)
            self.join_status_label.setText("Event quit.")
        else:
            self.join_status_label.setText("Error while trying to quit the event.")

    def create_event(self):
        self.switch_to_create_event()

    def back(self):
        """Switch back to home screen"""
        self.user_session.selected_space["id"] = None
        self.user_session.selected_space["name"] = None
        self.switch_to_home()
