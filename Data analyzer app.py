
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, \
QFileDialog, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTableWidget, \
QFrame, QTableWidgetItem, QWidget, QStackedLayout, QHeaderView, QSpacerItem, QLayout
from PyQt5 import QtCore , QtWidgets, QtGui
from PyQt5.QtCore import Qt
import sys
import pandas as pd
import os

class Window(QWidget):
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Data analyzer")
        self.setFixedSize(460, 560)
        
        self.stackedLayout = QStackedLayout()
        
        self.page1 = QWidget()
        self.layout1 = QVBoxLayout()
        self.layout1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.title = QLabel("DATA ANALYZER")
        self.title.setMinimumSize(80, 80)
        self.title.setStyleSheet("font-size: 30px; ")
        self.l1 = QLabel("Select needed measures:")
        self.check_mean = QCheckBox("Mean")
        self.check_sum = QCheckBox("Sum")
        self.check_max = QCheckBox("Max value")
        self.check_min = QCheckBox("Min value")
        self.check_std = QCheckBox("Standard deviation")
        self.check_var = QCheckBox("Variation")
        self.btn1 = QPushButton("Select file")
        self.btn1.setToolTip("Please select dataset file in xlsx or csv format")
        self.spacer = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.credit = QLabel("Created by Adam Kotecki")
        self.credit.setAlignment(Qt.AlignCenter)
        
        self.check_mean.setChecked(True)
        self.check_max.setChecked(True)
        self.check_min.setChecked(True)
        self.btn1.clicked.connect(self.get_data)
        
        self.layout1.addWidget(self.title)
        self.layout1.addWidget(self.l1)
        self.layout1.addWidget(self.check_mean)
        self.layout1.addWidget(self.check_max)
        self.layout1.addWidget(self.check_min)
        self.layout1.addWidget(self.check_sum)
        self.layout1.addWidget(self.check_std)
        self.layout1.addWidget(self.check_var)
        self.layout1.addWidget(self.btn1)
        self.layout1.addItem(self.spacer)
        self.layout1.addWidget(self.credit)
       
        self.page1.setLayout(self.layout1)
        self.stackedLayout.addWidget(self.page1)
        
        #---------------------------------------
        
        self.page2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.l2 = QLabel("Data insights:")
        self.l2.setStyleSheet("font-size: 15px; font-weight: bold")
        self.l3 = QLabel("")
        self.l4 = QLabel("")
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)
        self.l5 = QLabel("Numerical attributes:")
        self.table = QTableWidget()
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.l6 = QLabel("Categorical attributes:")
        self.table2 = QTableWidget()
        self.back_btn = QPushButton("Go back")
        
        self.back_btn.clicked.connect(self.switchPage)
        
        self.layout2.addWidget(self.l2)
        self.layout2.addWidget(self.l3)
        self.layout2.addWidget(self.l4)
        self.layout2.addWidget(self.line1)
        self.layout2.addWidget(self.l5)
        self.layout2.addWidget(self.table)
        self.layout2.addWidget(self.line2)
        self.layout2.addWidget(self.l6)
        self.layout2.addWidget(self.table2)
        self.layout2.addWidget(self.back_btn)
        
        self.page2.setLayout(self.layout2)
        self.stackedLayout.addWidget(self.page2)
        
        self.setLayout(self.stackedLayout)
        
        
    def switchPage(self):
        # print(self.stackedLayout.currentIndex())
        self.stackedLayout.setCurrentIndex(0)
        self.l1.setText("Select needed measures:")
        self.l1.setStyleSheet("color : black")
    
    def get_data(self):
        
        measures = []
        
        if self.check_mean.isChecked():
            measures.append("mean")
        if self.check_max.isChecked():
            measures.append("max")
        if self.check_min.isChecked():
            measures.append("min")
        if self.check_sum.isChecked():
            measures.append("sum")
        if self.check_std.isChecked():
            measures.append("std")
        if self.check_var.isChecked():
            measures.append("var")
            
        if len(measures) == 0:
            self.l1.setText("Please select at leat one measure")
            self.l1.setStyleSheet("color : red")
            return
        
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
        
        self.stackedLayout.setCurrentIndex(1)
        
        rows_count = str(df.shape[0])
        col_count = str(df.shape[1])
        
        numeric_cols = []
        for index, value in df.dtypes.items():
            if value == "int64" or value == "float64":
                numeric_cols.append(index)
                
        if len(numeric_cols) == 1:
            end = ""
        else:
            end = "s"
                
        self.l3.setText("Dataset has " + rows_count + " rows and " + col_count + " columns, including " + str(len(numeric_cols)) + f" numeric attribute{end}.")
        self.l3.setWordWrap(True)
        
        nulls = int(df.isnull().sum().sum())
        if nulls == 1:
            end = ""
        else:
            end = "s"
        self.l4.setText("It has " + str(nulls) + f" missing value{end}.")
        
        t_rows = len(numeric_cols)
        t_cols = len(measures)
        
        def set_row_color(table, row_index):
            if row_index % 2 == 0:
                for column in range(table.columnCount()):
                    table.item(row_index, column).setBackground(QtGui.QColor("#ebecf0"))
        
        if t_rows == 0:
            self.line1.setParent(None)
            self.l5.setParent(None)
            self.table.setParent(None)
        else:
            self.table.setRowCount(t_rows)
            self.table.setColumnCount(t_cols)
            
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
                    if m == "sum":
                        table.setItem(row_id, col_id, QTableWidgetItem(str(round(df[f"{name}"].sum(), 2) )))
                    if m == "std":
                        table.setItem(row_id, col_id, QTableWidgetItem(str(round(df[f"{name}"].std(), 2) )))
                    if m == "var":
                        table.setItem(row_id, col_id, QTableWidgetItem(str(round(df[f"{name}"].var(), 2) )))
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
            self.table.horizontalHeader().setStyleSheet("::section{Background-color: #b8e2f2}")
            self.table.verticalHeader().setStyleSheet("::section{Background-color: #b8e2f2}") # ; font-weight: bold
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # ---------------------------------------------------------
        # table for category attributes
        category_cols = []
        for index, value in df.dtypes.items():
            if value != "int64" and value != "float64":
                category_cols.append(index)
        
        t2_rows = len(category_cols)
        t2_cols = 2
        
        if t2_rows == 0:
            self.line2.setParent(None)
            self.l6.setParent(None)
            self.table2.setParent(None)
        else:
            self.table2.setRowCount(t2_rows)
            self.table2.setColumnCount(t2_cols)
            
            for row_id , name in enumerate(category_cols):
                self.table2.setItem(row_id, 0, QTableWidgetItem(str(df[f"{name}"].nunique() )))
                self.table2.setItem(row_id, 1, QTableWidgetItem(str(df[f"{name}"].isna().sum() )))
                set_row_color(self.table2, row_id)
            
            self.table2.setVerticalHeaderLabels(category_cols)
            self.table2.setHorizontalHeaderLabels(["No. unique values", "Missing values"])
            self.table2.horizontalHeader().setStyleSheet("::section{Background-color: #fed8b1}")
            self.table2.verticalHeader().setStyleSheet("::section{Background-color: #fed8b1}") #; font-weight: bold
            self.table2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            
def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    


    
    
    


