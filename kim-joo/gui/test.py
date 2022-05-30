import sys
# import numpy as np
from PyQt5.QtWidgets import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)

        self.clearBtn = QPushButton('Clear')
        self.clearBtn.clicked.connect(self.tableWidget.clear)

        self.scrollToTop = QPushButton('Scroll to Top')
        self.scrollToTop.clicked.connect(self.tableWidget.scrollToTop)

        self.scrollToBottom = QPushButton('Scroll to Bottom')
        self.scrollToBottom.clicked.connect(self.tableWidget.scrollToBottom)

        '''
        rand_items = np.random.randint(1, 100, size=(20, 4))

        for i in range(20):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(rand_items[i, j])))
        '''

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.clearBtn)
        layout.addWidget(self.scrollToTop)
        layout.addWidget(self.scrollToBottom)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5 - QTableWidget')
        self.setGeometry(300, 100, 600, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())