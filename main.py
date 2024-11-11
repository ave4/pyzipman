#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QStringListModel
import zipfile
import os

class NoFile(QErrorMessage):
    def __init__(self):
        super().__init__()
        self.showMessage("ZIP-файл не открыт!", "warning")

class ExtractDialog(QDialog):
    def __init__(self, archive_path):
        super().__init__()
        self.archive_path = archive_path
        self.setAutoFillBackground(True)
        layout = QGridLayout()
        layout.addWidget(QLabel("Путь распаковки"), 0, 0)
        self.path_ext = QLineEdit(os.getcwd())
        layout.addWidget(self.path_ext, 1, 0)
        dir_button = QPushButton("Диалог")
        layout.addWidget(dir_button, 1, 1)
        dir_button.clicked.connect(self.file_dia)
        ext_button = QPushButton("Извлечь файлы")
        layout.addWidget(ext_button, 2, 0)
        ext_button.clicked.connect(self.extract_zip)
        self.setLayout(layout)

    def file_dia(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Путь распаковки архива", os.getcwd(), QFileDialog.ShowDirsOnly)
        self.path_ext.setText(dir_path)

    def extract_zip(self):
        if self.archive_path and self.path_ext.text():
            with zipfile.ZipFile(self.archive_path, "r") as zf:
                zf.extractall(self.path_ext.text())
            QMessageBox.information(self, "Успех", "Файлы успешно извлечены!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZIP Manager")
        self.setGeometry(100, 100, 600, 400)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.toolbar = self.addToolBar('MainToolBar')
        self.toolbar.setMovable(False)

        self.openAction = QAction(QIcon('icons/document-open.png'), 'Open Archive', self)
        self.openAction.triggered.connect(self.open_file)
        self.toolbar.addAction(self.openAction)

        self.extractAction = QAction(QIcon('icons/insert-object.png'), 'Extract Archive', self)
        self.extractAction.triggered.connect(self.extract_zip)
        self.toolbar.addAction(self.extractAction)

        self.addAction = QAction(QIcon('icons/list-add.png'), 'Add to Archive', self)
        self.addAction.triggered.connect(self.add_to_archive)
        self.toolbar.addAction(self.addAction)

        self.newAction = QAction(QIcon('icons/document-new.png'), 'New Archive', self)
        self.newAction.triggered.connect(self.create_new_archive)
        self.toolbar.addAction(self.newAction)

        self.exitAction = QAction(QIcon('icons/window-close.png'), 'Exit', self)
        self.exitAction.triggered.connect(sys.exit)
        self.toolbar.addAction(self.exitAction)

        grid = QGridLayout(self.widget)
        self.tree = QTreeView(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Files'])
        self.tree.setModel(self.model)
        grid.addWidget(self.tree)

        self.current_archive_path = None

    def open_file(self):
        self.current_archive_path, _ = QFileDialog.getOpenFileName(self, 'Выбрать zip-файл', '', 'ZIP Archive (*.zip *.jar);;Все файлы (*)')
        if self.current_archive_path:
            self.update_tree()

    def update_tree(self):
        if not self.current_archive_path:
            return
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Files'])
        with zipfile.ZipFile(self.current_archive_path, "r") as zf:
            for file_name in zf.namelist():
                items = file_name.split('/')
                parent = self.model.invisibleRootItem()
                for item in items:
                    if not item:
                        continue
                    found_items = [parent.child(i) for i in range(parent.rowCount()) if parent.child(i).text() == item]
                    if found_items:
                        parent = found_items[0]
                    else:
                        new_item = QStandardItem(item)
                        parent.appendRow(new_item)
                        parent = new_item

    def extract_zip(self):
        if not self.current_archive_path:
            NoFile()
        else:
            dialog = ExtractDialog(self.current_archive_path)
            dialog.exec_()

    def add_to_archive(self):
        if not self.current_archive_path:
            NoFile()
            return
        files, _ = QFileDialog.getOpenFileNames(self, 'Выберите файлы для добавления в архив')
        if files:
            with zipfile.ZipFile(self.current_archive_path, 'a') as zf:
                for file in files:
                    zf.write(file, os.path.basename(file))
            self.update_tree()

    def create_new_archive(self):
        new_archive_path, _ = QFileDialog.getSaveFileName(self, 'Создать новый zip-файл', '', 'ZIP Archive (*.zip)')
        if new_archive_path:
            if not new_archive_path.endswith('.zip'):
                new_archive_path += '.zip'
            self.current_archive_path = new_archive_path
            with zipfile.ZipFile(new_archive_path, 'w') as zf:
                pass
            self.update_tree()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
