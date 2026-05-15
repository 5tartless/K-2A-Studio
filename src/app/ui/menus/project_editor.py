from app.utils import CustomPyQt as qt, project_manager as pt, tab_manager as TabManager

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
        self.edit_widget(self.create_widget(TabManager.TabBar, "/tab-manager", args={"reciever": self.get_widget("/editor").current_code, "name": "/tab/tab-manager", "object_name": "main"}))

        self.addToLayout(self.get_widget("/top", "layouts"), ("/tab-manager",))
        self.addToLayout(self.get_widget("/center", "layouts"), ("/editor",))
        self.addToLayout(self.get_widget("/", "layouts"), ("/top", "/center"))
        self.setAllStyleSheet(self.cssStyle)


class Editor(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.current_code = qt.SetVar(None, lambda value: value) #do none
        self.loaded = False

        self.get_widget(self.lname, "layouts").setContentsMargins(0, 0, 0, 0)

        self.create_widget(qt.CBridge, "/browser/bridge")
        self.edit_widget(self.create_widget(qt.QtWebChannel.QWebChannel, "/browser/channel"), registerObject=("pybridge", self.get_widget("/browser/bridge")))

        self.edit_widget(self.create_widget(qt.QtWebEngineWidgets.QWebEngineView, "/browser"),
                         setHtml=(self.open_editor_html(), qt.QtCore.QUrl("http://localhost")),
                         setWebChannel=self.get_widget("/browser/channel"))
        self.connect_signal((self.get_widget("/browser"),), {"loadFinished": self.on_browser_load_finished, "titleChanged": self.get_code_sync})
        self.addToLayout("/browser")

    def on_browser_load_finished(self):
        self.loaded = True
        self.get_code_sync()

    def get_code_sync(self) -> None:
        if self.loaded:
            result = None
            loop = qt.QtCore.QEventLoop()

            def callback(value):
                nonlocal result
                result = value
                loop.quit()

            self.get_widget("/browser").page().runJavaScript("window.editor.getValue();", callback)
            loop.exec_()
            self.current_code.value = result

    def open_editor_html(self) -> str:
        with open(pt.os.path.abspath("src/app/web/editor.html"), "r") as file:
            return file.read()
    
    def set_code(self, code: str) -> None:
        self.get_widget("/browser").page().runJavaScript(
            f"window.editor.setValue({pt.json.dumps(code)});"
        )
    
class FileExplorer():
    pass

class AIAssistant():
    pass

class HiddenConfBar():
    pass
