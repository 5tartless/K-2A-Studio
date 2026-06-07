from app.utils.CustomPyQt import CMenuBar, CContextMenu
from app.utils import file_manager as fm, project_manager as pt
from app.utils.code_manager import code_manager
from app.ui.components.tab_manager import TabManager
from app.ui.menus.project_editor import ProjectEditorMenu

class EditorMenuBar(CMenuBar):
    def __init__(self, menu: ProjectEditorMenu, tab_manager: TabManager, parent=None):
        super().__init__(parent)

        self.menus["file"].add_defaults()
        self.set_menu_action_callback("file", "new_file", tab_manager.add_tab)
        self.set_menu_action_keybind("file", "new_file", "Ctrl+N")
        self.set_menu_action_callback("file", "open_file", tab_manager.add_tab_from_path)
        self.set_menu_action_keybind("file", "open_file", "Ctrl+O")
        self.set_menu_action_callback("file", "save", menu.save_tab)
        self.set_menu_action_keybind("file", "save", "Ctrl+S")
        self.set_menu_action_callback("file", "save_as", lambda: menu.save_tab(True))
        self.set_menu_action_keybind("file", "save_as", "Ctrl+Shift+S")
        self.set_menu_action_callback("file", "exit", pt.get_parent_recursive(self, 2).close)
        self.set_menu_action_keybind("file", "exit", "Ctrl+Q")

        self.menus["edit"].add_action("preferences", "Preferences")
        self.menus["edit"].add_action("auto_save", "Enable Auto Save")
        self.set_menu_action_callback("edit", "auto_save", code_manager.toggle_auto_save)
        self.menus["edit"].add_defaults()
        self.set_menu_action_callback("edit", "undo", menu.get_widget("/center/workspace/editor").history_do)
        self.set_menu_action_callback("edit", "redo", lambda: menu.get_widget("/center/workspace/editor").history_do(True))
        self.set_menu_action_callback("edit", "cut", lambda: menu.get_widget("/center/workspace/editor").clipboard_do("cut"))
        self.set_menu_action_callback("edit", "copy", lambda: menu.get_widget("/center/workspace/editor").clipboard_do("copy"))
        self.set_menu_action_callback("edit", "paste", lambda: menu.get_widget("/center/workspace/editor").clipboard_do("paste"))

        self.add_menu("view", CContextMenu, title="View")
        self.menus["view"].add_action("editor_appearance", "Editor Appearance")
        self.menus["view"].add_action("menu_bar", "Show Menu Bar")
        self.menus["view"].addSeparator()
        self.menus["view"].add_action("file_explorer", "Show File Explorer")
        self.menus["view"].add_action("chat", "Show Chat")
        self.menus["view"].add_action("swap_chat_and_file_explorer", "Swap Both")
        self.menus["view"].addSeparator()
        self.menus["view"].add_action("tab_bar", "Show Tab Bar")

        self.set_menu_action_callback(
            "view", "menu_bar",
            lambda: menu.toggleWidgetVisible(menu.get_widget("/top/menu-bar"))
        ); self.set_menu_action_keybind("view", "menu_bar", "Ctrl+Shift+M")
        
        self.set_menu_action_callback(
            "view", "file_explorer",
            lambda: menu.get_widget("/center/workspace").toggle_collapse_widget(menu.get_widget("/center/workspace/file-explorer"))
        ); self.set_menu_action_keybind("view", "file_explorer", "Ctrl+B")
        
        self.set_menu_action_callback(
            "view", "chat",
            lambda: menu.get_widget("/center/workspace").toggle_collapse_widget(menu.get_widget("/center/workspace/chat-view"))
        ); self.set_menu_action_keybind("view", "chat", "Ctrl+Shift+B")
        
        self.set_menu_action_callback(
            "view", "swap_chat_and_file_explorer",
            lambda: menu.get_widget("/center/workspace").reverse_order(
                menu.get_widget("/center/workspace/chat-view"),
                menu.get_widget("/center/workspace/file-explorer")
            )
        )

        self.set_menu_action_callback(
            "view", "tab_bar",
            lambda: menu.toggleWidgetVisible(menu.get_widget("/tab-bar"))
        ); self.set_menu_action_keybind("view", "tab_bar", "Ctrl+Shift+T")
