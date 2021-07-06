from PyQt5 import QtWidgets, QTableWidget
import PyQt5 as qt
from c19_ui import Ui_MainWindow
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Main()
    application.show()
    
    sys.exit(app.exec())