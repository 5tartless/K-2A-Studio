from app.utils import CustomPyQt as qt
from app.ui.menus._basic_menu import K2A_Menu

class ProjectMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)