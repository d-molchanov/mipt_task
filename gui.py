import sys
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QApplication


from PyQt6.QtGui import QAction, QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '/home')[0]
        self.textEdit.setText(str(fnames))
        # f = open(fname, 'r')

        # with f:
        #     data = f.read()
        #     self.textEdit.setText(data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())