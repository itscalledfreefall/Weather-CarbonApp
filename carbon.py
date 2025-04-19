import sys

from json import JSONDecodeError

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QListWidget, QComboBox, QDialog, QTextEdit)
import json
from PyQt5.QtCore import Qt
class HistoryWindow(QDialog):
    def __init__(self, history_data, parent = None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.setGeometry(100,100,400,300)

        layout = QVBoxLayout()

        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        self.history_text.setText(str(history_data))

        layout.addWidget(self.history_text)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


class CarbonLite(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = QLabel(self)
        self.calculator_button = QPushButton("Calculate", self)
        self.amount_input = QLineEdit(self)
        self.save_button = QPushButton("Save Result",self)
        self.show_history_button = QPushButton("Show previous calculations",self)
        self.combo_box = QComboBox(self)  # ComboBox widget
        self.unitUI()

    def electricity_calculator(self, user_input):
        return user_input * 0.0006

    def natural_gas_calculator(self, user_input):
        return user_input * 0.0024

    def fuel_calculator(self, user_input):
        return user_input * 0.0034

    def fuel_calculator_normal(self, user_input):
        return user_input * 0.0027

    def func_chooser(self):
        selected_item = self.combo_box.currentText()  # Get the selected item from the combo box
        try:
            user_input = float(self.amount_input.text())  # Get the user input (amount)
            if selected_item == "Electricity":
                result = self.electricity_calculator(user_input)
            elif selected_item == "Natural Gas":
                result = self.natural_gas_calculator(user_input)
            elif selected_item == "Fuel (Diesel)":
                result = self.fuel_calculator(user_input)
            elif selected_item == "Fuel (Petrol)":
                result = self.fuel_calculator_normal(user_input)
            else:
                result = "Invalid Selection"
            self.result_label.setText(f"Result: {result:.4f} tCO₂e")
            self.last_result = {"type":selected_item,"amount":user_input,"result":result}
        except ValueError:
            self.result_label.setText("Please enter a valid number.")
            self.last_result = None

    def unitUI(self):
        self.setWindowTitle("Carbon Lite")
        vbox = QVBoxLayout()

        # combobox selections
        self.combo_box.addItem("Electricity")
        self.combo_box.addItem("Natural Gas")
        self.combo_box.addItem("Fuel (Diesel)")
        self.combo_box.addItem("Fuel (Petrol)")

        # widgets
        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.amount_input)
        vbox.addWidget(self.calculator_button)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.show_history_button)
        vbox.addWidget(self.result_label)

        self.setLayout(vbox)

        # Connect the combo box signal to func_chooser
        self.combo_box.currentIndexChanged.connect(self.func_chooser)
        # Connect the calculate button to func_chooser as well
        self.calculator_button.clicked.connect(self.func_chooser)

        self.save_button.clicked.connect(self.save_calculations)

        self.show_history_button.clicked.connect(self.show_calculations_history)



        self.result_label.setObjectName("result_label")
        self.calculator_button.setObjectName("calculator_button")
        self.combo_box.setObjectName("combo_box")
        self.save_button.setObjectName("save_button")
        self.show_history_button.setObjectName("show_history_button")





        self.setStyleSheet("""
        QLabel,QPushButton{
        font-family:Times New Roman;
        font-size:15px;
        }
        QComboBox{
        font-size:15px;
       }
       
        """)
    def save_calculations(self):
        if hasattr(self,"last_result") and self.last_result:
            try:
                with(open("calculations.json","r")) as file:
                    data = json.load(file)
            except(FileNotFoundError or JSONDecodeError):
                data = []

            data.append(self.last_result)

            with(open("calculations.json","w")) as file:
                json.dump(data, file, indent=4)
            self.result_label.setText("Result saved!")

    def show_calculations_history(self):
        try:
            with open("calculations.json", "r") as file:
                history_data = json.load(file)

            # Format the history data into a readable string
            history_text = ""
            for entry in history_data:
                history_text += f"Type: {entry['type']}, Amount: {entry['amount']}, Result: {entry['result']:.4f} tCO₂e\n"

            # Pass the formatted string to the HistoryWindow
            self.history_window = HistoryWindow(history_text, self)
            self.history_window.show()
        except (FileNotFoundError, JSONDecodeError):
            self.history_window = HistoryWindow("No history data found.", self)
            self.history_window.show()










