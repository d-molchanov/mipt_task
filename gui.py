import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFileDialog


from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.statusBar()

        self.label = QLabel()
        self.button = QPushButton()

        layout = QVBoxLayout()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '/home')[0]
        self.textEdit.setText('\n'.join(fnames))
        # f = open(fname, 'r')

        # with f:
        #     data = f.read()
        #     self.textEdit.setText(data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())