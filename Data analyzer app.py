from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, \
QFileDialog, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore , QtWidgets, QtGui
from PyQt5.QtCore import Qt
import sys
import pandas as pd
import os

class Window(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Data analyzer")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.btn1 = QPushButton("Select file")
        self.btn1.clicked.connect(self.get_data)
        self.layout.addWidget(self.btn1)
        self.table = QTableWidget()
        self.setLayout(self.layout)
        
        # self.l1 = QLabel("Select category of data:")

    def get_data(self):
        print("funkcja dziala")
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Hey! Select a File')
        file = path[0]
        ext = os.path.splitext(file)[1]
      
        try:
            if ext == ".csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except:
            msg = QMessageBox()
            msg.setText("Something went wrong. Please make sure that selected file have correct format.")
            msg.setWindowTitle("Error")
            msg.exec()
            return
        
        rows_count = str(df.shape[0])
        col_count = str(df.shape[1])
        print("Dataset has " + rows_count + " rows and " + col_count + " columns")
        
        numeric_cols = []
        for index, value in df.dtypes.items():
            if value == "int64" or value == "float64":
                numeric_cols.append(index)
        
        measures = ["mean", "max", "min", "std"]
        
        t_rows = len(numeric_cols)
        t_cols = len(measures)
        
        self.table.setRowCount(t_rows)
        self.table.setColumnCount(t_cols)
        
      
        def set_row_color(table, row_index):
            if row_index % 2 == 0:
                for column in range(table.columnCount()):
                    table.item(row_index, column).setBackground(QtGui.QColor("#ebecf0"))
                    
        # function for adding dynamic number of columns:
        def calculate(table, measure_list, row_id, name):
            col_id = 0
            for m in measure_list:
                if m == "mean":
                    table.setItem(row_id, col_id, QTableWidgetItem(str(round(df[f"{name}"].mean(), 2) )))
                if m == "max":
                    table.setItem(row_id, col_id, QTableWidgetItem(str(df[f"{name}"].max() )))
                if m == "min":
                    table.setItem(row_id, col_id, QTableWidgetItem(str(df[f"{name}"].min() )))
                if m == "std":
                    table.setItem(row_id, col_id, QTableWidgetItem(str(round(df[f"{name}"].std(), 2) )))
                col_id = col_id + 1
        
        row_id = 0
        
        # filling in the table and seting rows colors:
        for name in numeric_cols:
            calculate(self.table, measures, row_id, name)
            set_row_color(self.table, row_id)
            row_id = row_id + 1
        
        # Setting labels and theirs color:
        self.table.setVerticalHeaderLabels(numeric_cols)
        self.table.setHorizontalHeaderLabels(measures)
        stylesheet = "::section{Background-color: #b8e2f2}"
        self.table.horizontalHeader().setStyleSheet(stylesheet)
        self.table.verticalHeader().setStyleSheet(stylesheet)
       
        self.results_view()
            
    def results_view(self):
        
        '''
        for widgets in self.winfo_children():
            widgets.destroy()
        '''
        
        self.l1 = QLabel("Data insights:")
        self.back_btn = QPushButton("Go back")
        self.back_btn.clicked.connect(self.main_view)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.back_btn)
         
    def main_view(self):
        pass
        
def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    


    
    
    