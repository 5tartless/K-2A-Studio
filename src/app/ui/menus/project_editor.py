from app.ui.components import tab_manager as TabManager
from app.utils import CustomPyQt as qt, project_manager as pt, file_manager as fm
from app.utils.code_manager import code_manager
from app.utils import code_runner
from app.ui.components.file_explorer import FileExplorer
from app.ui.components.editor import Editor
from app.ui.components.chat_view import ChatView

class ProjectEditorMenu(qt.CMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        code_manager._auto_save_timer.timeout.connect(self.save_tab)

    def appear(self, **kwargs):
        self.load(**kwargs)

    def hideEvent(self, a0): #this feature should be moved alongside load to make the app less ram consuming.
        for widget in self.widgets.copy():
            del self.widgets[widget]
        for layout in self.layouts.copy():
            del self.layouts[layout]

        return super().hideEvent(a0)
    
    def load(self, **kwargs):
        project_data: dict = kwargs.get("project_data", {})
        print("Data recieved: ", project_data)

        self.setLayout(self.create_layout(qt.Qw.QVBoxLayout, "/"))
        self.edit_widget(self.get_widget("/", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top"), setObjectName="main", setMaximumHeight=48,
                        setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/top"), setSizePolicy=(qt.Qw.QSizePolicy.Expanding, qt.Qw.QSizePolicy.Fixed))
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center"), setObjectName="main", setMinimumHeight=256, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center"))
        self.edit_widget(self.get_widget("/top", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.edit_widget(self.get_widget("/center", "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.edit_widget(self.create_widget(qt.CSplitter, "/center/workspace"), setSizePolicy=(qt.Qw.QSizePolicy.Expanding, qt.Qw.QSizePolicy.Expanding))
        self.edit_widget(
            self.create_widget(
                ChatView,
                "/center/workspace/chat-view",
                args={"name": "/center/workspace/chat-view", "object_name": "main"}
            ),
            setMinimumWidth=256,
            setSizePolicy=(qt.Qw.QSizePolicy.Expanding, qt.Qw.QSizePolicy.Expanding)
        )
        self.edit_widget(self.create_widget(Editor, "/center/workspace/editor", args={"name": "/center/workspace/editor", "object_name": "none"}), setMinimumWidth=512)
        self.get_widget("/center/workspace/editor").on_browser_load_callbacks.append(self.load_tab_bar)
        self.edit_widget(
            self.create_widget(
                FileExplorer,
                "/center/workspace/file-explorer",
                args={
                    "project_path": project_data["path"] #qt.QtCore.QDir.currentPath()
                }
            ),
            setMinimumWidth=192
        )
        
        self.get_widget("/center/workspace").addWidget(self.get_widget("/center/workspace/chat-view"))
        self.get_widget("/center/workspace").addWidget(self.get_widget("/center/workspace/editor"))
        self.get_widget("/center/workspace").addWidget(self.get_widget("/center/workspace/file-explorer"))
        self.get_widget("/center/workspace").setCollapsible(1, False)
 
        self.addToLayout(self.get_widget("/center", "layouts"), "/center/workspace")
        self.addToLayout(self.get_widget("/", "layouts"), ("/top", "/center"))
        self.setAllStyleSheet(self.cssStyle)
    
    def load_tab_bar(self):
        self.edit_widget(self.create_widget(TabManager.TabBar, "/tab-bar", args={"reciever": self.get_widget("/center/workspace/editor"), "name": "/tab/tab-bar", "object_name": "main"}),
                        setMaximumHeight=28)
        self.connect_to_signal(self.get_widget("/center/workspace/file-explorer"), file_opened=self.get_widget("/tab-bar").get_tab_manager().add_tab_from_path)
        
        from app.ui.components.editor_menu_bar import EditorMenuBar
        self.create_widget(
            EditorMenuBar,
            "/top/menu-bar",
            args={
                "menu": self,
                "tab_manager": self.get_widget("/tab-bar").get_tab_manager()
            }
        )
        self.addToLayout(self.get_widget("/top", "layouts"), ("/top/menu-bar", "/tab-bar"))

    def save_tab(self, save_as: bool = False) -> None:
        tab_manager: TabManager.TabManager = self.get_widget("/tab-bar").get_tab_manager()
        tab_manager.save_tab(tab_manager.get_current_tab(), save_as)

    def run_code(self) -> None:
        editor = self.get_widget("/center/workspace/editor")
        chat_view = self.get_widget("/center/workspace/chat-view")
        if not editor or not chat_view:
            return

        code = editor.current_code.value or ""
        if not code.strip():
            return

        extension = ".py"
        if editor.tab_manager and editor.tab_manager.current_tid >= 0:
            tab = editor.tab_manager.get_tab(editor.tab_manager.current_tid)
            if tab and tab.path:
                _, ext = fm.os.path.splitext(tab.path)
                if ext:
                    extension = ext

        chat_container = chat_view.get_widget("/chat-container")
        chat_container.add_message("▶️ Ejecutando código...", from_="system")

        if not hasattr(self, "_run_workers"):
            self._run_workers = []

        worker = qt.Worker(lambda: code_runner.run_code(code, extension))
        worker.workerFinished.connect(lambda result: self._on_run_finished(result, chat_container, worker))
        self._run_workers.append(worker)
        worker.start()

    def _on_run_finished(self, result: dict, chat_container, worker) -> None:
        if result.get("exit_code") == 0 and not result.get("stderr"):
            output = result.get("stdout") or "(el código se ejecutó sin salida)"
            message = f"✅ Resultado:\n{output}"
        else:
            output = result.get("stderr") or result.get("stdout") or "Ocurrió un error desconocido."
            message = f"❌ Error:\n{output}"

        chat_container.add_message(message, from_="system")

        if worker in getattr(self, "_run_workers", []):
            self._run_workers.remove(worker)
