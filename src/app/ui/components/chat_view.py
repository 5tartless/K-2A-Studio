from app.utils.CustomPyQt import CFrame, CTextEdit, Qw, QtCore, Worker
from app.ui.components.message import MessageContainer
from app.utils import file_manager as fm, project_manager as pt
from app.utils.ai_manager import ai_manager

class ChatView(CFrame):
    message_added = QtCore.pyqtSignal(str, str) 

    def __init__(self, parent, layout=Qw.QVBoxLayout, *args, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)

        self._ai_workers: list = []  # mantiene referencias vivas mientras corren los hilos
        self._ai_busy: bool = False

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
        self.message_added.connect(self.on_message_added)

    def get_editor(self):
        """Recupera la instancia del Editor, hermana del chat dentro del workspace."""
        project_menu = pt.get_parent_recursive(self, 3)
        return project_menu.get_widget("/center/workspace/editor") if project_menu else None

    def on_message_added(self, text: str, from_: str):
        # solo reaccionamos a mensajes escritos por el usuario, no a los del propio bot
        # ni a los mensajes de sistema (como el de "Pensando...")
        if from_ != "user" or self._ai_busy:
            return

        editor = self.get_editor()
        code = (editor.current_code.value or "") if editor else ""
        file_name = editor.get_current_file_name() if editor else ""

        self._ai_busy = True
        chat_container = self.get_widget("/chat-container")
        thinking_name = f"/message-{len(chat_container.widgets)}"
        chat_container.add_message("🤖 Pensando...", from_="system")

        worker = Worker(lambda: ai_manager.chat(text, code, file_name))
        worker.workerFinished.connect(
            lambda result: self.handle_ai_response(result, editor, thinking_name, worker)
        )
        self._ai_workers.append(worker)
        worker.start()

    def handle_ai_response(self, result: dict, editor, thinking_name: str, worker):
        chat_container = self.get_widget("/chat-container")
        chat_container.deleteWidgets(thinking_name, "widgets", False)

        reply = result.get("reply") or "No obtuve una respuesta del modelo."
        chat_container.add_message(reply, from_="assistant")

        suggestions = result.get("suggestions") or []
        if editor:
            if suggestions:
                editor.highlight_suggestions(suggestions)
            else:
                editor.clear_suggestions()

        self._ai_busy = False
        if worker in self._ai_workers:
            self._ai_workers.remove(worker)

class ChatContainer(CFrame):
    def __init__(self, parent, layout=Qw.QVBoxLayout, *args, **kwargs):
        super().__init__(parent, layout=layout, *args, **kwargs)
        
        self.edit_widget(
            self.get_widget(self.lname, "layouts"),
            setAlignment=QtCore.Qt.AlignTop
        )

    def add_message(self, text: str, from_: str = "user"):
        message_name = f"/message-{len(self.widgets)}"
        widget = self.create_widget(
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

        # Igual que con el listado de proyectos: el widget se crea y se agrega al layout,
        # pero su tamaño/render final (sobre todo con texto de varias líneas) puede no
        # calcularse ni pintarse hasta el siguiente ciclo del event loop, "cortando"
        # visualmente el mensaje hasta que algo más fuerza un repintado. Lo forzamos aquí,
        # y de paso hacemos scroll automático hasta el final para ver el mensaje nuevo.
        QtCore.QTimer.singleShot(0, lambda: self._finalize_message(widget))

        pt.get_parent_recursive(self, 3).message_added.emit(text, from_)
        return widget

    def _finalize_message(self, widget):
        widget.adjustSize()
        self.adjustSize()
        self.updateGeometry()
        self.update()
        scroll_area = self.parent()  # ChatContainer vive dentro de un QScrollArea
        if isinstance(scroll_area, Qw.QScrollArea):
            bar = scroll_area.verticalScrollBar()
            bar.setValue(bar.maximum())

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
                    clicked=lambda: self.callback(from_="user"),
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
