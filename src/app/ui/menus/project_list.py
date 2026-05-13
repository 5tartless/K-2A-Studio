from app.utils import CustomPyQt as qt, project_manager as pt
from app.ui.menus._basic_menu import K2A_Menu

class ProjectListMenu(K2A_Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setAllStyleSheet(self.cssStyle)

        self.edit_widget(self.create_widget(ProjectList, "/center/project-list", args={"layout": qt.Qw.QVBoxLayout, "name": "/center/project-list", "object_name": "scroll-bar"}))
        self.edit_widget(self.create_widget(qt.Qw.QScrollArea, "/center/project-scroll-area"), setWidgetResizable=True, setObjectName="scroll-bar",
                        setWidget=self.get_widget("/center/project-list"))
        
        self.addToLayout(self.get_widget("/center", "layouts"), "/center/project-scroll-area")
        self.list_projects()
    
    def appear(self, **kwargs):
        self.clear()
        self.list_projects()
        return super().appear(**kwargs)
    
    def getPList(self) -> ProjectList:
        return self.get_widget("/center/project-list")

    def clear(self):
        plist = self.getPList()
        for project in plist.widgets.copy():
            if project.startswith("/projects/"):
                plist.deleteWidgets(project)

    def list_projects(self):
        plist = self.getPList()
        app_projects = pt.list_projects()
        if app_projects:
            for project in app_projects: #list[dict]
                name = f"/projects/{project["pid"]}"
                plist.edit_widget(plist.create_widget(Project, name, args={"name": name, "project_data": project, "object_name": "main"}))
                plist.addToLayout(name)
        else:
            name = "/projects/no-projects-found"
            plist.edit_widget(plist.create_widget(NoProjectsFound, name, args={"layout": qt.Qw.QVBoxLayout, "name": name, "object_name": "main"}))
            plist.addToLayout(name)


class ProjectList(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_widget("/center/project-list", "layouts").setAlignment(qt.QtCore.Qt.AlignTop)
    

class Project(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QHBoxLayout, **kwargs)
        self.setFixedHeight(92)
        self.project_data = kwargs.get("project_data", {})
        self.init_project()
        
        if self.project_data:
            self.get_widget("/project-brief-data").setName(self.project_data["name"])
            self.get_widget("/project-brief-data").setPath(self.project_data["path"])
            self.get_widget("/project-brief-data").setOnGithub("GitHub" if self.project_data["github-url"] else "Local")
            # self.get_widget("project-edit").setVersion()

    def init_project(self):

        self.edit_widget(self.create_widget(ProjectBriefData, "/project-brief-data", args={"name":"/project-brief-data", "object_name": "main"}))
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/manage-button"), setText="Manage")
        self.edit_widget(self.create_widget(ProjectEdit, "/project-edit", args={"name":"/project-edit", "object_name":"main"}))
        self.addToLayout(("/project-brief-data", "/manage-button", "/project-edit"))


class ProjectBriefData(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/name"), setText="Unknown", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/path"), setText="Unknown", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/on-github"), setText="", setObjectName="main")

        self.get_widget(self.lname, "layouts").setSpacing(0)
        self.addToLayout(("/name", "/path", "/on-github"))
    
    def setName(self, txt):
        self.get_widget("/name").setText(txt)
    def setPath(self, txt):
        self.get_widget("/path").setText(txt)
    def setOnGithub(self, txt):
        self.get_widget("/on-github").setText(txt)

class ProjectEdit(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=qt.Qw.QVBoxLayout, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/version"), setText="Version: Unknown", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/edit"), setText="Edit", setObjectName="main")

        self.connect_signal((self.get_widget("/edit"),), {"clicked": self.clickedEdit})
        self.get_widget(self.lname, "layouts").setSpacing(0)
        self.addToLayout(("/version", "/edit"))

    def setVersion(self, txt: str):
        self.get_widget("/version").setText(self.wrapText(txt, 20))
    def clickedEdit(self):
        pass


class NoProjectsFound(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(92)
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setText="No projects were found.", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/subtitle"), setText="You can go to home if you want to add a project.", setObjectName="main")

        self.addToLayout(("/title", "/subtitle"))



