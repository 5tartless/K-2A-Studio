from app.utils import CustomPyQt as qt
from app.ui.menus._basic_menu import K2A_Menu
from app.ui.cards.pscardrepo import PSCardRepo
from app.ui.cards.pscardlocal import PSCardLocal

class ImportProjectMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # self.setAllStyleSheet(self.cssStyle)
        self.init_fill_request()

    def appear(self, **kwargs):
        return super().appear(**kwargs)

    def init_fill_request(self):
        self.get_widget("/center", "layouts").setSpacing(0)

        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/title"), setObjectName="main", setText="Import a project", setAlignment=qt.QtCore.Qt.AlignCenter)
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/title/subtitle"), setObjectName="main", setText="With this next step empower your project with AI assistance",
                        setAlignment=qt.QtCore.Qt.AlignCenter)
        
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center/options"), setObjectName="main-top", setFixedHeight=500, setLayout=self.create_layout(qt.Qw.QHBoxLayout, "/center/options"))
        self.edit_widget(self.create_widget(PSCardRepo, "/center/options/repo", args={"layout":qt.Qw.QVBoxLayout, "name":"/center/options/repo", "object_name":"main-top"}),
                        setMaximumWidth=500, setMinimumWidth=300, setSizePolicy=(qt.Qw.QSizePolicy.Preferred, qt.Qw.QSizePolicy.Minimum))
        self.edit_widget(self.create_widget(PSCardLocal, "/center/options/local", args={"layout":qt.Qw.QVBoxLayout, "name":"/center/options/local", "object_name":"main-top"}),
                        setMaximumWidth=500, setMinimumWidth=300, setSizePolicy=(qt.Qw.QSizePolicy.Preferred, qt.Qw.QSizePolicy.Minimum))
        #for more code about PSCardRepo and PSCardLocal go to its classes they are CFrames

        self.get_widget("/center/options", "layouts").setSpacing(32)
        self.addToLayout(self.get_widget("/center/options", "layouts"), ("-s1", ("/center/options/repo", 2), ("/center/options/local", 2), "-s1"))
        self.addToLayout(self.get_widget("/center", "layouts"), (("/center/title"), ("/center/title/subtitle"), ("/center/options"), "-s20"))