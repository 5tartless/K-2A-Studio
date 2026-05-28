from app.utils import CustomPyQt as qt, project_manager as pt, tab_manager as TabManager, file_manager as fm
from app.utils.code_manager import code_manager

class ProjectEditorMenu(qt.CMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

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

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top"), setObjectName="main", setMaximumHeight=48, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/top"))
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center"), setObjectName="main", setMinimumHeight=64, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center"))
        self.edit_widget(self.get_widget("/top", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.edit_widget(self.get_widget("/center", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        #classes:
            #editor (monaco)
        self.edit_widget(self.create_widget(Editor, "/editor", args={"name": "/editor", "object_name": "none"}), setSizePolicy=(qt.Qw.QSizePolicy.Minimum,qt.Qw.QSizePolicy.Minimum))
        self.get_widget("/editor").on_browser_load_callbacks.append(self.load_tab_bar)

        self.edit_widget(self.create_widget(qt.CMenuBar, "/top/menu-bar"))
        self.addToLayout(self.get_widget("/top", "layouts"), "/top/menu-bar")
        self.addToLayout(self.get_widget("/center", "layouts"), ("/editor",))
        self.addToLayout(self.get_widget("/", "layouts"), ("/top", "/center"))
        
        self.setAllStyleSheet(self.cssStyle)
    
    def load_tab_bar(self):
        self.edit_widget(self.create_widget(TabManager.TabBar, "/tab-manager", args={"reciever": self.get_widget("/editor"), "name": "/tab/tab-manager", "object_name": "main"}))
        self.addToLayout(self.get_widget("/top", "layouts"), ("/tab-manager",))
        self.config_menu_bar()

    def config_menu_bar(self):
        menu_bar: qt.CMenuBar = self.get_widget("/top/menu-bar")
        editor: Editor = self.get_widget("/editor")
        tab_bar: TabManager.TabBar = self.get_widget("/tab-manager")
        fm_action_list = menu_bar.fm_action_list()
        em_action_list = menu_bar.em_action_list()
        vm_action_list = menu_bar.vm_action_list()

        tab_manager = tab_bar.get_tab_manager()
        fm_action_list["new_file"].triggered.connect(tab_manager.add_tab)
        fm_action_list["open_file"].triggered.connect(tab_manager.add_tab_from_path)
        fm_action_list["save"].triggered.connect(lambda: tab_manager.save_tab(tab_manager.get_current_tab()))
        fm_action_list["save_as"].triggered.connect(lambda: tab_manager.save_tab(tab_manager.get_current_tab(), True))
        fm_action_list["exit"].triggered.connect(pt.get_parent_recursive(self, 2).close)


class Editor(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.current_code = qt.SetVar(None, self.store_code_memory)
        self._setting_code = False

        self.loaded = False
        self.on_browser_load_callbacks: list = []
        self.tab_manager: TabManager.TabManager

        self._save_timer = qt.QtCore.QTimer(self)
        self._save_timer.setInterval(150)
        self._save_timer.timeout.connect(self.get_code_sync)

        self.get_widget(self.lname, "layouts").setContentsMargins(0, 0, 0, 0)
        self.edit_widget(self.create_widget(qt.QtWebEngineWidgets.QWebEngineView, "/browser"),
            setHtml=(self.open_editor_html(), qt.QtCore.QUrl("http://localhost")),
        )
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

    def on_browser_load_finished(self):
        self.loaded = True
        for callback in self.on_browser_load_callbacks:
            callback()
        self._save_timer.start()

    def get_code_sync(self) -> None:
        if self.loaded and not self._setting_code:
            loop = qt.QtCore.QEventLoop()

            def callback(value):
                self.current_code.value = value
                loop.quit()

            self.get_widget("/browser").page().runJavaScript("window.editor.getValue();", callback)
            loop.exec_()

    def open_editor_html(self) -> str:
        return fm.read(fm.os.path.abspath("src/app/web/editor.html"))
    
    def set_code(self, code: str) -> None:
        self._setting_code = True
        escaped = fm.json.dumps(code)
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.setValue({escaped});",
            lambda _: setattr(self, "_setting_code", False)
        )

class FileExplorer():
    pass

class AIAssistant():
    pass
