from dropbox.files import FolderMetadata
from dropbox import DropboxOAuth2FlowNoRedirect
from utils import *
from threading import Thread
from PyQt4 import QtGui, QtCore, uic
from os import listdir, mkdir, remove

APP_KEY = 'zkiaxcf0wxznl0a'
APP_SECRET = 'o122g6x79gbg1a8'


login_form = uic.loadUiType("login_widget.ui")
options_form = uic.loadUiType("options_widget.ui")


class widgetLogin(login_form[0], login_form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        url = self.auth_flow.start()
        self.webView.load(QtCore.QUrl(url))


class widgetOptions(options_form[0], options_form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.top_tree_items = []
        self.old_items = []
        self.thread = Thread(target=self.load_tree, daemon=True)

        # This enables the ability to right click in the tree
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.item_menu)

        # This enables the button callback so that the user can logout
        self.pushButtonLogout.clicked.connect(self.logout)

        # Thread to emit signal
        self.h_thread = HistoryThread()
        self.h_thread.signal.connect(self.get_history_helper)

    def item_menu(self, pos):
        self.labelError.setText('')
        indexes = self.treeWidget.selectedIndexes()
        if not indexes:
            return
        item = self.treeWidget.itemFromIndex(indexes[0])
        if hasattr(item, 'is_root'):
            self.ask_root(item, pos)
        elif item.is_folder:
            self.ask_folder(item, pos)
        else:
            self.ask_file(item, pos)

    def ask_root(self, item, pos):
        menu = QtGui.QMenu()
        menu.addAction('Upload file to root',
                       lambda: self.upload(item))
        menu.exec_(self.treeWidget.viewport().mapToGlobal(pos))

    def ask_folder(self, item, pos):
        menu = QtGui.QMenu()
        menu.addAction('Download folder',
                       lambda: self.download(item))
        menu.addAction('Upload file to folder',
                       lambda: self.upload(item))
        menu.addAction('Change folder name',
                       lambda: self.rename(item))
        menu.addAction('Move folder',
                       lambda: self.move(item))
        menu.addAction('See folder\'s information and history',
                       lambda: self.get_history(item))
        menu.addAction('Create new folder',
                       lambda: self.create_folder(item))
        menu.addAction('Delete folder',
                       lambda: self.delete(item))
        menu.exec_(self.treeWidget.viewport().mapToGlobal(pos))

    def ask_file(self, item, pos):
        menu = QtGui.QMenu()
        menu.addAction('Download file',
                       lambda: self.download(item))
        menu.addAction('Change file name',
                       lambda: self.rename(item))
        menu.addAction('Move file',
                       lambda: self.move(item))
        menu.addAction('See file\'s information and history',
                       lambda: self.get_history(item))
        menu.addAction('Create new folder',
                       lambda: self.create_folder(item))
        menu.addAction('Delete file',
                       lambda: self.delete(item))
        menu.exec_(self.treeWidget.viewport().mapToGlobal(pos))

    def download(self, item):
        '''Downloads the desired element to PC, and to do so
        it asks the user for a destination, if the element is a folder
        it will ask for a directory into which it will be downloaded'''
        if item.is_folder:
            download_name = item.file.name
            save_path = QtGui.QFileDialog.getExistingDirectory(
                self, 'Choose directory for ' + download_name)
            if save_path:
                Thread(target=self.download_folder_helper, daemon=True,
                       args=(save_path, item.path, download_name)).start()
        else:
            download_name = item.file.name
            save_path = QtGui.QFileDialog.getSaveFileName(
                self, 'Download ' + download_name, download_name)
            if save_path:
                Thread(target=self.download_helper, daemon=True,
                       args=(save_path, item.path)).start()

    def download_folder_helper(self, save_path, online_path, folder_name):
        self.progressBar.setRange(0, 0)
        self.labelTask.setText('Downloading:')
        try:
            files = self.dbx.files_list_folder(online_path)
            # Make sure the folder name is available in user directory
            # if not, modify it to be: "name (iterations)"
            i = 1
            new_folder_name = folder_name
            while new_folder_name in listdir(save_path):
                new_folder_name = folder_name + ' (%d)' % i
                i += 1
            route = save_path + '/' + new_folder_name
            mkdir(route)
            self.recursive_download(route, files)
        except:
            self.labelError.setText('Download error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def recursive_download(self, route, files):
        '''Downloads every file in the folder, along
        with creating any subdirectories for it to make
        sense'''
        for i in files.entries:
            if isinstance(i, FolderMetadata):
                new_route = route + '/' + i.name
                mkdir(new_route)
                new_files = self.dbx.files_list_folder(i.path_lower)
                self.recursive_download(new_route, new_files)
            else:
                self.dbx.files_download_to_file(
                    route + '/' + i.name, i.path_lower)

    def download_helper(self, save_path, online_path):
        self.progressBar.setRange(0, 0)
        self.labelTask.setText('Downloading:')
        try:
            self.dbx.files_download_to_file(save_path, online_path)
        except:
            self.labelError.setText('Download error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def upload(self, item):
        '''Uploads to the desired folder any item on the user\'s PC,
        it asks for the file with a QFileDialog'''
        online_folder_path = item.path
        local_file_path = QtGui.QFileDialog.getOpenFileName(
            self, 'Upload file', '')
        if local_file_path:
            with open(local_file_path, 'rb') as file:
                file_name = local_file_path.split('/')[-1]
                online_file_path = online_folder_path + '/' + file_name
                Thread(
                    target=self.upload_helper, daemon=True,
                    args=(file.read(), file_name, online_file_path, item)
                ).start()

    def upload_helper(self, file_data, file_name, online_path,
                      item, autorename=True):
        self.progressBar.setRange(0, 0)
        self.labelTask.setText('Uploading:')
        try:
            self.dbx.files_upload(file_data, online_path,
                                  autorename=autorename)
            n_item = QtGui.QTreeWidgetItem([file_name])
            n_item.path = online_path.lower()
            n_item.file = self.dbx.files_get_metadata(online_path)
            n_item.is_folder = False
            item.addChild(n_item)
        except Exception as e:
            print(e)
            self.labelError.setText('Upload error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def rename(self, item):
        '''Changes the name of a file or folder by using the
        dropbox move method. Once changed, it modifies the item
        in the tree, along whith retrieving the metadata again.'''
        item_type = 'folder' if item.is_folder else 'file'
        extension_disclaimer = ('(Remember to include the file extension)'
                                if not item.is_folder else '')
        new_name, ok = QtGui.QInputDialog.getText(
            self, 'New %s\'s name' % item_type,
            'Enter the new name for this %s:\n%s' % (
                item_type, extension_disclaimer))
        if ok:
            super_path = '/'.join(item.path.split('/')[:-1])
            new_path = super_path + '/' + new_name
            Thread(target=self.rename_helper, daemon=True,
                   args=(item, new_path, new_name, super_path)).start()

    def rename_helper(self, item, new_path, new_name, super_path):
        self.progressBar.setRange(0, 0)
        self.labelTask.setText('Renaming:')
        try:
            self.dbx.files_move(item.path, new_path)
            item.setText(0, new_name)
            item.file = self.dbx.files_get_metadata(new_path)
            item.path = new_path
            if item.is_folder:
                # here we update the childs so that the files and
                # folders inside the renamed folder don't remain
                # with the old paths, and generate conflicts
                item.takeChildren()
                Thread(target=self.update_subdirs, daemon=True,
                       args=(super_path, new_path, item)).start()
        except:
            self.labelError.setText('Rename error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def update_subdirs(self, super_path, new_path, item):
        '''Similar to "fill_tree" or "load_tree" methods but
        for an specific directory'''
        files_folders = self.dbx.files_list_folder(super_path)
        files_folders = [i for i in files_folders.entries if
                         new_path.lower() == i.path_lower]
        # The next lines were made to keep the format
        # as the method "fill_tree" works with an object
        # that has an attribute "entries", so as the list was modified
        # a new object must be made with that attribute.
        f = type('', (), {})()
        f.entries = files_folders
        Thread(target=self.fill_tree, daemon=True, args=(f, [item])).start()

    def move(self, item):
        '''Moves the desired element to a new location, it
        prompts the user with an special dialog asking
        for the destination'''
        dialog = PathDialog()
        dialog.dbx = self.dbx
        dialog.load_items()
        if dialog.exec_():
            destination = dialog.get_result()
            destination += '/' + item.file.name
            Thread(target=self.move_helper, daemon=True,
                   args=(item.path, destination, item)).start()

    def move_helper(self, from_path, to_path, item):
        self.progressBar.setRange(0, 0)
        try:
            self.dbx.files_move(from_path, to_path)
            # if you loose the reference to this widget
            # PyQt raises an error, so its moved to a "trash" list.
            self.old_items.append(self.treeWidget.takeTopLevelItem(0))
            self.top_tree_items = []
            self.root_item = None
            # Loads the whole tree again
            Thread(target=self.load_tree, daemon=True).start()
        except:
            self.labelError.setText('Move error')
        self.progressBar.setRange(0, 1)

    def get_history(self, item):
        '''Gets the history of the file or folder by searching
        the metadata of each element, which was stored while
        loading the tree. It calls an special QThread so that
        it is able to use signals, and avoid freezing the program
        while executing this task.'''
        self.labelTask.setText('Getting history:')
        if item.is_folder:
            # In this case threading.Thread cant be used cause
            # of the need to emit a signal as the information is
            # retrieved because QMessageBox cannot be used outside
            # the main thread, so it must be triggered by a signal.
            self.h_thread.path = item.path
            self.h_thread.dbx = self.dbx
            self.progressBar.setRange(0, 0)
            self.h_thread.start()
        else:
            c_mod = str(item.file.client_modified)
            s_mod = str(item.file.server_modified)
            string = 'Last modification on server: %s\n' % s_mod
            string += 'Last modification on client: %s\n' % c_mod
            string += 'File size: %s' % get_size_string(item.file.size)
            QtGui.QMessageBox.information(
                self, 'History', string, QtGui.QMessageBox.Ok)

    def get_history_helper(self, string):
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')
        QtGui.QMessageBox.information(
            self, 'History', string, QtGui.QMessageBox.Ok)

    def create_folder(self, item):
        '''Creates folder in the item\'s directory, it
        prompts for a name for the folder'''
        new_name, ok = QtGui.QInputDialog.getText(
            self, 'New folder name',
            'Enter the name for this new folder:')
        if ok:
            super_path = '/'.join(item.path.split('/')[:-1])
            new_path = super_path + '/' + new_name
            Thread(target=self.create_folder_helper, daemon=True,
                   args=(new_path, new_name, item)).start()

    def create_folder_helper(self, new_path, new_name, item):
        self.progressBar.setRange(0, 0)
        self.labelTask.setText('Creating:')
        try:
            self.dbx.files_create_folder(new_path)
            n_item = QtGui.QTreeWidgetItem([new_name])
            n_item.path = new_path.lower()
            n_item.file = self.dbx.files_get_metadata(new_path)
            n_item.is_folder = True
            item.parent().addChild(n_item)
        except:
            self.labelError.setText('Create folder error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def delete(self, item):
        '''Deletes the item selected by the user, it also prompts
        a warning so the user does not delete anything by accident'''
        item_type = 'folder' if item.is_folder else 'file'
        disclaimer = ('(This will delete everything inside this folder)'
                      if item.is_folder else '')
        message = 'Dou you really want to delete this %s: %s\n%s' % (
            item_type, item.file.name, disclaimer)
        ans = QtGui.QMessageBox.question(
            self,
            'Delete %s' % item_type,
            message,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if ans == QtGui.QMessageBox.Yes:
            Thread(target=self.delete_helper, daemon=True,
                   args=(item, item_type)).start()

    def delete_helper(self, item, item_type):
        self.labelTask.setText('Deleting:')
        self.progressBar.setRange(0, 0)
        try:
            self.dbx.files_delete(item.path)
            item.takeChildren()
            item.parent().removeChild(item)
        except:
            self.labelError.setText('Delete %s error' % item_type)
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def load_tree(self):
        '''Initial loading of the tree, it starts filling the tree
        with elements, and calls the recursive method "fill_tree"'''
        self.labelTask.setText('Loading:')
        self.progressBar.setRange(0, 0)
        tree = self.treeWidget
        self.root_item = QtGui.QTreeWidgetItem(['Dropbox files'])
        self.root_item.is_root = True
        self.root_item.path = ''
        self.root_item.is_folder = True
        tree.addTopLevelItem(self.root_item)
        self.root_item.setExpanded(True)
        try:
            dirs = self.dbx.files_list_folder('')
            for i in dirs.entries:
                item = QtGui.QTreeWidgetItem([i.name])
                item.path = i.path_lower
                item.file = i
                if isinstance(i, FolderMetadata):
                    item.is_folder = True
                else:
                    item.is_folder = False
                self.top_tree_items.append(item)
            self.root_item.addChildren(self.top_tree_items)
            self.fill_tree(dirs, self.top_tree_items)
        except Exception as e:
            print(e)
            self.labelError.setText('Loading error')
        self.progressBar.setRange(0, 1)
        self.labelTask.setText('Stand by.')

    def fill_tree(self, files_folders, top_items):
        '''Recursive method to load every folder and file
        in the treeWidget'''
        for i in range(len(files_folders.entries)):
            direc = files_folders.entries[i]
            if isinstance(direc, FolderMetadata):
                new_top_items = []
                subd = self.dbx.files_list_folder(direc.path_lower)
                item = top_items[i]
                for i in subd.entries:
                    n_item = QtGui.QTreeWidgetItem([i.name])
                    n_item.path = i.path_lower
                    n_item.file = i
                    if isinstance(i, FolderMetadata):
                        n_item.is_folder = True
                    else:
                        n_item.is_folder = False
                    new_top_items.append(n_item)
                item.addChildren(new_top_items)
                self.fill_tree(subd, new_top_items)

    def logout(self):
        '''Deletes the token from the PC so that te next
        time the users attempts to use the app, it asks for
        permission again'''
        string = 'Are you sure? This action will close the window '
        string += 'and the next time you use this application you '
        string += 'will be required to authenticate again. To just '
        string += 'exit, close the window.'
        ans = QtGui.QMessageBox.question(
            self,
            'Logout',
            string,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if ans == QtGui.QMessageBox.Yes:
            if 'db.token' in listdir():
                remove('db.token')
                QtGui.QApplication.quit()
