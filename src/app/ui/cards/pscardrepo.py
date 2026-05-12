from app.utils import CustomPyQt as qt, project_creator as pt

class CloneRepo(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setText="Repository URL:")
        self.edit_widget(self.create_widget(qt.Qw.QLineEdit, "/url"), setPlaceholderText="https://github.com/user/project")
        self.edit_widget(self.create_widget(ButtonsCFrame, "/buttons", args={"layout": qt.Qw.QHBoxLayout, "name": "/buttons", "object_name": "menu"}))
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/result"), setText="", setObjectName="main")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/advice"), setText=self.wrapText("Note:\nYou are about to clone a github repository. This could take a while.", 50))

        self.addToLayout(("/title", "/url", "/result", "/buttons", "/advice"))
    
    def clear(self):
        self.get_widget("/url").clear()
        self.get_widget("/result").clear()

class ReviewRepo(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/import-repo"), setText="Clone Repository", setObjectName="main-top")
        self.connect_signal((self.get_widget("/import-repo"),), {"clicked": lambda: self.parent().setCurrentIndex(1)})
        
        self.addToLayout("/import-repo")

class ButtonsCFrame(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/cancel"), setText="Cancel")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/confirm"), setText="Confirm and Import")

        self.connect_signal((self.get_widget("/cancel"),self.get_widget("/confirm")),
                            ({"clicked": lambda: (pt.get_parent_recursive(self, 2).setCurrentIndex(0), self.parent().clear())},
                            {"clicked": lambda: pt.get_parent_recursive(self, 3).confirm_clone(str(self.parent().get_widget("/url").text()))}))
        self.addToLayout(("/confirm", "/cancel"))



class PSCardRepo(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_widgets()

    def confirm_clone(self, url: str):
        result = pt.import_github_project(url)
        self.get_widget("/clone-repo").get_widget("/result").setText(self.wrapText(result, 50))
        print(result)

    def init_widgets(self):
        self.create_widget(qt.Qw.QStackedWidget, "/stack")

        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/icon"), setObjectName="main-top", setText="*ICON*")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setObjectName="main-top", setText="Import from GitHub")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/subtitle"), setObjectName="main-top", setText="Cloud-Sync")
        self.edit_widget(self.create_widget(CloneRepo, "/clone-repo", args={"layout":qt.Qw.QVBoxLayout, "name": "/clone-repo", "object_name":"main"}))
        self.edit_widget(self.create_widget(ReviewRepo, "/review-repo", args={"layout":qt.Qw.QVBoxLayout, "name": "/review-repo", "object_name":"main"}))
        self.addToLayout(("/icon", "/title", "/subtitle", "/stack"))

        self.get_widget("/stack").addWidget(self.get_widget("/review-repo"))
        self.get_widget("/stack").addWidget(self.get_widget("/clone-repo"))
        self.get_widget("/stack").setCurrentIndex(0)
