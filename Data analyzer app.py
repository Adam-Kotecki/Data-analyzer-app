from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, \
QFileDialog, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5 import QtCore , QtWidgets
import sys
import pandas as pd

class Window(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Data analyzer")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.btn1 = QPushButton("Select file")
        self.btn1.clicked.connect(self.get_data)
        layout.addWidget(self.btn1)
        self.setLayout(layout)
        
        # self.l1 = QLabel("Select category of data:")

    def get_data(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Hey! Select a File')
        file = path[0]
        try:
            df = pd.read_csv(file)
        except:
            msg = QMessageBox()
            msg.setText("Something went wrong. Please make sure that selected file have correct format.")
            msg.setWindowTitle("Error")
            msg.exec()
            return
        print("success")
        rows_count = str(df.shape[0])
        col_count = str(df.shape[1])
        print("Dataset has " + rows_count + " rows and " + col_count + " columns")
        print(type(df.dtypes))
        
        print("----------------------------------------")
        numeric_cols = []
        for index, value in df.dtypes.items():
            if value == "int64" or value == "float64":
                numeric_cols.append(index)
        
        for name in numeric_cols:
            print("mean of " + f"{name}" + " " + str(df[f"{name}"].mean()))
            print("sum of " + f"{name}" + " " + str(df[f"{name}"].sum()))
            print("Standard Deviation of " + f"{name}" + " " + str(df[f"{name}"].std()))
        
                
def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()