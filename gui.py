import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QCheckBox


from PyQt6.QtGui import QAction, QIcon, QPixmap, QGuiApplication
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
        self.label = QLabel(self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        # self.area.setWidget(self.label)
        self.button = QPushButton('Save as')
        self.plus_button = QPushButton('+')
        self.plus_button.setFixedSize(QSize(24, 24))
        self.plus_button.clicked.connect(self.increase_scale)
        self.minus_button = QPushButton('-')
        self.minus_button.setFixedSize(QSize(24, 24))
        self.minus_button.clicked.connect(self.decrease_scale)

        self.text_edit = QLineEdit(self)
        # self.text_edit.setMinimumWidth(10)
        # self.text_edit.setMaximumWidth(20)
        self.text_edit.setFixedWidth(42)
        # self.text_edit.textChanged.connect(self.change_image)
        self.text_edit.editingFinished.connect(self.change_image)
        # print(self.text_edit.width())
        # print(*dir(self.text_edit), sep='\n')
        self.persentage = QLabel(self, text='%')
        hbox = QHBoxLayout()
        hbox.addWidget(self.button)
        hbox.addWidget(self.minus_button)
        hbox.addWidget(self.text_edit)
        hbox.addWidget(self.persentage)
        hbox.addWidget(self.plus_button)
        hbox.addStretch(1)
        # print(*dir(hbox), sep='\n')
        # self.button.resize(100, 100)
        self.button.clicked.connect(self.saveFileDialog)
        
        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.area)
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        
        # self.setMinimumSize(200, 200)
        # self.setMaximumSize(800, 800)
        self.setWindowTitle('Hello!')
        self.show()

    def increase_scale(self):
        try:
            value = float(self.text_edit.text())
            value += 25
            self.scale = value/100.0
        except ValueError:
            value = self.scale*100.0
        self.text_edit.setText(f'{value:.1f}')
        self.scale_pixmap(value/100)


    def decrease_scale(self):
        try:
            value = float(self.text_edit.text())
            value -= 25
            self.scale = value/100.0
        except ValueError:
            value = self.scale*100
        if value <= 0:
            value = 1.0
        self.text_edit.setText(f'{value:.1f}')
        self.scale_pixmap(value/100)



    # def greet(self):
    #     print('Hello!')
    #     self.load_image('grayscale_test.png')
    def scale_pixmap(self, scale):
        scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*scale), int(self.pixmap.height()*scale)))
        self.label.setPixmap(scaled)


    def change_image(self):
        print(self.text_edit.text())
        try:
            scale = float(self.text_edit.text())/100.0
            scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*scale), int(self.pixmap.height()*scale)))
            self.label.setPixmap(scaled)
            self.scale = scale
        except ValueError:
            scale = self.scale
        self.text_edit.setText(f'{scale*100:.1f}')
        

    def load_image(self, filename):
        self.setWindowTitle(filename)
        self.filename = filename
        self.pixmap = QPixmap(filename)
        print(self.text_edit.height())
        # scaled = pixmap.scaled(QSize(pixmap.width()//2, pixmap.height()//2))
        # scaled = self.pixmap.scaled(QSize(self.pixmap.width(), self.pixmap.height()))
        
        avail_geom = QGuiApplication.primaryScreen().availableSize()
        avail_width = avail_geom.width()
        avail_height = avail_geom.height()
        k_window = 0.9
        init_window_width = avail_width*k_window    # add int() maybe
        init_window_height = avail_height*k_window  # add int() maybe

        k_image = 0.93
        k_w_image = init_window_width * k_image / self.pixmap.width()
        k_h_image = init_window_height * k_image / self.pixmap.height()
        k_min_image = min(k_w_image, k_h_image)

        if k_min_image >= 1.0:
            self.setGeometry(100, 100, int(self.pixmap.width()/k_image), int(self.pixmap.height()/k_image))
            self.text_edit.setText('100.0')
            self.label.setPixmap(self.pixmap)
            self.scale = 1
        else:
            self.setGeometry(100, 100, int(init_window_width), int(init_window_height))
            scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*k_min_image), int(self.pixmap.height()*k_min_image)))
            self.text_edit.setText(f'{k_min_image*100:.1f}')
            self.label.setPixmap(scaled)
            self.scale = k_min_image
        self.area.setWidget(self.label)
        

        # print(f'{self.frameGeometry() = }')
        # print(f'{self.geometry() = }')
        # print(k_min, k_h, k_w)
        # self.setGeometry(100, 100, int(avail_width*0.9), int(avail_height*0.9))
        # self.setGeometry(100, 100, int(self.pixmap.width()/k), int(self.pixmap.height()/k))
        
    def saveFileDialog(self):
        # dialog = QFileDialog()
        # dialog.setNameFilter('*.png, *.jpg, *.bmp')
        # dialog.exec()
        # filename = dialog.getSaveFileName(self, 'Save file', '*.png, *.jpg, *.bmp')
        # filename = QFileDialog.getSaveFileName(self, 'Save file', self.filename, 'Images (*.png, *.jpg, *.bmp)')
        filename, ext = QFileDialog.getSaveFileName(self, 'Save file', '.', '*.png;;*.jpg;;*.bmp')
        new_filename = f'{filename}.{ext[2:]}' 
        print(new_filename)
        self.pixmap.save(new_filename, quality=-1)
        # self.label.resize(600, 600)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.child_windows = []

        # print(f'{QGuiApplication.primaryScreen().availableGeometry() = }')
        # print(f'{QGuiApplication.primaryScreen().geometry() = }')
        # print(f'{QGuiApplication.primaryScreen().size() = }')
        # print(f'{QGuiApplication.primaryScreen().model() = }')
        # print(f'{QGuiApplication.primaryScreen().name() = }')
        # print(f'{QGuiApplication.primaryScreen().manufacturer() = }')
        # print(f'{QGuiApplication.primaryScreen().serialNumber() = }')
        # print(f'{QGuiApplication.primaryScreen().physicalSize() = }')
        # print(f'{QGuiApplication.primaryScreen().refreshRate() = }')
        # print(f'{QGuiApplication.primaryScreen().availableVirtualSize() = }')
        # print(f'{QGuiApplication.primaryScreen().availableVirtualGeometry() = }')


    def initUI(self):

        self.open_button = QPushButton(self)
        self.open_button.setText('Open file(s)')
        self.open_button.clicked.connect(self.showDialog)

        self.slideshow_checkbox = QCheckBox(self)
        self.slideshow_checkbox.setText('Slideshow')
        self.slideshow_checkbox.clicked.connect(self.test)

        hbox = QHBoxLayout()
        hbox.addWidget(self.open_button)
        hbox.addWidget(self.slideshow_checkbox)
        hbox.addStretch(1)


        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.vbox = vbox

        container = QWidget(self)
        container.setLayout(vbox)
        self.setCentralWidget(container)



        # self.textEdit = QTextEdit()
        # # self.setCentralWidget(self.textEdit)
        # self.statusBar()

        # self.label = QLabel()
        # self.button = QPushButton('Add tab')
        # self.button.clicked.connect(self.add_tab)
        # self._page = 3
        # layout = QVBoxLayout()

        # self.form_button = QPushButton('Create window!')
        # self.form_button.clicked.connect(self.create_window)

        # openFile = QAction(QIcon('open.png'), 'Open', self)
        # openFile.setShortcut('Ctrl+O')
        # openFile.setStatusTip('Open new File')
        # openFile.triggered.connect(self.showDialog)

        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(openFile)

        # self.tabs = QTabWidget()
        # self.tabs.addTab(QWidget(), 'First tab')
        # self.tabs.addTab(QWidget(), 'Second tab')
        # self.tabs.addTab(QWidget(), 'Third tab')
        # self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        # self.tabs.setTabsClosable(True)
        # self.tabs.setMovable(True)

        # layout.addWidget(self.button)
        # layout.addWidget(self.label)
        # layout.addWidget(self.textEdit)
        # layout.addWidget(self.tabs)
        # layout.addWidget(self.form_button)

        # self.open_button = QPushButton('Open file(s)')
        # self.open_button.clicked.connect(self.showDialog)
        # layout.addWidget(self.open_button)

        # container = QWidget()
        # container.setLayout(layout)

        # self.setCentralWidget(container)

        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Raw data to image')
        self.show()

    def test(self):
        if self.slideshow_checkbox.isChecked():
            self.period_hbox = QHBoxLayout()
            self.led = QLineEdit(self)
            self.led.setText('1')

            self.lbl = QLabel(self)
            self.lbl.setText('s')
            self.period_hbox.addWidget(self.led)
            self.period_hbox.addWidget(self.lbl)
            self.period_hbox.addStretch(1)
            self.vbox.insertLayout(1, self.period_hbox)

            # self.vbox.addWidget(self.led)
            # self.vbox.addStretch(1)
        else:
            self.period_hbox.deleteLater()
            self.led.deleteLater()
            self.lbl.deleteLater()


    def add_tab(self):
        self._page += 1
        tab = Widget(self._page)      # QWidget(self)

        self.tabs.addTab(tab, f"tab {self._page}") 

    def showDialog(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '.')[0]
        # self.textEdit.setText('\n'.join(fnames))
        for f in fnames:
            child_window = ChildWindow()
            child_window.load_image(f)
            self.child_windows.append(child_window)
        # f = open(fname, 'r')

        # with f:
        #     data = f.read()
        #     self.textEdit.setText(data)



    def create_window(self):
        child_window = ChildWindow()
        self.child_windows.append(child_window)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())