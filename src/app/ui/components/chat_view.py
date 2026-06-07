from app.utils.CustomPyQt import CFrame, CTextEdit, Qw, QtCore
from app.ui.components.message import MessageContainer
from app.utils import file_manager as fm, project_manager as pt

class ChatView(CFrame):
    message_added = QtCore.pyqtSignal(str, str) 

    def __init__(self, parent, layout=Qw.QVBoxLayout, *args, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)

        self.edit_widget(
            self.create_widget(
                ChatContainer,
                "/chat-container",
                args={"name": "/chat-container", "object_name": "main"}
            ),
            setContentsMargins=(5,5,5,5)
        )
        self.edit_widget(
            self.create_widget(
                Qw.QScrollArea,
                "/chat-scroll-area"
            ),
            setWidgetResizable=True,
            setWidget=self.get_widget("/chat-container")
        )
        self.edit_widget(
            self.create_widget(
                InputArea,
                "/input-area",
                args={"name": "/input-area", "object_name": "main-top"}
            ),
            setMinimumHeight=96,
            setMaximumHeight=256,
            setSizePolicy=(Qw.QSizePolicy.Preferred, Qw.QSizePolicy.Minimum)
        )
        self.addToLayout(("/chat-scroll-area", "/input-area"))

class ChatContainer(CFrame):
    def __init__(self, parent, layout=Qw.QVBoxLayout, *args, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)
        
        self.edit_widget(
            self.get_widget(self.lname, "layouts"),
            setAlignment=QtCore.Qt.AlignTop
        )

    def add_message(self, text: str, from_: str = "user"):
        message_name = f"/message-{len(self.widgets)}"
        self.create_widget(
            MessageContainer,
            message_name,
            args={
                "name": message_name,
                # "object_name": "main",
                "text": text,
                "from_": from_ 
            }
        )
        self.addToLayout(message_name)
        pt.get_parent_recursive(self, 3).message_added.emit(text, from_)

class InputArea(CFrame):
    class InputMessageContainer(CFrame):
        def __init__(self, parent, layout=Qw.QHBoxLayout, callback=None, *args, **kwargs):
            super().__init__(parent, layout=layout, *args, **kwargs)
            self.callback = callback
            self.edit_widget(
                self.create_widget(
                    CTextEdit,
                    "/message-input",
                ),
                setPlaceholderText="Type your message here...",
                adjust_height=None,
                setFocus=True,
            )
            self.edit_widget(
                self.create_widget(
                    Qw.QPushButton,
                    "/send-button",
                ),
                setText="Send"
            )
            if self.callback: 
                self.connect_to_signal(
                    self.get_widget("/send-button"),
                    self.get_widget("/message-input"),
                    clicked=lambda: self.callback(from_="assistant"), #debugging
                    return_pressed=self.callback)
            self.addToLayout(("/message-input", "/send-button"))
            self.get_widget(self.lname, "layouts").setAlignment(self.get_widget("/send-button"), QtCore.Qt.AlignBottom)

    class MiscButtonsContainer(CFrame):
        def __init__(self, parent, layout=Qw.QHBoxLayout, *args, **kwargs):
            super().__init__(parent, layout=layout, *args, **kwargs)
            self.edit_widget(
                self.create_widget(
                    Qw.QPushButton,
                    "/attach-button",
                ),
                setText="+",
                setSizePolicy=(Qw.QSizePolicy.Fixed, Qw.QSizePolicy.Fixed)
            )
            self.get_widget(self.lname, "layouts").setAlignment(QtCore.Qt.AlignLeft)
            self.addToLayout(("/attach-button"))

    def __init__(self, parent, layout=Qw.QVBoxLayout, *args, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)
        self.edit_widget(
            self.create_widget(
                self.InputMessageContainer,
                "/message-container",
                args={"name": "/message-container", "object_name": "main", "callback": self.send_message}
            )
        )
        self.edit_widget(
            self.create_widget(
                self.MiscButtonsContainer,
                "/misc-buttons-container",
                args={"name": "/misc-buttons-container", "object_name": "main"}
            )
        )
        self.addToLayout(("/message-container", "/misc-buttons-container"))

    def send_message(self, from_="user"):
        message_input = self.get_widget("/message-container").get_widget("/message-input")
        message_text = message_input.toPlainText().strip()
        if message_text:
            chat_container = self.parent().get_widget("/chat-container")
            chat_container.add_message(message_text, from_=from_)
            message_input.clear()
            message_input.setFocus(True)
