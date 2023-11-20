import sqlite3
import sys
import mainWindow, coffeeEditForm

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5 import uic

idi = 1


class AddEditCoffeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = coffeeEditForm.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Добавить/редактировать кофе")

        self.ui.save_button.clicked.connect(self.save_data)

    def save_data(self):
        global idi
        id1 = self.ui.id_edit.text()
        name = self.ui.name_edit.text()
        roast = self.ui.roast_edit.text()
        type = self.ui.ground_edit.text()
        description = self.ui.description_edit.text()
        price = self.ui.price_edit.text()
        amount = self.ui.amount_edit.text()

        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        a = cursor.execute(f"SELECT * FROM coffee WHERE Id = {int(id1)}").fetchall()

        if len(a) != 0:
            cursor.execute("UPDATE coffee SET sort=?, roasting=?, type=?, taste=?, price=?, amount=? WHERE id=?",
                           (name, roast, type, description, int(price), amount, int(id1)))
        else:
            cursor.execute(
                "INSERT INTO coffee (id, sort, roasting, type, taste, price, amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (idi + 1, name, roast, type, description, price, amount))
        idi += 1
        conn.commit()
        conn.close()

        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coffee App")
        self.design = mainWindow.Ui_MainWindow()
        self.design.setupUi(self)
        self.design.add_button.clicked.connect(self.add)
        self.loadTable()
        self.design.table_widget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки",
                                                     "Молотый/в зернах", "Описание вкуса",
                                                     "Цена", "Объем упаковки в литрах"])

    def loadTable(self):
        self.design.table_widget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки",
                                                     "Молотый/в зернах", "Описание вкуса",
                                                     "Цена", "Объем упаковки в литрах"])

        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()
        self.design.table_widget.itemChanged.connect(self.run)
        self.design.table_widget.setRowCount(len(coffee_data))
        self.design.table_widget.setColumnCount(7)
        for row, coffee in enumerate(coffee_data):
            for col, value in enumerate(coffee):
                item = QTableWidgetItem(str(value))
                self.design.table_widget.setItem(row, col, item)
        self.design.table_widget.horizontalHeader().setStretchLastSection(True)
        conn.close()

    def getString(self, row) -> tuple:
        b = list()
        for i in range(0, 7):
            try:
                b.append(self.design.table_widget.item(row, i).text())
            except AttributeError:
                continue
        b = tuple(b)
        return b

    def run(self, item: QTableWidgetItem):
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        row = item.row()
        a = self.getString(row)
        if len(a) > 6:
            cursor.execute("UPDATE coffee SET sort=?, roasting=?, type=?, taste=?, price=?, amount=? WHERE id=?",
                           (a[1], a[2], a[3], a[4], a[5], a[6], a[0]))
        conn.commit()
        conn.close()

    def add(self):
        if AddEditCoffeeDialog().exec():
            self.loadTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_app = CoffeeApp()
    coffee_app.show()
    sys.exit(app.exec_())
