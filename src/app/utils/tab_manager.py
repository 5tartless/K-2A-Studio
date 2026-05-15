from app.utils import CustomPyQt as qt, file_manager as fm

class TabBar(qt.CFrame):
    def __init__(self, *args, reciever=None, **kwargs):
        super().__init__(*args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.edit_widget(self.get_widget(self.lname, "layouts"), setAlignment=(qt.QtCore.Qt.AlignLeft), setContentsMargins=(0, 0, 0, 0), setSpacing=10)
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/add-tab"), setText="+", setObjectName="main", setMinimumWidth=32)
        self.create_widget(TabManager, "/manager", args={
            "reciever": reciever, "name": "/manager", "object_name": "main"
        })
        self.edit_widget(self.create_widget(qt.Qw.QScrollArea, "/tab"), setWidgetResizable=True, setWidget=self.get_widget("/manager"))

        self.addToLayout(("/tab", "/add-tab"))

class TabManager(qt.CFrame):
    def __init__(self, parent, *args, reciever: object, **kwargs):
        super().__init__(*args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.tabs: dict = {}
        self.tab_history: list = []

        self.max_tid = -1
        self.current_tid = -1

        self.edit_widget(self.get_widget(self.lname, "layouts"), setAlignment=(qt.QtCore.Qt.AlignLeft), setContentsMargins=(0, 0, 0, 0), setSpacing=10)
        self.connect_signal((parent.get_widget("/add-tab"),), {"clicked": self.add_tab})

        self.add_tab()

    def add_to_tab_history(self, tid: int):
        if tid in self.tab_history:
            self.remove_from_tab_history(tid)
        self.tab_history.append(tid)

    def remove_from_tab_history(self, tid: int):
        if tid in self.tab_history:
            self.tab_history.pop(self.tab_history.index(tid))

    def set_active(self, tid: int): #to be made
        current_tab = self.get_widget(f"/tab/{self.current_tid}", "tabs")
        if current_tab: 
            self.edit_widget(current_tab, setObjectName="tab-active", reloadStyleSheet=None)
        if tid >= 0:
            self.edit_widget(self.get_widget(f"/tab/{tid}", "tabs"), setObjectName="main", reloadStyleSheet=None)
        self.current_tid = tid
        self.add_to_tab_history(tid)

    def add_tab(self, title: str = None, path: str = None):
        self.max_tid += 1

        tab_name = f"/tab/{self.max_tid}"
        self.create_widget(Tab, tab_name, "tabs", args={
            "tid": self.max_tid,
            "title": title or f"Untitled-{self.max_tid}",
            "path": path,
            "name": tab_name,
            "object_name": "main-top"
        })
        self.connect_signal((self.get_widget(tab_name, "tabs"),), ({"request_kill": self.request_kill_tab}, {"clicked": self.set_active}))

        self.addToLayout(tab_name, from_where="tabs")
        self.set_active(self.max_tid)

    def request_kill_tab(self, tid: Tab):
        self.deleteWidgets(f"/tab/{tid}", "tabs")
        self.remove_from_tab_history(tid)
        self.set_active(self.tab_history[-1:][0])

class Tab(qt.CFrame):
    request_kill = qt.QtCore.pyqtSignal(object)
    clicked = qt.QtCore.pyqtSignal(object)

    def __init__(self, *args, tid: int, title: str, path: str, **kwargs):
        super().__init__(*args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.setFixedWidth(80)
        self.tid = tid
        
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setText=title, setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/kill-tab"), setText="X", setObjectName="main")
        self.connect_signal((self.get_widget("/kill-tab"), ), {"clicked": self.kill})

        self.setPath(path)
        
        self.edit_widget(self.get_widget(self.lname, "layouts"), setContentsMargins=(0, 0, 0, 0), setSpacing=0)
        self.addToLayout((("/title", 4), "-s2", ("/kill-tab", 4)))
    
    def setPath(self, path: str):
        pass

    def kill(self):
        self.request_kill.emit(self.tid)

    def mousePressEvent(self, event):
        if event.button() == qt.QtCore.Qt.LeftButton:
            self.clicked.emit(self.tid)
    