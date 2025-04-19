import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from weather import WeatherApp
from carbon import CarbonLite

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather & Carbon App")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.weather_tab = WeatherApp()
        self.carbon_tab = CarbonLite()

        self.tabs.addTab(self.weather_tab, "Weather")
        self.tabs.addTab(self.carbon_tab, "Carbon Calculator")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-size: 15px;
        }

        QTabWidget::pane {
            border: 1px solid #3a3a3a;
            border-radius: 8px;
        }

        QTabBar::tab {
            background: #2d2d2d;
            padding: 8px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin: 1px;
        }

        QTabBar::tab:selected {
            background: #0078d7;
        }

        QPushButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 15px;
        }

        QPushButton:hover {
            background-color: #005fa3;
        }

        QLineEdit, QTextEdit, QComboBox {
            background-color: #2d2d2d;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            padding: 6px;
            color: white;
        }

        QLabel {
            font-weight: bold;
        }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
