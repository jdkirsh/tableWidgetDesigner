'''
Aug 17 2020 - tableWidget in Designer - Working!
'''



import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pandas as pd

# qtcreator_file  = "<your .ui file>" # Enter file here.
qtcreator_file  = "tw1Designer.ui" # Enter file here.jkTableView.ui
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        data = pd.read_csv("SPYtoDF.csv")
        self.tw1.setColumnCount(2)
        self.tw1.setHorizontalHeaderLabels(['Colour', 'Model'])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())