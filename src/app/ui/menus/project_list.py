from app.utils import CustomPyQt as qt
from app.ui.menus._basic_menu import K2A_Menu

class ProjectListMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setAllStyleSheet(self.cssStyle)
    
    def appear(self, **kwargs):
        return super().appear(**kwargs)