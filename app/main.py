import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from utils.session import UserSession
from screens.login_screen import LoginScreen
from screens.profile_creation_screen import ProfileCreationScreen
from screens.home_screen import HomeScreen
from screens.space_screen import SpaceScreen
from screens.create_event_screen import CreateEventScreen
from models.user_model import UserModel


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sports App")
        self.user_session = UserSession()  # Shared user session
        self.user_model = UserModel()     # Shared UserModel instance
        self.resize(600, 400)

        self.current_screen = None
        self.show_login_screen()  # Start with the login screen

    def show_login_screen(self):
        """Switch to LoginScreen."""
        if self.current_screen:
            self.current_screen.deleteLater()
        self.current_screen = LoginScreen(
            switch_to_profile_creation=self.show_profile_creation_screen,
            switch_to_home_screen=self.show_home_screen,
            user_session=self.user_session,
            user_model=self.user_model
        )
        self.setCentralWidget(self.current_screen)

    def show_profile_creation_screen(self):
        """Switch to ProfileCreationScreen."""
        if self.current_screen:
            self.current_screen.deleteLater()
        self.current_screen = ProfileCreationScreen(
            switch_to_login=self.show_login_screen,
            user_model=self.user_model
        )
        self.setCentralWidget(self.current_screen)

    def show_home_screen(self):
        """Switch to HomeScreen."""
        if self.current_screen:
            self.current_screen.deleteLater()
        self.current_screen = HomeScreen(
            switch_to_login=self.show_login_screen,
            switch_to_space=self.show_space_screen,
            user_session=self.user_session,
            user_model=self.user_model
        )
        self.setCentralWidget(self.current_screen)

    def show_space_screen(self):
        """Switch to SpaceScreen."""
        if self.current_screen:
            self.current_screen.deleteLater()
        self.current_screen = SpaceScreen(
            switch_to_home=self.show_home_screen,
            switch_to_create_event=self.show_create_event_screen,
            user_session=self.user_session,
            user_model=self.user_model
        )
        self.setCentralWidget(self.current_screen)

    def show_create_event_screen(self):
        """Switch to CreateEventScreen."""
        if self.current_screen:
            self.current_screen.deleteLater()
        self.current_screen = CreateEventScreen(
            switch_to_space=self.show_space_screen,
            user_session=self.user_session,
            user_model=self.user_model
        )
        self.setCentralWidget(self.current_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
