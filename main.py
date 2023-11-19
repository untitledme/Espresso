import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coffee App")

        uic.loadUi("main.ui", self)

        self.table_widget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки",
                                                     "Молотый/в зернах", "Описание вкуса",
                                                     "Цена", "Объем упаковки в литрах"])

        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()

        self.table_widget.setRowCount(len(coffee_data))
        self.table_widget.setColumnCount(7)
        for row, coffee in enumerate(coffee_data):
            for col, value in enumerate(coffee):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        conn.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_app = CoffeeApp()
    coffee_app.show()
    sys.exit(app.exec_())
