from app.utils import CustomPyQt as qt, project_creator as pt

class PSCardLocal(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/icon"), setObjectName="main-top", setText="*ICON*")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/title"), setObjectName="main-top", setText="Import Local Folder")
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/subtitle"), setObjectName="main-top", setText="Offline & Private")

        self.create_widget(SelectDirectoryLocal, "/select-directory", args={"layout": qt.Qw.QVBoxLayout, "name": "/select-directory", "object_name": "main"})
        self.create_widget(ReviewDirectoryLocal, "/review-directory", args={"layout": qt.Qw.QVBoxLayout, "name": "/review-directory", "object_name": "main"})
        self.create_widget(qt.Qw.QStackedWidget, "/stack")
        self.addToLayout(self.get_widget("/center/options/local", "layouts"), (
            "/icon", "/title", "/subtitle", "/stack"
        ))
        
        self.get_widget("/stack").addWidget(self.get_widget("/select-directory"))
        self.get_widget("/stack").addWidget(self.get_widget("/review-directory"))
        self.get_widget("/stack").setCurrentIndex(0)

class SelectDirectoryLocal(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/button"), setObjectName="main-top", setText="Select Directory")
        self.connect_signal((self.get_widget("/button"),), {"clicked": lambda: self.select_clicked()})

        self.addToLayout(self.get_widget("/select-directory", "layouts"), "/button")
    
    def select_clicked(self):
        path = qt.Qw.QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if pt.path_exists(path):
            pt.get_parent_recursive(self, 2).get_widget("/review-directory").get_path(path)
            pt.get_parent_recursive(self, 2).get_widget("/stack").setCurrentIndex(1)



class ReviewDirectoryLocal(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None
        self.edit_widget(self.create_widget(qt.PollCLineEdit, "/directory-poll", args={"title_type": qt.Qw.QPushButton, "name": "/directory-poll", "object_name": "main"}),
                        setTitleText="Explore")
        self.create_widget(ButtonBox, "/button-box", args={"layout": qt.Qw.QHBoxLayout, "name": "/button-box", "object_name": "main"})
        self.edit_widget(self.create_widget(qt.Qw.QLabel, "/directory-poll/result"), setObjectName="main")
        

        self.connect_signal((self.get_widget("/directory-poll").getTitle(),), {"clicked": lambda: self.get_path(qt.Qw.QFileDialog.getExistingDirectory(self, "Select Project Folder", self.path))})
        self.addToLayout(self.get_widget("/review-directory", "layouts"), ("/directory-poll", "/directory-poll/result", "/button-box"))
    
    def get_path(self, path): #for qfiledialog
        self.path = self.path if not path else path
        self.get_widget("/directory-poll").setLineEditText(self.path)

    def set_result_text(self, text: str):
        text = self.wrapText(text, 60)
        self.get_widget("/directory-poll/result").setText(text)
        
        # if not pt.path_exists(self.path): return
        #see if there is an existing project
        # if pt.is_project(self.path):
            # pass

class ButtonBox(qt.CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/select"), setObjectName="main", setText="Select")
        self.edit_widget(self.create_widget(qt.Qw.QPushButton, "/cancel"), setObjectName="main", setText="Cancel")
        self.connect_signal((self.get_widget("/select"), self.get_widget("/cancel")), ({"clicked": lambda: self.select(
            self.parent().get_widget("/directory-poll").getLineEdit().text()
        )}, {"clicked": lambda: self.cancel()}) )
        
        
        self.addToLayout(self.get_widget("/button-box", "layouts"), ("/select", "/cancel"))

    def cancel(self):
        self.parent().get_widget("/directory-poll").getLineEdit().clear()
        self.parent().set_result_text("")
        pt.get_parent_recursive(self, 3).get_widget("/stack").setCurrentIndex(0)

    def select(self, path):
        message = pt.import_local_project(path)
        if message:
            self.parent().set_result_text(message)
            return
        self.cancel()

