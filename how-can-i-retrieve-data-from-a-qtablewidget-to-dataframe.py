# https://stackoverflow.com/questions/37680981/how-can-i-retrieve-data-from-a-qtablewidget-to-dataframe

def dataframe_generation_from_table(self,table):
    number_of_rows = table.rowCount()
    number_of_columns = table.columnCount()

    tmp_df = pd.DataFrame(
                columns=['Date', str(self.final_lvl_of_analysis), 'Value'], # Fill columnets
                index=range(number_of_rows) # Fill rows
                )

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            tmp_df.ix[i, j] = table.item(i, j).data()

    return tmp_df

def saveFile(self):
    df = pd.DataFrame()
    savePath = QtGui.QFileDialog.getSaveFileName(None, "Blood Hound",
        "Testing.csv", "CSV files (*.csv)")
    rows = self.tableWidget.rowCount()
    columns = self.tableWidget.columnCount()

    for i in range(rows):
        for j in range(columns):
            df.loc[i, j] = str(self.tableWidget.item(i, j).text())
    df.to_csv((savePath), header = None, index = 0)