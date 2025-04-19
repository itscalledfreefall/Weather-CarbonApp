import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QInputDialog)
from PyQt5.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather")
        self.resize(700, 500)

        self.city_label = QLabel("Enter a city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather info", self)
        self.save_as_default_city = QPushButton("Save this as my default city", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.default_location = None
        self.ask_users_location()  # asking for a location to user

        self.initUI()

        # if there is location saved auto shows the locations weather
        if self.default_location:
            self.city_input.setText(self.default_location)
            self.get_weather()

    def ask_users_location(self):
        location, ok = QInputDialog.getText(
            self,
            "Enter your location",
            "Please enter your city:",
            QLineEdit.Normal
        )
        if ok and location.strip():
            self.default_location = location.strip().title()
        else:
            self.default_location = "Istanbul"

    def initUI(self):
        self.setWindowTitle("CO Free Weather")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.save_as_default_city)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.save_as_default_city.setObjectName("save_as_default_city")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")
        self.temperature_label.setObjectName("temperature_label")

        self.setStyleSheet("""
        QLabel, QPushButton {
            font-family: Times New Roman;
        }
        QLabel#city_label {
            font-size: 25px;
            font-style: italic;
        }
        QLineEdit#city_input {
            font-size: 15px;
            font-weight: bold;
        }
        QPushButton#get_weather_button {
            font-size: 15px;
        }
        QPushButton#save_as_default_city {
            font-size: 15px;
        }
        QLabel#temperature_label {
            font-size: 50px;
            font-weight: bold;
        }
        QLabel#emoji_label {
            font-size: 70px;
            font-family: Segoe UI emoji;
        }
        QLabel#description_label {
            font-size: 20px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "e6f17416f6e2a1341eeaf38b901afc22"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200: # 200 means it is all good
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error_message("Bad request\nPlease check your input.")
                case 401:
                    self.display_error_message("Unauthorized\nInvalid API Key.")
                case 403:
                    self.display_error_message("Forbidden\nAccess is denied.")
                case 404:
                    self.display_error_message("Not Found\nCity not found.")
                case 500:
                    self.display_error_message("Internal server error\nPlease try again later.")
                case 502:
                    self.display_error_message("Bad gateway\nInvalid response from the server.")
                case 503:
                    self.display_error_message("Service Unavailable\nServer is down.")
                case 504:
                    self.display_error_message("Gateway timeout \nNo response from server.")
                case _:
                    self.display_error_message(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error_message("Connection error\nCheck your connection")

        except requests.exceptions.Timeout:
            self.display_error_message("Timeout Error \nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error_message("Too many redirects\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error_message(f"Request Error:\n{req_error}")

    def display_error_message(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 20px;")
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temperature_c = data["main"]["temp"]
        self.temperature_label.setStyleSheet("font-size:50px;")
        self.temperature_label.setText(f"{temperature_c:.0f}°C")

        weather_id = data["weather"][0]["id"]
        weather_desc = data["weather"][0]["description"]
        self.description_label.setText(f"{weather_desc}")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

def run_weather_app():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())


