from app.utils import CustomPyQt as qt

class K2A_Menu(qt.CMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._top_center_setup()


        self.addToLayout(self.create_layout(qt.Qw.QVBoxLayout, "/"), (("/top"), ("/center")))
        self.setLayout(self.get_widget("/", "layouts"))

    def home_menu(self):
        main_window = self.getMainWindow()
        if main_window.current_menu_index != 0:
            main_window.menu_fader.play(duration=100, startValue=1, middleValue=0, endValue=1, skipEndValue=False, middleFunction=lambda: main_window.showMenu(0, animate=False))

    def _top_center_setup(self):
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top"), setObjectName="main-top",
                        setFixedHeight=80, setLayout=self.create_layout(qt.Qw.QHBoxLayout, "/top"))
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/top/logo"), setObjectName="main", setFixedWidth=64, setText="*LOGO*")
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/top/nav-bar"), setObjectName="main", setLayout=self.create_layout(qt.Qw.QHBoxLayout, "/top/nav-bar"))
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/top/nav-bar/button/home"), setText="Home")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/top/nav-bar/button/manage-projects"), setText="Projects")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/top/nav-bar/button/settings"), setText="Settings")

        self.addToLayout(self.get_widget("/top/nav-bar", "layouts"), ("/top/nav-bar/button/home", "/top/nav-bar/button/manage-projects", "/top/nav-bar/button/settings"))
        self.addToLayout(self.get_widget("/top", "layouts"), ("/top/logo", "/top/nav-bar"))
    
    
        self.connect_signal((self.get_widget("/top/nav-bar/button/home"),), {"clicked": self.home_menu})
        self.edit_widget(self.create_widget(qt.Qw.QWidget, "/center"), setObjectName="main-top",
                        setMinimumHeight=240, setLayout=self.create_layout(qt.Qw.QVBoxLayout, "/center"))