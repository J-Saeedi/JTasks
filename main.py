from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
        QLineEdit, QDoubleSpinBox, QSlider, QTableWidget, \
        QTableWidgetItem, QLCDNumber, QFileDialog

from PyQt5 import uic
import sys
from PyQt5.QtCore import QEvent


class jtask_window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("JTasks.ui", self)

        self.add_this_item_button = self.findChild(QPushButton, "pushButtonAdd")
        self.add_this_item_button.clicked.connect(self.add_item)

        self.this_item_name = self.findChild(QLineEdit, "lineEditName")
        self.this_item_time = self.findChild(QDoubleSpinBox, "doubleSpinBox")
        self.this_item_priority = self.findChild(QSlider, "horizontalSlider")

        self.table = self.findChild(QTableWidget,"tableWidget")
        self.table.cellChanged.connect(self.calculate_sum)
        self.header = self.table.horizontalHeader()
        self.header.sortIndicatorChanged.connect(self.calculate_sum)
        self.table.clicked.connect(self.calculate_sum)
        self.move_up = self.findChild(QPushButton, "pushButtonUp")
        self.move_up.clicked.connect(self.up)
        self.move_down = self.findChild(QPushButton, "pushButtonDown")
        self.move_down.clicked.connect(self.down)

        self.sum_input = self.findChild(QDoubleSpinBox,"doubleSpinBox_sum")
        self.sum_input.valueChanged.connect(self.calculate_sum)
        self.sum_output = self.findChild(QLCDNumber,"lcdNumber")

        self.saveButton = self.findChild(QPushButton, "SaveButton")
        self.saveButton.clicked.connect(self.save_to_file)
        self.openButton = self.findChild(QPushButton, "OpenButton")
        self.openButton.clicked.connect(self.open_from_file)

        self.show()
    def add_item(self):
        item_name = self.this_item_name.text()
        item_time = self.this_item_time.text()
        item_priority = str(self.this_item_priority.value())
        print(item_name, item_time, item_priority)
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition, 0, QTableWidgetItem(item_name))
        self.table.setItem(rowPosition, 1, QTableWidgetItem(item_time))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(item_priority))
        self.calculate_sum()

    def signal_from_table(self, current, previous):
        print(current.row())
        if self.this_item_name.text() =="":
            self.move_up.setEnabled(False)
            print("-----")
        print("hahah")


    def check(self):
        print("it is ok")
        print(self.table.item(0,0).text())

    def up(self):
        old_index = self.table.currentRow()
        if old_index == 0:
            return None

        old_data = [self.table.item(old_index, i).text() for i in range(3)]
        old_neighbor = [self.table.item(old_index-1, i).text() for i in range(3)]
        new_index = old_index - 1
        new_data = [self.table.setItem(new_index, i, QTableWidgetItem(value)) for i,value in enumerate(old_data)]
        new_neighbor = [self.table.setItem(old_index, i, QTableWidgetItem(value))\
                            for i,value in enumerate(old_neighbor)]
        self.table.clearSelection()
        self.table.selectRow(new_index)
        self.calculate_sum()

    def down(self):
        old_index = self.table.currentRow()
        if old_index == self.table.rowCount()-1:
            return None

        old_data = [self.table.item(old_index, i).text() for i in range(3)]
        old_neighbor = [self.table.item(old_index+1, i).text() for i in range(3)]
        new_index = old_index + 1
        new_data = [self.table.setItem(new_index, i, QTableWidgetItem(value)) for i,value in enumerate(old_data)]
        new_neighbor = [self.table.setItem(old_index, i, QTableWidgetItem(value))\
                            for i,value in enumerate(old_neighbor)]
        self.table.clearSelection()
        self.table.selectRow(new_index)
        self.calculate_sum()

    def calculate_sum(self):
        sum = 0
        for i in range(int(self.sum_input.text())):
            try:
                sum += float(self.table.item(i,1).text())
            except:
                pass
        self.sum_output.display(float(sum))


    def save_to_file(self):
        row_counts = self.table.rowCount()
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save to File","","JCSV Files (*.j.csv)", options=options)
        if not fileName:
            return # exit the function
        with open(fileName, 'w') as f:
            for i in range(row_counts):
                f.write(",".join([self.table.item(i,0).text(), \
                            self.table.item(i,1).text(), \
                            self.table.item(i,2).text()  ])+"\n")

    def open_from_file(self):
        new_row_index = self.table.rowCount()
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Save to File","","JCSV Files (*.j.csv)", options=options)
        if not fileName:
            return # exit the function
        with open(fileName, 'r') as f:
            for this_row in f.readlines():
                if this_row.strip():
                    this_data = this_row.strip().split(",")
                    print(this_data)
                    self.table.insertRow(new_row_index)
                    self.table.setItem(new_row_index, 0, QTableWidgetItem(this_data[0]))
                    self.table.setItem(new_row_index, 1, QTableWidgetItem(this_data[1]))
                    self.table.setItem(new_row_index, 2, QTableWidgetItem(this_data[2]))
                    new_row_index += 1

app = QApplication(sys.argv)
window = jtask_window()
sys.exit(app.exec_())
