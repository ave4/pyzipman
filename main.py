#!/usr/bin/env python
import sys
#from PySide6.QtCore import *
#from PySide6.QtWidgets import *
from PyQt5.Qt import *
import zipfile

new_file = None

#class OpenFile(QDialog):
#        def __init__(self, formats):
#                super().__init__()
#                self.fileName = QFileDialog.getOpenFileName(self,
#    "Open Archive", "/home/", "ZIP Files (*.jar *.zip)"))

class NoFile(QErrorMessage):
        def  __init__(self):
                super().__init__()
                self.showMessage("ZIP-файл не открыт!", "warning")

class ExtractDialog(QDialog):
        def  __init__(self):
                super().__init__()
                self.setAutoFillBackground(True)
                layout = QGridLayout()
                layout.addWidget(QLabel("Путь распаковки"),0,0)
                self.path_ext = QLineEdit("/")
                layout.addWidget(self.path_ext, 1,0)
                dir_button = QPushButton("Диалог")
                layout.addWidget(dir_button, 1,1)
                dir_button.clicked.connect(self.file_dia)
                ext_button = QPushButton("Излечь файлы")
                layout.addWidget(ext_button, 2,0)
                ext_button.clicked.connect(self.extract_zip)
                self.setLayout(layout)
        def file_dia(self):
                dir_path = QFileDialog.getExistingDirectory(None, "Путь распаковки архива", "", QFileDialog.ShowDirsOnly)
                print(dir_path)
                self.path_ext.setText(dir_path)
        def extract_zip(self):
                if (new_file and self.path_ext.text()):
                        with zipfile.ZipFile(new_file, "r") as zf:
                                zf.extractall(self.path_ext.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZIP Manager")

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.exitAction = QAction(QIcon('window-close.png'), 'Exit', self)
        self.exitAction.triggered.connect(app.quit)
        self.openAction = QAction(QIcon('document-open.png'), 'Open Archive', self)
        self.extrAction = QAction(QIcon('insert-object.png'), 'Extract Archive', self)
        self.addAction = QAction(QIcon('list-add.png'), 'Add to Archive', self)
        self.openAction.triggered.connect(self.open_file)
        self.extrAction.triggered.connect(self.extract_zip)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setObjectName('toolbar')
        #self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.extrAction)
        self.toolbar.addAction(self.addAction)
        self.toolbar.addAction(self.exitAction)
        grid = QGridLayout(self.widget)
        self.tree = QListView(self)
        grid.addWidget(self.tree)
        self.w = None
        

    def open_file(self):
        global new_file
        new_file = QFileDialog.getOpenFileName(None, 'Выбрать zip-файл', '',
                                               'ZIP Archive (*.zip *.jar);;Все файлы (*)')[0]
        if (new_file):
                with zipfile.ZipFile(new_file, "r") as zf:
                        self.update_tree(zf.namelist())
    def update_tree(self, zlist):
        print(zlist)
        self.model_1 = QStringListModel(self)
        self.model_1.setStringList(zlist)
        self.tree.setModel(self.model_1)
        #tree = QTreeView
    def extract_zip(self):
        #dlayout = QGridLayout()
        #dlayout.addWidget(QLabel("Путь распаковки"), 0, 0)
        #diawindow = QDialog()
        #diawindow.setLayout(dlayout)
        #self.w = ExtractDialog()
        if self.w is None:
                if new_file is None:
                        eras = QErrorMessage(parent=self)
                        eras.showMessage("ZIP-файл не открыт!", "warning")
                else:
                        self.w = ExtractDialog()
                        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
