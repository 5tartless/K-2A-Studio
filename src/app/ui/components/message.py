from app.utils.CustomPyQt import CFrame, Qw, QtCore

class MessageContainer(CFrame):
    class MessageBubble(CFrame):
        def __init__(self, parent, *args, layout=Qw.QHBoxLayout, **kwargs):
            super().__init__(parent, layout=layout, *args, **kwargs)

        def set_text(self, text: str):
            self.edit_widget(
                self.create_widget(
                    Qw.QLabel,
                    "/message-label",
                ) if not self.get_widget("/message-label") else self.get_widget("/message-label"),
                # setObjectName="message-text",
                setWordWrap=True,
                setText=self.wrap_text(text, 6, 16),
                setTextInteractionFlags=QtCore.Qt.TextSelectableByMouse,
                setCursor=QtCore.Qt.IBeamCursor,
                setSizePolicy=(Qw.QSizePolicy.Preferred, Qw.QSizePolicy.Minimum)
            )
            self.style().polish(self.get_widget("/message-label"))
            self.addToLayout("/message-label")

    def __init__(self, parent, text: str, from_, *args, layout=Qw.QHBoxLayout, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)
        self.message_bubble = self.create_widget(
            self.MessageBubble,
            "/message-bubble"
        )
        self.edit_widget(
            self.message_bubble,
            set_text=text,
            setMinimumHeight=32,
            setSizePolicy=(Qw.QSizePolicy.Preferred, Qw.QSizePolicy.Minimum)
        )

        self.from_ = from_
        layout = self.get_widget(self.lname, "layouts")
        if self.from_ == "user":
            self.message_bubble.setObjectName("user-message")
            layout.setAlignment(QtCore.Qt.AlignRight)
        elif self.from_ == "assistant":
            self.message_bubble.setObjectName("assistant-message")
            layout.setAlignment(QtCore.Qt.AlignLeft)
        else:
            self.message_bubble.setObjectName("system-message")
            layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.addToLayout("/message-bubble")
