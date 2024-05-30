import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QScrollArea


from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class Widget(QWidget):
    def __init__(self, page):
        super().__init__()
        
        # self.label = QLabel(f'Page {page}', alignment = Qt.AlignCenter)
        self.label = QLabel(f'Page {page}')
        self.label.setStyleSheet("QLabel {color: #1E5F74; font: 20pt;}")
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)

class ChildWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel()
        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        self.area.setWidget(self.label)
        self.button = QPushButton('Hello!')
        self.plus_button = QPushButton('+')
        self.plus_button.setFixedSize(QSize(24, 24))
        self.minus_button = QPushButton('-')
        self.minus_button.setFixedSize(QSize(24, 24))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addWidget(self.plus_button)
        hbox.addWidget(self.minus_button)
        # self.button.resize(100, 100)
        self.button.clicked.connect(self.greet)
        
        layout = QVBoxLayout()
        layout.addWidget(self.area)
        layout.addWidget(self.label)
        layout.addLayout(hbox)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setGeometry(300, 300, 350, 300)
        # self.setMinimumSize(200, 200)
        # self.setMaximumSize(800, 800)
        self.setWindowTitle('Hello!')
        self.show()


    def greet(self):
        print('Hello!')
        self.load_image('grayscale_test.png')

    def load_image(self, filename):
        pixmap = QPixmap(filename)
        # scaled = pixmap.scaled(QSize(pixmap.width()//2, pixmap.height()//2))
        scaled = pixmap.scaled(QSize(pixmap.width()*2, pixmap.height()*2))
        self.label.setPixmap(scaled)
        # self.label.resize(600, 600)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.windows = []
        self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.statusBar()

        self.label = QLabel()
        self.button = QPushButton('Add tab')
        self.button.clicked.connect(self.add_tab)
        self._page = 3
        layout = QVBoxLayout()

        self.form_button = QPushButton('Create window!')
        self.form_button.clicked.connect(self.create_window)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), 'First tab')
        self.tabs.addTab(QWidget(), 'Second tab')
        self.tabs.addTab(QWidget(), 'Third tab')
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.tabs)
        layout.addWidget(self.form_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Raw data to image')
        self.show()

    def add_tab(self):
        self._page += 1
        tab = Widget(self._page)      # QWidget(self)

        self.tabs.addTab(tab, f"tab {self._page}") 

    def showDialog(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '/')[0]
        self.textEdit.setText('\n'.join(fnames))
        # f = open(fname, 'r')

        # with f:
        #     data = f.read()
        #     self.textEdit.setText(data)

    def create_window(self):
        child_window = ChildWindow()
        self.windows.append(child_window)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())