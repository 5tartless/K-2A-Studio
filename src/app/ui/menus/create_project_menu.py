from app.utils import CustomPyQt as qt
from app.utils.project_manager import path_exists, create_project, get_parent_recursive, is_project, PROJECT_DEFAULT_SETTINGS
from app.ui.menus._basic_menu import K2A_Menu

class CreateProjectMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # self.setAllStyleSheet(self.cssStyle)
        self.edit_widget(self.create_widget(CreateBox, "/center/create-box", args={"layout": qt.Qw.QVBoxLayout, "name": "/center/create-box", "object_name": "main-top"}))

        self.addToLayout(self.get_widget("/center", "layouts"), "/center/create-box")

    def appear(self, **kwargs):
        return super().appear(**kwargs)
    

class CreateBox(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = ""
        self.can_create: bool = False


        self.edit_widget(self.create_widget(qt.PollCLineEdit, "/project-name", args={"name": "/project-name", "object_name": "main-top"}),
                         setPlaceholderText="Let the inspiration come in...", setTitleText="Project Name: ")
        self.edit_widget(self.create_widget(qt.PollCLineEdit, "/project-directory", args={"name": "/project-directory", "object_name": "main-top", "title_type": qt.Qw.QPushButton}),
                        setTitleText="Explore")
        self.connect_signal((
            self.get_widget("/project-directory").get_widget("/title"), self.get_widget("/project-directory").getLineEdit(), self.get_widget("/project-name").getLineEdit()), (
            {"clicked": lambda: self.explore_pd()}, {"returnPressed": lambda: self.explore_pd(True)}, {"returnPressed": lambda: self.explore_pd(True)}
        ))
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/project-directory/result"), setObjectName="main")

        self.edit_widget(self.create_widget(BottomButtons, "/bottom-buttons", args={"layout": qt.Qw.QHBoxLayout, "name": "/bottom-buttons", "object_name": "main"}))

        self.addToLayout(("/project-name", "/project-directory", "/project-directory/result", "-s1", "/bottom-buttons"))
    
    def explore_pd(self, read_le: bool = False):
        line_edit = self.get_widget("/project-directory").getLineEdit()
        
        result = qt.Qw.QFileDialog.getExistingDirectory(self, "Select or Create Folder", self.path) if not read_le else line_edit.text()
        self.path = self.path if not result else result
        line_edit.setText(self.path)

        path_existance = path_exists(self.path)
        project_name = str(self.get_widget("/project-name").getLineEdit().text())

        message = ""
        self.can_create = False
        if not project_name:
            message = "Please enter a name."
        elif not path_existance:
            message = "Path doesn't exist."
        elif path_existance and is_project(self.path):
            message = self.wrapText("This project already exists. Check it on your project list!", 100)
        else:
            self.can_create = True
            message = "Ok."
        self.get_widget("/project-directory/result").setText(message)
    
    def clear(self):
        self.get_widget("/project-name").getLineEdit().clear()
        self.get_widget("/project-directory").getLineEdit().clear()
        self.get_widget("/project-directory/result").clear()

    def cancel(self):
        self.clear()
        get_parent_recursive(self, 2).home_menu()

    def create_project(self):
        self.explore_pd(True)
        if self.can_create:
            data = PROJECT_DEFAULT_SETTINGS.copy()
            data["path"] = str(self.path)
            data["name"] = str(self.get_widget("/project-name").getLineEdit().text())

            create_project(data)
            get_parent_recursive(self, 2).home_menu()
            self.clear()

class BottomButtons(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/create"), setText="Create", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/export-github"), setText="Export to GitHub", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/dependencies"), setText="Dependencies", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/cancel"), setText="Cancel", setObjectName="main")

        self.connect_signal((self.get_widget("/create"), self.get_widget("/cancel")), (
                {"clicked": lambda: self.parent().create_project()}, {"clicked": lambda: self.parent().cancel()}
            )
        )


        self.addToLayout(("/create", "/export-github", "-s1", "/dependencies", "/cancel"))
    