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

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top"), setObjectName="main", setMaximumHeight=32, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/top"))
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center"), setObjectName="main", setMinimumHeight=64, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center"))
        self.edit_widget(self.get_widget("/top", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.edit_widget(self.get_widget("/center", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        #classes:
            #editor (monaco)
        self.edit_widget(self.create_widget(Editor, "/editor", args={"name": "/editor", "object_name": "none"}))
        self.get_widget("/editor").on_browser_load_callbacks.append(self.load_tab_bar)

        self.addToLayout(self.get_widget("/center", "layouts"), ("/editor",))
        self.addToLayout(self.get_widget("/", "layouts"), ("/top", "/center"))
        
        self.setAllStyleSheet(self.cssStyle)
    def load_tab_bar(self):
        self.edit_widget(self.create_widget(TabManager.TabBar, "/tab-manager", args={"reciever": self.get_widget("/editor"), "name": "/tab/tab-manager", "object_name": "main"}))
        self.addToLayout(self.get_widget("/top", "layouts"), ("/tab-manager",))

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

    # def await_monaco(self): #USELESS for now i don't know if it will ever be useful i just like that code.
    #     def set_result(ready: bool):
    #         if ready:
    #             for callback in self.await_monaco_callbacks:
    #                 callback()
    #         else: qt.QtCore.QTimer.singleShot(50, check_monaco_ready)
    #     def check_monaco_ready():
    #         self.get_widget("/browser").page().runJavaScript(
    #             "typeof window.editor !== 'undefined'",
    #             set_result
    #         )
    #     check_monaco_ready()

    def store_code_memory(self, code: str):
        if self.tab_manager.current_tid >= 0:
            code_manager.update_code(self.tab_manager.get_tab_name(self.tab_manager.current_tid), code)

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
        escaped = pt.json.dumps(code)
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.setValue({escaped});",
            lambda _: setattr(self, "_setting_code", False)
        )

class FileExplorer():
    pass

class AIAssistant():
    pass

class HiddenConfBar():
    pass
