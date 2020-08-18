import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pandas as pd

# qtcreator_file  = "<your .ui file>" # Enter file here.
qtcreator_file  = "jkTableView.ui" # Enter file here.jkTableView.ui
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # data = pd.DataFrame([
        #     [1, 9, 2],
        #     [1, 0, -1],
        #     [3, 5, 2],
        #     [3, 3, 2],
        #     [5, 8, 9],
        # ], columns=['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])
        data = pd.read_csv("SPYtoDF.csv")
        self.model = TableModel(data)
        self.jktableView.setModel(self.model)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())