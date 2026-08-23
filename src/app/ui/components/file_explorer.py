from app.utils.CustomPyQt import CSideBarFileExplorer, CContextMenu, QtCore, Qw
from app.utils import file_manager as fm, project_manager as pt

class FileExplorer(CSideBarFileExplorer):
    file_opened = QtCore.pyqtSignal(str)
    class ContextMenu(CContextMenu):
        def __init__(self, title="Inspect", parent=None):
            super().__init__(title, parent)
            

    def __init__(self, parent=None, project_path: str = ""):
        super().__init__(parent, project_path)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu_requested)
        for i in range(3):
            self.hideColumn(i+1)
        self.setHeaderHidden(True)
        # self.doubleClicked.connect(self.on_file_opened)

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            if event.button() == QtCore.Qt.LeftButton:
                self.on_file_opened(index)
        super().mouseDoubleClickEvent(event)

    def on_file_opened(self, index):
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            return
        self.file_opened.emit(path)

    def on_context_menu_requested(self, position) -> None:
        index = self.indexAt(position)
        path = self.file_model.filePath(index) if index.isValid() else self.project_path
        context_menu = self.ContextMenu(parent=self)
        if not index.isValid() or self.file_model.isDir(index):
            context_menu.add_action("new_file", "New file")
            context_menu.connect_action("new_file", lambda: self.new_file(path))
            context_menu.add_action("new_folder", "New folder")
            context_menu.connect_action("new_folder", lambda: self.new_folder(path))
            if index.isValid(): context_menu.addSeparator()
        if index.isValid():
            context_menu.addSeparator()
            context_menu.add_action("rename", "Rename")
            context_menu.connect_action("rename", lambda: self.rename(index))
            context_menu.add_action("delete", "Delete")
            context_menu.connect_action("delete", lambda: self.delete(index))
            context_menu.addSeparator()
            context_menu.add_action("copy-rpath", "Copy relative path")
            context_menu.connect_action("copy-rpath", lambda: self.copy_path(index, True))
            context_menu.add_action("copy-path", "Copy path")
            context_menu.connect_action("copy-path", lambda: self.copy_path(index))
        context_menu.exec_(self.viewport().mapToGlobal(position))
    
    def get_tab_manager(self):
        return pt.get_parent_recursive(self, 3).get_widget("/tab-bar").get_tab_manager()

    def new_file(self, path):
        name, ok = Qw.QInputDialog.getText(self, "New file", "File name:")
        if ok and name:
            new_file_path = fm.os.path.join(path, name)
            if not fm.path_exists(new_file_path):
                fm.write(new_file_path, "")
            else:
                print(f"INFO: File with name: {name}. Already exists")
    def new_folder(self, path):
        name, ok = Qw.QInputDialog.getText(self, "New folder", "Folder name:")
        if ok and name:
            try:
                fm.os.makedirs(fm.os.path.join(path, name))
            except OSError:
                print(f"INFO: Folder with name: {name}. Already exists.")

    def rename(self, index):
        old_path = self.file_model.filePath(index)
        old_name = fm.get_file_name(old_path)
        is_dir = self.file_model.isDir(index)
        name, ok = Qw.QInputDialog.getText(self, "Rename", "New name:", text=old_name)
        if ok and name:
            new_path = fm.os.path.join(fm.os.path.dirname(old_path), name)
            if is_dir:
                tabs: list = self.get_tab_manager().list_tabs()
                for tab in tabs:
                    if old_path in tab.path:
                        old_path_chunks: list = old_path.split("/")
                        tab_path_chunks: list = tab.path.split("/")
                        tab_path_chunks[len(old_path_chunks) - 1] = name
                        tab.path = "/".join(tab_path_chunks)
            else:
                tab = self.get_tab_manager().find_tab(title=old_name)
                if tab:
                    tab.rename(name)
            fm.os.rename(old_path, new_path)

    def delete(self, index):
        path = self.file_model.filePath(index)
        is_dir = self.file_model.isDir(index)
        delete_message = f"Would you like to delete this {'folder and its contents' if is_dir else 'file'}?"
        reply = Qw.QMessageBox.question(self, "Delete", delete_message, Qw.QMessageBox.Yes | Qw.QMessageBox.No)
        if reply == Qw.QMessageBox.Yes:
            if is_dir:
                tabs: list = self.get_tab_manager().list_tabs()
                for tab in tabs:
                    if path in tab.path:
                        tab.kill(force=True)
                fm.shutil.rmtree(path)
            else:
                name = fm.get_file_name(path)
                tab = self.get_tab_manager().find_tab(title=name)
                if tab: 
                    tab.kill(force=True)
                fm.os.remove(path)

    def copy_path(self, index, rpath: bool = False):
        path: str = self.file_model.filePath(index)
        if rpath:
            project_path_chunks = self.project_path.split("/")
            path_chunks = path.split("/")[1:]
            path = "/".join(path_chunks[(len(project_path_chunks)-1): ])
        Qw.QApplication.clipboard().setText(path)