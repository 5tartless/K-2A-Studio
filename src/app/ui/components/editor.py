from app.utils.code_manager import code_manager
from app.utils import CustomPyQt as qt, file_manager as fm

class Editor(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.current_code = qt.SetVar(None, self.store_code_memory)
        self._setting_code = False

        self.loaded = False
        self.on_browser_load_callbacks: list = []
        self.tab_manager = None

        self._code_update_timer = qt.create_timer(parent=self, time_out_callback=self.get_code_sync, interval=150)

        self.get_widget(self.lname, "layouts").setContentsMargins(0, 0, 0, 0)
        self.edit_widget(
            self.create_widget(
                qt.QtWebEngineWidgets.QWebEngineView,
                "/browser"
            ),
            setHtml=(
                self.open_editor_html(),
                qt.QtCore.QUrl("http://localhost")
            )
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