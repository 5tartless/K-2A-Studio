from app.utils import CustomPyQt as qt, project_creator as pt
from app.ui.menus.home_menu import HomeMenu
from app.ui.menus.import_project_menu import ImportProjectMenu
from app.ui.menus.create_project_menu import CreateProjectMenu
from app.ui.menus.project_list import ProjectListMenu

import sys

class K2A_App(qt.CMainWindow):
    def __init__(self, window = None, winName = "KaModel", winSize = ..., cssRelativePath = "", debug = False, parent=None):
        super().__init__(window, winName, winSize, cssRelativePath, debug, parent)
        self.setMinimumWidth(750)

        self.menu_fader = qt.AnimationFader(self.get_widget("stackedMenus"))
        self.addMenu(self.create_widget(HomeMenu, "homeMenu", createVisible=False, 
                                        args={"cssRelativePath": self.cssPath, "debug": self.debug}),
                    self.create_widget(ImportProjectMenu, "importProjectMenu", createVisible=False,
                                       args={"cssRelativePath": self.cssPath, "debug": self.debug}),
                    self.create_widget(CreateProjectMenu, "createProjectMenu", createVisible=False,
                                       args={"cssRelativePath": self.cssPath, "debug": self.debug}),
                    self.create_widget(ProjectListMenu, "projectListMenu", createVisible=False, 
                                        args={"cssRelativePath": self.cssPath, "debug": self.debug}))
        self.showMenu(3)
        
if __name__ == "__main__":
    pt.setup()

    # ui init
    window = qt.Qw.QApplication(sys.argv)
    app = K2A_App(window, winSize=(1080,720), cssRelativePath="src/css/style.css", debug=True)

    sys.exit(window.exec())
