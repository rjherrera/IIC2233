from datetime import datetime
from PyQt4 import QtGui
from threading import Thread
from dropbox.files import FolderMetadata
from PyQt4.QtCore import QThread, pyqtSignal


def get_size_string(size):
    '''Normalizes the size that comes in Bytes, to
    human readable string.'''
    if size < 1000:
        return '%.3f B' % (size)
    elif size < 1000000:
        return '%.3f KB' % (size / 10e2)
    elif size < 1000000000:
        return '%.3f MB' % (size / 10e5)
    elif size < 1000000000000:
        return '%.3f GB' % (size / 10e8)


class HistoryThread(QThread):
    '''Personalized Qthread with signal to let the app now when its ready'''

    signal = pyqtSignal(str)

    def run(self):
        try:
            files = self.dbx.files_list_folder(self.path, recursive=True)
            max_date = datetime.min
            max_file = None
            size = 0
            for i in files.entries:
                if hasattr(i, 'client_modified'):
                    if (i.client_modified > max_date or
                            i.server_modified > max_date):
                        max_date = max(i.client_modified, i.server_modified)
                        max_file = i
                        size += i.size
            string = 'Last modification: %s\n' % str(max_date)
            string += 'Modification made in file "%s" located in "%s"\n' % (
                max_file.name,
                max_file.path_lower.strip(max_file.name.lower()))
            string += 'Folder size: %s' % get_size_string(size)
            self.signal.emit(string)
        except:
            self.labelError.setText('History error')


class PathDialog(QtGui.QDialog):
    '''Custom dialog with custom widgets on it. It is used
    for the selection of the destination path for moving elements'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 300)
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setRange(0, 1)
        self.progressBar.setTextVisible(False)
        self.labelTask = QtGui.QLabel('')
        self.labelError = QtGui.QLabel('')
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabel('Folders')
        self.pushButton = QtGui.QPushButton('Select destination')
        self.pushButton.clicked.connect(self.submit)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.treeWidget, 0, 0, 1, 6)
        layout.addWidget(self.labelTask, 1, 0, 1, 1)
        layout.addWidget(self.progressBar, 1, 1, 1, 5)
        layout.addWidget(self.pushButton, 2, 0, 1, 3)
        layout.addWidget(self.labelError, 2, 3, 1, 3)
        self.setLayout(layout)

    def submit(self):
        items = self.treeWidget.selectedItems()
        if items:
            self.result = items[0]
            self.accept()
        else:
            self.labelError.setText('You must select a folder')

    def get_result(self):
        return self.result.path

    def load_items(self):
        Thread(target=self.load_tree, daemon=True).start()

    def load_tree(self):
        self.labelTask.setText('Getting folders:')
        self.progressBar.setRange(0, 0)
        tree = self.treeWidget
        self.root_item = QtGui.QTreeWidgetItem(['Dropbox files'])
        self.root_item.is_root = True
        self.root_item.path = ''
        self.root_item.is_folder = True
        tree.addTopLevelItem(self.root_item)
        self.root_item.setExpanded(True)
        top_tree_items = []
        try:
            dirs = self.dbx.files_list_folder('')
            for i in dirs.entries:
                if isinstance(i, FolderMetadata):
                    item = QtGui.QTreeWidgetItem([i.name])
                    item.path = i.path_lower
                    item.file = i
                    item.is_folder = True
                    top_tree_items.append(item)
            self.root_item.addChildren(top_tree_items)
            self.fill_tree(dirs, top_tree_items)
        except:
            self.labelError.setText('Loading error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Ready.')

    def fill_tree(self, files_folders, top_items):
        folders = [i for i in files_folders.entries
                   if isinstance(i, FolderMetadata)]
        for i in range(len(folders)):
            direc = folders[i]
            if isinstance(direc, FolderMetadata):
                new_top_items = []
                subd = self.dbx.files_list_folder(direc.path_lower)
                item = top_items[i]
                for i in subd.entries:
                    if isinstance(i, FolderMetadata):
                        n_item = QtGui.QTreeWidgetItem([i.name])
                        n_item.path = i.path_lower
                        n_item.file = i
                        n_item.is_folder = True
                        new_top_items.append(n_item)
                item.addChildren(new_top_items)
                self.fill_tree(subd, new_top_items)
