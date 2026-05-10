from app.utils import CustomPyQt as qt
from app.ui.menus._basic_menu import K2A_Menu

class HomeMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._center_titles_setup()
        # self.setAllStyleSheet(self.cssStyle)
    
    def import_menu(self): 
        main_window = self.getMainWindow()
        main_window.menu_fader.play(duration=100, startValue=1, middleValue=0, endValue=1, middleFunction=lambda: main_window.showMenu(1))
    def create_menu(self): 
        main_window = self.getMainWindow()
        main_window.menu_fader.play(duration=100, startValue=1, middleValue=0, endValue=1, middleFunction=lambda: main_window.showMenu(2))

    def appear(self, **kwargs):
        if kwargs.get("animate", True):
            self.getMainWindow().menu_fader.play(
                duration=kwargs.get("duration", 750),
                startValue=kwargs.get("startValue", 0),
                middleValue=kwargs.get("middleValue", 1),
                endValue=kwargs.get("endValue", 1),
                skipEndValue=kwargs.get("skipEndValue", True),
                middleFunction=kwargs.get("middleFunction"),
                easingCurve=qt.QtCore.QEasingCurve.InOutCubic)

    def _center_titles_setup(self):
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/title"), setObjectName="main",
                        setText="Welcome To K2A PlaceHolder", setAlignment=qt.QtCore.Qt.AlignCenter, setSizePolicy=(qt.Qw.QSizePolicy.Preferred, qt.Qw.QSizePolicy.Maximum))
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/title/subtitle"), setObjectName="main",
                        setText="An application ready for you to manage your projects as you please!", setAlignment=qt.QtCore.Qt.AlignCenter,
                        setSizePolicy=(qt.Qw.QSizePolicy.Preferred, qt.Qw.QSizePolicy.Maximum))
        
        self._center_project_import_setup()
        self._center_project_create_setup()
        self._center_project_setup()

    def _center_project_import_setup(self):

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center/project"), setObjectName="main", setFixedHeight=450,
                        setLayout=self.create_layout(qt.Qw.QHBoxLayout, "/center/project"))
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center/project/import"), setObjectName="main-top", setMaximumWidth=450, setMinimumWidth=200,
                        setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center/project/import"))
        
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/project/import/icon"), setText="** IMPORT ICON **")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/project/import/text"), setText="You can import from a repository or a local folder.")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/center/project/import/button"), setText="Import")
        
    def _center_project_create_setup(self):

        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center/project/create"), setObjectName="main-top", setMaximumWidth=450, setMinimumWidth=200,
                        setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center/project/create"))
        
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/project/create/icon"), setText="** CREATE ICON **")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/center/project/create/text"), setText=self.wrapText(
            "Create with AI assistance your own project structure that can later be moved towards a github repository.", 60))
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/center/project/create/button"), setText="Create")

    def _center_project_setup(self):
        self.connect_signal(onePerOne=True, widgets=(self.get_widget("/center/project/import/button"), self.get_widget("/center/project/create/button")), signals=(
            {"clicked": self.import_menu}, {"clicked": self.create_menu}
        ))

        self.addToLayout(self.get_widget("/center/project/import", "layouts"), ("/center/project/import/icon", "/center/project/import/text", "/center/project/import/button"))
        self.addToLayout(self.get_widget("/center/project/create", "layouts"), ("/center/project/create/icon", "/center/project/create/text", "/center/project/create/button"))

        self.addToLayout(self.get_widget("/center/project", "layouts"), ("-s1", ("/center/project/import", 7), ("/center/project/create", 7), "-s1"))
        self.edit_widget(self.get_widget("/center/project", "layouts"), setSpacing=32)
        self.addToLayout(self.get_widget("/center", "layouts"), (("/center/title", 1), ("/center/title/subtitle", 1), ("/center/project", 1), "-s22"))
        self.edit_widget(self.get_widget("/center", "layouts"), setSpacing=0)