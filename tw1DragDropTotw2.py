'''
Aug 17 2020 - tableWidget in Designer - Working!
Aug 17 2020 - two tablewidget in Designer - Working!
Aug 17 2020 - drag and drop from tablewidget tw1 to tw2 - Working !

'''



import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pandas as pd

# qtcreator_file  = "<your .ui file>" # Enter file here.
# this drag and drop example uses the same gui as w1Andtw2Designer.py
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem

qtcreator_file  = "tw1Andtw2Designer.ui" # Enter file here.jkTableView.ui
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)



# class TableWidgetDragRows(QTableWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # self.setDragEnabled(True)
#         # self.setAcceptDrops(True)
#         # self.setSelectionBehavior(QAbstractItemView.SelectRows)
#         # self.setDragDropOverwriteMode(False)
#         # # self.setSelectionMode(QAbstractItemView.SingleSelection)
#
#         self.last_drop_row = None
#
#     # Override this method to get the correct row index for insertion
#     def dropMimeData(self, row, col, mimeData, action):
#         self.last_drop_row = row
#         return True
#
#
#     def dropEvent(self, event):
#         # The QTableWidget from which selected rows will be moved
#         sender = event.source()
#
#         # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
#         super().dropEvent(event)
#         # Now we know where to insert selected row(s)
#         dropRow = self.last_drop_row
#
#         selectedRows = sender.getselectedRowsFast()
#
#
#         # Allocate space for transfer
#         for r in selectedRows:
#             self.insertRow(dropRow)
#
#         # if sender == receiver (self), after creating new empty rows selected rows might change their locations
#         sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
#         selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]
#
#         # copy content of selected rows into empty ones
#         for i, srow in enumerate(selectedRows):
#             for j in range(self.columnCount()):
#                 item = sender.item(srow, j)
#                 print ("item.text=",item.text())
#                 if item:
#                     source = QTableWidgetItem(item)
#                     self.setItem(dropRow + i, j, source)
#
#         # delete selected rows
#         for srow in reversed(selectedRows):
#             sender.removeRow(srow)
#
#         event.accept()
#
#
#     def getselectedRowsFast(self):
#         selectedRows = []
#         for item in self.selectedItems():
#             if item.row() not in selectedRows:
#                 selectedRows.append(item.row())
#         selectedRows.sort()
#         return selectedRows
#



# class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow, TableWidgetDragRows):
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        data = pd.read_csv("SPYtoDF.csv")
        self.tw1.setColumnCount(2)
        self.tw1.setHorizontalHeaderLabels(['Colour', 'Model'])
        self.tw1.setDragEnabled(True)
        self.tw1.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tw2.setColumnCount(2)
        self.tw2.setHorizontalHeaderLabels(['Colour', 'Model'])
        self.tw2.setAcceptDrops(True)

        filled_widget = self.tw1
        items = [('Red', 'Toyota'), ('Blue', 'RV'), ('Green', 'Beetle')]
        for i, (colour, model) in enumerate(items):
            c = QTableWidgetItem(colour)
            m = QTableWidgetItem(model)

            filled_widget.insertRow(filled_widget.rowCount())
            filled_widget.setItem(i, 0, c)
            filled_widget.setItem(i, 1, m)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())