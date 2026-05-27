from app.utils import CustomPyQt as qt, file_manager as fm, project_manager as pt
from app.utils.code_manager import code_manager

class TabBar(qt.CFrame):
    def __init__(self, parent, *args, reciever=None, **kwargs):
        super().__init__(parent, *args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.edit_widget(self.get_widget(self.lname, "layouts"), setAlignment=(qt.QtCore.Qt.AlignLeft), setContentsMargins=(0, 0, 0, 0), setSpacing=10)
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/add-tab"), setText="+", setObjectName="main", setMinimumWidth=32)
        self.create_widget(TabManager, "/manager", args={
            "reciever": reciever, "name": "/manager", "object_name": "main"
        })
        self.edit_widget(self.create_widget(qt.Qw.QScrollArea, "/tab"), setWidgetResizable=True, setWidget=self.get_widget("/manager"))

        self.addToLayout(("/tab", "/add-tab"))

class TabManager(qt.CFrame):
    def __init__(self, parent, *args, reciever: object, **kwargs):
        super().__init__(parent, *args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.tabs: dict = {}
        self.tab_history: list = []
        self.receiver = reciever
        self.receiver.tab_manager = self

        self.max_tid = -1
        self.current_tid = -1

        self.edit_widget(self.get_widget(self.lname, "layouts"), setAlignment=(qt.QtCore.Qt.AlignLeft), setContentsMargins=(0, 0, 0, 0), setSpacing=10)
        self.connect_signal((self.parent().get_widget("/add-tab"),), {"clicked": self.add_tab})

        self.add_tab("test", "src/samples/sample1.py")

    def add_to_tab_history(self, tid: int):
        if tid in self.tab_history:
            self.remove_from_tab_history(tid)
        self.tab_history.append(tid)

    def remove_from_tab_history(self, tid: int):
        if tid in self.tab_history:
            self.tab_history.pop(self.tab_history.index(tid))

    def get_tab(self, tid: int) -> Tab:
        return self.get_widget(self.get_tab_name(tid), "tabs")

    def get_tab_name(self, tid: int) -> str:
        return f"/tab/{tid}"

    def set_active(self, tid: int):
        if self.current_tid != tid:

            current_tab = self.get_tab(self.current_tid)
            if current_tab: #old
                self.edit_widget(current_tab, setObjectName="tab-active", reloadStyleSheet=None)
                code_manager.update_code(self.get_tab_name(self.current_tid), self.receiver.current_code.value)
            if tid >= 0:    #new
                self.edit_widget(self.get_tab(tid), setObjectName="main", callText=None, reloadStyleSheet=None)
            
            self.current_tid = tid
            self.add_to_tab_history(tid)

    def add_tab(self, title: str = None, path: str = None):
        self.max_tid += 1

        tab_name = self.get_tab_name(self.max_tid)
        self.create_widget(Tab, tab_name, "tabs", args={
            "tid": self.max_tid,
            "title": title or f"Untitled-{self.max_tid}",
            "path": path,
            "receiver": self.receiver,
            "name": tab_name,
            "object_name": "main-top"
        })
        self.connect_signal((self.get_widget(tab_name, "tabs"),), ({"request_kill": self.request_kill_tab, "clicked": self.set_active}))

        self.addToLayout(tab_name, from_where="tabs")
        self.set_active(self.max_tid)

    def request_kill_tab(self, tid: Tab):
        code_manager.delete_code(self.get_tab_name(tid))
        self.deleteWidgets(self.get_tab_name(tid), "tabs")
        self.remove_from_tab_history(tid)
        if self.tab_history:
            self.set_active(self.tab_history[-1:][0])
        else:
            self.current_tid = -1
            self.receiver.set_code("")

class Tab(qt.CFrame):
    request_kill = qt.QtCore.pyqtSignal(object)
    clicked = qt.QtCore.pyqtSignal(object)

    def __init__(self, *args, tid: int, title: str, path: str, **kwargs):
        super().__init__(*args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.tid = tid
        self.path = path
        self.title = title
        self.receiver = kwargs["receiver"]
        self.name = kwargs["name"]

        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setText=self.title, setMinimumWidth=60, setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/kill-tab"), setText="X", setFixedSize=(16,16), setObjectName="main")
        self.connect_signal((self.get_widget("/kill-tab"), ), {"clicked": self.kill})

        self.edit_widget(self.get_widget(self.lname, "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.addToLayout((("/title", 4), ("/kill-tab", 3)))
        self.setFixedWidth(80)
    
    def callText(self):
        code_exists = code_manager.code_exists(self.name)
        # print(code_exists)
        
        # if code_exists:
        #     self.receiver.set_code(code_manager.get_code(self.name))
        #     return
        # else:
        #     if fm.path.exist(self.path):
        #         content = fm.read(self.path)
        #         code_manager.update_code(self.name, content)
        #         self.receiver.set_code(content)
        #         return
        # self.receiver.set_code("")

        if fm.path_exist(self.path):
            if not code_exists:
                content = fm.read(self.path)
                code_manager.update_code(self.name, content)
                self.receiver.set_code(content)
                return
        
        if code_exists:
            self.receiver.set_code(
                code_manager.get_code(self.name)
            )
            return
        self.receiver.set_code("")

    def kill(self):
        self.request_kill.emit(self.tid)

    def mousePressEvent(self, event):
        if event.button() == qt.QtCore.Qt.LeftButton:
            self.clicked.emit(self.tid)