import PyQt5 as qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QShortcut,
    QTableWidgetItem,
)
from c19_ui import Ui_MainWindow
from c19_api import C19_info
import sys


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.c19_info = C19_info()
        self.current_country = ""
        self.fill_table()

        self.ui.refresh.clicked.connect(self.__refresh)
        QShortcut("ctrl+r", self).activated.connect(self.__refresh)

        self.ui.search.clicked.connect(self.__search)
        self.ui.search_input.returnPressed.connect(self.__search)
        QShortcut("ctrl+s", self).activated.connect(
            lambda: self.ui.search_input.setFocus()
        )

    def fill_table(self, country=""):
        try:
            self.c19_info.update_data_with(country)
            data = self.c19_info.get_table_colloms()
            self.current_country = country
        except:
            self.__search_error()
            return
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        
        table_Headers = []
        self.ui.tableWidget.setColumnCount(len(data))
        self.ui.tableWidget.setRowCount(len(list(data.values())[0]))
        for n, key in enumerate(data.keys()):
            table_Headers.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.ui.tableWidget.setItem(m, n, newitem)
        self.ui.tableWidget.setHorizontalHeaderLabels(table_Headers)
        
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def __refresh(self):
        self.fill_table(self.current_country)

    def __search(self):
        self.fill_table(self.ui.search_input.text())

    def __search_error(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ALARM!")
        dlg.setText("Cant find anything with this search input, try use 2/3 letters country name instead of full.\nBlank search mean all european countries")
        button = dlg.exec()



if __name__ == "__main__":
    app = QApplication([])
    application = Main()
    application.show()

    sys.exit(app.exec())
