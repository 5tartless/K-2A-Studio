from app.utils import CustomPyQt as qt, project_manager as pt, tab_manager as TabManager, file_manager as fm
from app.utils.code_manager import code_manager
from app.ui.components.file_explorer import FileExplorer

class ProjectEditorMenu(qt.CMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        code_manager._auto_save_timer.timeout.connect(self.save_tab)

    def appear(self, **kwargs):
        self.load(kwargs)

    def hideEvent(self, a0): #this feature should be moved alongside load to make the app less ram consuming.
        for widget in self.widgets.copy():
            del self.widgets[widget]
        for layout in self.layouts.copy():
            del self.layouts[layout]

        return super().hideEvent(a0)

    def load(self, project_data):
        # print("Data recieved: ", project_data)
        self.setLayout(self.create_layout(qt.Qw.QVBoxLayout, "/"))
        self.edit_widget(self.get_widget("/", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top"), setObjectName="main", setMaximumHeight=48,
                        setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/top"), setSizePolicy=(qt.Qw.QSizePolicy.Expanding, qt.Qw.QSizePolicy.Fixed))
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center"), setObjectName="main", setMinimumHeight=256, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center"))
        self.edit_widget(self.get_widget("/top", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.edit_widget(self.get_widget("/center", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        #classes:
            #editor (monaco)
        self.edit_widget(self.create_widget(qt.CSplitter, "/center/workspace"), setSizes=([200,600],), setSizePolicy=(qt.Qw.QSizePolicy.Expanding, qt.Qw.QSizePolicy.Expanding))
        self.edit_widget(self.create_widget(Editor, "/center/workspace/editor", args={"name": "/center/workspace/editor", "object_name": "none"}), setMinimumWidth=512)
        self.get_widget("/center/workspace/editor").on_browser_load_callbacks.append(self.load_tab_bar)
        self.get_widget("/center/workspace").addWidget(self.get_widget("/center/workspace/editor"))
        self.edit_widget(self.create_widget(FileExplorer, "/center/workspace/file-explorer", args={"project_path": qt.QtCore.QDir.currentPath()}),
                         setMinimumWidth=192)
        self.get_widget("/center/workspace").addWidget(self.get_widget("/center/workspace/file-explorer"))

        
        self.get_widget("/center/workspace").setCollapsible(0, False)
        self.edit_widget(self.create_widget(qt.CMenuBar, "/top/menu-bar"))
        self.addToLayout(self.get_widget("/top", "layouts"), "/top/menu-bar")
        self.addToLayout(self.get_widget("/center", "layouts"), "/center/workspace")
        self.addToLayout(self.get_widget("/", "layouts"), ("/top", "/center"))
        
        self.setAllStyleSheet(self.cssStyle)
    
    def load_tab_bar(self):
        self.edit_widget(self.create_widget(TabManager.TabBar, "/tab-bar", args={"reciever": self.get_widget("/center/workspace/editor"), "name": "/tab/tab-bar", "object_name": "main"}),
                        setMaximumHeight=28)
        self.addToLayout(self.get_widget("/top", "layouts"), ("/tab-bar",))
        self.connect_to_signal(self.get_widget("/center/workspace/file-explorer"), file_opened=self.get_widget("/tab-bar").get_tab_manager().add_tab_from_path)
        self.config_menu_bar()

    def save_tab(self, save_as: bool = False) -> None:
        tab_manager: TabManager.TabManager = self.get_widget("/tab-bar").get_tab_manager()
        tab_manager.save_tab(tab_manager.get_current_tab(), save_as)

    def config_menu_bar(self):
        menu_bar: qt.CMenuBar = self.get_widget("/top/menu-bar")
        tab_bar: TabManager.TabBar = self.get_widget("/tab-bar")
        editor: Editor = self.get_widget("/center/workspace/editor")

        tab_manager = tab_bar.get_tab_manager()

        menu_bar.menus["file"].add_defaults()
        menu_bar.set_menu_action_callback("file", "new_file", tab_manager.add_tab)
        menu_bar.set_menu_action_keybind("file", "new_file", "Ctrl+N")
        menu_bar.set_menu_action_callback("file", "open_file", tab_manager.add_tab_from_path)
        menu_bar.set_menu_action_keybind("file", "open_file", "Ctrl+O")
        menu_bar.set_menu_action_callback("file", "save", self.save_tab)
        menu_bar.set_menu_action_keybind("file", "save", "Ctrl+S")
        menu_bar.set_menu_action_callback("file", "save_as", lambda: self.save_tab(True))
        menu_bar.set_menu_action_keybind("file", "save_as", "Ctrl+Shift+S")
        menu_bar.set_menu_action_callback("file", "exit", pt.get_parent_recursive(self, 2).close)
        menu_bar.set_menu_action_keybind("file", "exit", "Ctrl+Q")

        menu_bar.menus["edit"].add_action("preferences", "Preferences")
        menu_bar.menus["edit"].add_action("auto_save", "Enable Auto Save")
        menu_bar.set_menu_action_callback("edit", "auto_save", code_manager.toggle_auto_save)
        menu_bar.menus["edit"].add_defaults()
        menu_bar.set_menu_action_callback("edit", "undo", self.get_widget("/center/workspace/editor").history_do)
        menu_bar.set_menu_action_callback("edit", "redo", lambda: self.get_widget("/center/workspace/editor").history_do(True))
        menu_bar.set_menu_action_callback("edit", "cut", lambda: self.get_widget("/center/workspace/editor").clipboard_do("cut"))
        menu_bar.set_menu_action_callback("edit", "copy", lambda: self.get_widget("/center/workspace/editor").clipboard_do("copy"))
        menu_bar.set_menu_action_callback("edit", "paste", lambda: self.get_widget("/center/workspace/editor").clipboard_do("paste"))

        menu_bar.add_menu("view", qt.CContextMenu, title="View")
        menu_bar.menus["view"].add_action("editor_appearance", "Editor Appearance")
        menu_bar.menus["view"].add_action("chat", "Show Chat")
        menu_bar.menus["view"].add_action("menu_bar", "Show Menu Bar")
        menu_bar.menus["view"].addSeparator()
        menu_bar.menus["view"].add_action("file_explorer", "Show File Explorer")
        menu_bar.menus["view"].add_action("swap_chat_and_file_explorer", "Swap With Chat")
        menu_bar.menus["view"].addSeparator()
        menu_bar.menus["view"].add_action("tab_bar", "Show Tab Bar")
        menu_bar.set_menu_action_callback("view", "file_explorer", lambda: self.get_widget("/center/workspace").toggle_collapse_widget(self.get_widget("/center/workspace/file-explorer")))
        menu_bar.set_menu_action_keybind("view", "file_explorer", "Ctrl+B")
        menu_bar.set_menu_action_callback("view", "menu_bar", lambda: self.toggleWidgetVisible(self.get_widget("/top/menu-bar")))
        menu_bar.set_menu_action_keybind("view", "menu_bar", "Ctrl+Shift+M")
        menu_bar.set_menu_action_callback("view", "tab_bar", lambda: self.toggleWidgetVisible(self.get_widget("/tab-bar")))
        menu_bar.set_menu_action_keybind("view", "tab_bar", "Ctrl+Shift+T")

class Editor(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.current_code = qt.SetVar(None, self.store_code_memory)
        self._setting_code = False

        self.loaded = False
        self.on_browser_load_callbacks: list = []
        self.tab_manager: TabManager.TabManager

        self._code_update_timer = qt.create_timer(parent=self, time_out_callback=self.get_code_sync, interval=150)

        self.get_widget(self.lname, "layouts").setContentsMargins(0, 0, 0, 0)
        self.edit_widget(self.create_widget(qt.QtWebEngineWidgets.QWebEngineView, "/browser"),
            setHtml=(self.open_editor_html(), qt.QtCore.QUrl("http://localhost")),
        )
        for setting in [qt.QtWebEngineWidgets.QWebEngineSettings.JavascriptCanAccessClipboard, qt.QtWebEngineWidgets.QWebEngineSettings.JavascriptCanPaste]:
            self.get_widget("/browser").settings().setAttribute(setting, True)
        self.connect_signal((self.get_widget("/browser"),), {"loadFinished": self.on_browser_load_finished})
        self.addToLayout("/browser")

    def store_code_memory(self, code: str):
        if self.tab_manager.current_tid >= 0:
            current_tab = self.tab_manager.get_tab(self.tab_manager.current_tid)
            if code_manager.code_exists(current_tab.name): 
                if fm.path_exists(current_tab.path) and self.current_code.value == fm.read(current_tab.path):
                    current_tab.saved = True
                elif code_manager.get_code(current_tab.name) != code:
                    current_tab.saved = False
            code_manager.update_code(current_tab.name, code)

    def history_do(self, redo: bool = False):
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.trigger('keyboard', '{'undo' if not redo else 'redo'}', null);"
        )
    def clipboard_do(self, action: str): #action = 'cut', 'copy', 'paste'
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.trigger('keyboard', 'editor.action.clipboard{action.capitalize()}Action', null);"
        )

    def open_editor_html(self) -> str:
        return fm.read(fm.os.path.abspath("src/app/web/editor.html"))
    
    def on_browser_load_finished(self):
        self.loaded = True
        for callback in self.on_browser_load_callbacks:
            callback()
        self._code_update_timer.start()

    def get_code_sync(self) -> None:
        if self.loaded and not self._setting_code:
            loop = qt.QtCore.QEventLoop()

            def callback(value):
                self.current_code.value = value
                loop.quit()

            self.get_widget("/browser").page().runJavaScript("window.editor.getValue();", callback)
            loop.exec_()

    def set_code(self, code: str) -> None:
        self._setting_code = True
        escaped = fm.json.dumps(code)
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.setValue({escaped});",
            lambda _: setattr(self, "_setting_code", False)
        )

class AIAssistant():
    pass
