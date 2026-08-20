import sys
import os
import subprocess
from pathlib import Path

os.environ["QT_QPA_PLATFORM"] = "windows"

requirements = Path(__file__).resolve().parent.parent / "requirements.txt"
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements)])

from app.utils import CustomPyQt as qt, project_manager as pt
from app.ui.menus.home_menu import HomeMenu
from app.ui.menus.import_project_menu import ImportProjectMenu
from app.ui.menus.create_project_menu import CreateProjectMenu
from app.ui.menus.project_list import ProjectListMenu
from app.ui.menus.project_editor import ProjectEditorMenu

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
                                args={"cssRelativePath": self.cssPath, "debug": self.debug}),
            self.create_widget(ProjectEditorMenu, "projectEditorMenu", createVisible=False, 
                                args={"cssRelativePath": self.cssPath, "debug": self.debug})
        )
        self.showMenu(0)
    
    def closeEvent(self, a0):
        if self.current_menu_index == 4:
            tab_manager = self.get_widget("projectEditorMenu").get_widget("/tab-bar").get_tab_manager()
            tab_manager.save_all_tabs()
            if not tab_manager.are_all_tabs_saved(): 
                a0.ignore()
                return
        a0.accept()

if __name__ == "__main__":
    pt.setup()

    window = qt.Qw.QApplication(sys.argv)
    app = K2A_App(window, winSize=(1080,720), cssRelativePath="src/css/style.css", debug=True)

    sys.exit(window.exec())
