import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QHBoxLayout, QApplication, \
    QVBoxLayout

from database import TwTopTwBottom, twBottomToListOfDict2

from database import underlyingDB

# qtcreator_file  = "<your .ui file>" # Enter file here.
qtcreator_file  = "OptionsOracleV01.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class TableWidgetDragRows(QTableWidget):    # sub class of QTableWidget
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)   # accept arguments

        self.cellClicked.connect(self.cell_was_clicked)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows) # full row drag mode

        self.last_drop_row = None

    def cell_was_clicked(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))
        item = self.itemAt(row, column)
        self.ID = item.text()


    # def currentIndexChanged(self, ind):
    def currentIndexChanged(self, ind, n):
        print("Combo Index changed {0} {1} : {2}".format(ind, self.sender().currentIndex(),
                                                             self.sender().currentText()))

    # Override this method to get the correct row index for insertion
    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        # print ("In dropMimeData...")
        return True


    def dropEvent(self, event):
        # print ("In dropEvent...")

        sender = event.source()

        # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
        super().dropEvent(event)
        # Now we know where to insert selected row(s)
        # print ("in  super().dropEvent(event)..."," dropRow = self.last_drop_row", self.last_drop_row)
        dropRow = self.last_drop_row
        # print("dropRow=",dropRow)

        selectedRows = sender.getselectedRowsFast()
        # print ("selectedRows=",selectedRows)

        # Allocate space for transfer
        for r in selectedRows:
            self.insertRow(dropRow)
            # print ("In Loop..."," self.insertRow(dropRow)...", " dropRow=",dropRow)

        # if sender == receiver (self), after creating new empty rows selected rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        var1 = enumerate(selectedRows)
        for i, srow in enumerate(selectedRows): # iterate every selected Row
            # print ("for i, srow in enumerate(selectedRows)=", " i=",i, " srow=", srow, " enumerate(selectedRows)=",var1)
            rowColumn = 1
            dfRow = dropRow
            dfColumn = 'Type'
            item = sender.item(srow, rowColumn)
            source = QTableWidgetItem(item)
            print("dropping :", item.text(), " srow=", srow, " rowColumn=", rowColumn)
            self.comboBox = QtWidgets.QComboBox()
            li = ["Put","Call"]
            self.comboBox.addItems(li)
            # self.comboBox.currentIndexChanged.connect(self.currentIndexChanged)
            self.comboBox.currentIndexChanged.connect(lambda: self.currentIndexChanged('z') )

            # self.setCellWidget(dropRow + i, rowColumn, comboBox)
            self.setCellWidget(dropRow + i, self.strategy.columns.get_loc(dfColumn), self.comboBox)
            print("UPDATING=", "dfRow=", dfRow, " dfColumn=", dfColumn, " item.text=", item.text())
            self.strategy.at[dfRow, dfColumn] = item.text()
            self.comboBox.setCurrentText(item.text())
            # self.comboBox.currentIndexChanged(print ("cinim"))

            # self.comboBox.activated.connect(pass_Net_Adap)
            #
            # def pass_Net_Adap(self):
            #     print ("type=", self.comboBox.currentText())

            # rowColumn = 2
            # item = sender.item(srow, rowColumn)
            # source = QTableWidgetItem(item)
            # self.setItem(dropRow + i, rowColumn, source)
            # dfRow = dropRow
            # dfColumn = 'Type'
            # print("UPDATING=", "dfRow=", dfRow, " dfColumn=", dfColumn, " item.text=", item.text() )
            # self.strategy.at[dfRow, dfColumn] = item.text()

            # print ("self.strategy=", self.strategy)

            # rowColumn = 3
            # item = sender.item(srow, rowColumn)
            # source = QTableWidgetItem(item)
            # self.setItem(dropRow + i, rowColumn, source)
            # dfRow = dropRow
            # dfColumn = 'Strike'
            # print("UPDATING=", "dfRow=", dfRow, " dfColumn=", dfColumn, " item.text=", item.text())
            # self.strategy.at[dfRow, dfColumn] = item.text()
            # print("self.strategy=", self.strategy)
            #
            #
            # rowColumn = 4
            # item = sender.item(srow, rowColumn)
            # source = QTableWidgetItem(item)
            # self.setItem(dropRow + i, rowColumn, source)
            # dfRow = dropRow
            # dfColumn = 'Symbol'
            # print("UPDATING=", "dfRow=", dfRow, " dfColumn=", dfColumn, " item.text=", item.text())
            # self.strategy.at[dfRow, dfColumn] = item.text()
            #
            # rowColumn = 5
            # item = sender.item(srow, rowColumn)
            # source = QTableWidgetItem(item)
            # self.setItem(dropRow + i, rowColumn, source)
            # dfRow = dropRow
            # dfColumn = 'Last'
            # print("UPDATING=", "dfRow=", dfRow, " dfColumn=", dfColumn, " item.text=", item.text())
            # # self.strategy.at[dfRow, dfColumn] = item.text()
            # self.strategy.at[dfRow, dfColumn] = float(item.text().replace(',', ''))
            # # print("self.strategy=", self.strategy)
            # # print("pause")
            # print(self.strategy.loc[[0]])


        # delete selected rows
        for srow in reversed(selectedRows):
            sender.removeRow(srow)

        event.accept()


    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
                # print("In getselectedRowsFast: item.row=", item.text())
        selectedRows.sort()
        # print ("In getselectedRowsFast: selectedRows=", selectedRows)
        return selectedRows


class OpOraWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        OptionsView = TableWidgetDragRows()
        OptionsView.data = TwTopTwBottom.gettwTop()
        OptionsView.setColumnCount(OptionsView.data.shape[1])
        OptionsView.setHorizontalHeaderLabels(list(OptionsView.data.columns))
        OptionsView.setAcceptDrops(False)

        for index, row in OptionsView.data.iterrows():
            Ty = QTableWidgetItem(str(row['Type']))
            St = QTableWidgetItem(str(row['Strike']))
            Sy = QTableWidgetItem(str(row['Symbol']))
            Op = QTableWidgetItem(str(row['Open_Int']))
            Vo = QTableWidgetItem(str(row['Volume']))
            La = QTableWidgetItem(str(row['Last']))
            Ex = QTableWidgetItem(str(row['Exp']))

            OptionsView.insertRow(index)
            OptionsView.setItem(index, 1, Ty)
            OptionsView.setItem(index, 2, St)
            OptionsView.setItem(index, 3, Sy)
            OptionsView.setItem(index, 4, Op)
            OptionsView.setItem(index, 5, Vo)
            OptionsView.setItem(index, 6, La)
            OptionsView.setItem(index, 7, Ex)

        self.RefreshPb.clicked.connect(self.refresh_underlying)

    def refresh_underlying(self):
        print ("Refreshing")
        self.underlyingDF = underlyingDB.loadUnderlying()

        print (self.underlyingDF['Symbol'][0])

        self.SymbolLe.setText(self.underlyingDF['Symbol'][0])
        self.LastUpdateLe.setText(self.underlyingDF['RecDate'][0])
        self.LastPriceLe.setText(self.underlyingDF['LastPrice'][0])
        self.ImpPctLe.setText(self.underlyingDF['ImpPct'][0])
        self.HisPctLe.setText(self.underlyingDF['HisPct'][0])
        self.DividendPctLe.setText(self.underlyingDF['DividendPct'][0])
        self.BidLe.setText(self.underlyingDF['Bid'][0])
        self.AskLe.setText(self.underlyingDF['Ask'][0])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OpOraWindow()
    window.show()
    sys.exit(app.exec_())