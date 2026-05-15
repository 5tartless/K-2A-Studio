from PyQt5 import QtCore, QtWidgets as Qw, QtGui, QtWebEngineWidgets, QtWebChannel
import os, sys

class CCore():
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.widgets = {}
        self.layouts = {}
    def get_style(self, path: str) -> str:
        path = self.getAbsolutePath(path)
        if not os.path.exists(path): return ""
        with open(path, "r") as file: return file.read()
    def create_widget(self, widget: any, name: str, store_in: str = "", args: list | dict = [], createVisible: bool = True) -> any: #creates a widget locally
        if (not name in self.widgets) if not store_in else (not name in getattr(self, store_in)):
            if type(args) == list: value = widget(self, *args)
            else: value = widget(self, **args)
            #value = widget(self, *[] if not args else args) if type(args) == list else widget(self, **args)
            if not store_in:
                self.widgets[name] = value
                self.edit_widget(self.widgets[name], **{"show":None} if createVisible else {})
                return self.widgets[name]
            else:
                store_side = getattr(self, store_in)
                store_side[name] = value; self.edit_widget(store_side[name], show=None)
                return store_side[name]
    def create_layout(self, layout: Qw.QLayout, name: str, store_in: str = ""):
        newLayout = layout()
        if (not name in self.layouts) if not store_in else (not name in getattr(self, store_in)):
            if not store_in: self.layouts[name] = newLayout
            else: store_side = getattr(self, store_in); store_side[name] = newLayout
        return newLayout
    def addToLayout(self, layout: Qw.QLayout, items: str | tuple[str], from_where: str = None):
        store_in = getattr(self, from_where) if from_where else self.widgets
        if type(items) == tuple:
            for item in items:
                if type(item) == tuple: self.edit_widget(layout, addWidget=(store_in[item[0]], *item[1:]))
                else:
                    if item[:2] != "-s": self.edit_widget(layout, addWidget=store_in[item])
                    else: self.edit_widget(layout, addStretch=int(item[2:]))
        else: self.edit_widget(layout, addWidget=store_in[items])
    def find(self, obj_in: any, what: any) -> int:
        finder = 0
        for i in obj_in:
            if i == what: return finder
            finder += 1
    def edit_widget(self, widget, **kwargs): #edits a label by passing methods and arguments like this: setText="MyText"
        widgetOptions = [getattr(widget, func) for func in kwargs if hasattr(widget, func)]
        args = {} #label.setText : [kwargs["setText"]] if "setText" in kwargs else []... like this but in a lot of lines of code
        for newArg in widgetOptions: args[newArg] = [kwargs[newArg.__name__]] if newArg.__name__ in kwargs else [] #automates doing the process manually and eventually increasing the dictionary's size in the script
        while True: #if there is a tuple/list in args it converts it by moving the tuple's/list's content into args
            for argument in args:
                if len(args[argument]) > 0:
                    for func in args[argument]:
                        if type(func).__name__ in ["tuple", "list"]:
                            tempArgData = args[argument][self.find(args[argument], func)]; args[argument].remove(tempArgData)
                            for value in tempArgData: args[argument].append(value)
                            continue
            break
        for argument in args.keys():
            if len(args[argument]) > 0: argument(*args[argument]) if not args[argument][0] == None else argument()
    def get_widget(self, name: str, fromWhere: str = "widgets") -> any:
        if hasattr(self, fromWhere):
            store = getattr(self, fromWhere)
            if not name in store: return None
            return store[name]
        else: return None
    def wrapText(self, text: str, word_limit: int) -> str: #** 1.86)
        lines = []
        current_line = ""
        for word in text.split(" "):
            if len(current_line) + len(word) + 1 <= word_limit: current_line += word+" "
            elif len(word) > word_limit:
                if current_line:
                    lines.append(current_line)
                    current_line = ""
                for i in range(0, len(word), word_limit):
                    lines.append(word[i:i+word_limit])
            else:
                lines.append(current_line)
                current_line = word+" "
        if current_line: lines.append(current_line)
        return "\n".join(lines)
    def connect_signal(self, widgets: tuple, signals: tuple[dict] | dict, onePerOne: bool = False) -> None:
        if isinstance(signals, tuple):
            for i, d in enumerate(signals):
                for signal in d:
                    for j, widget in enumerate(widgets):
                        if j == i:
                            if hasattr(widget, signal): getattr(widget, signal).connect(d[signal])
        else:
            for widget in widgets:
                for signal in signals:
                    if hasattr(widget, signal): getattr(widget, signal).connect(signals[signal])
                    if onePerOne: break
    def deleteWidgets(self, widgets: str | tuple, fromWhere: str = "widgets") -> None:
        if hasattr(self, fromWhere):
            store = getattr(self, fromWhere)
            try: badWidgets = [store[widget] for widget in widgets] if type(widgets) == list else [store[widgets]]
            except KeyError: print(f"WARNING: No widget in: {fromWhere}, aborting operation..."); return
            for toDelete in badWidgets:
                toDelete.deleteLater()
                if type(widgets) == list:
                    for widget in widgets: del store[widget]
                else: del store[widgets]
    def restoreLayout(self, layouts: str | tuple[str], fromWhere: str = "layouts"):
        if hasattr(self, fromWhere):
            store = getattr(self, fromWhere)
            def restore(layout: any):
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        WidgetItem = item.widget()
                        WidgetItem.setParent(None)
                    elif item.layout(): self.restoreLayout(item.layout())
            if type(layouts) in [tuple, list]:
                for layout in layouts: restore(store[layout])
            else: restore(store[layouts])
    def getAbsolutePath(self, relative: str) -> str:
        base = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base, relative)
    
    def reloadStyleSheet(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class CMainWindow(CCore, Qw.QMainWindow):
    def __init__(self, window: Qw.QApplication = None, winName: str = "KaModel", winSize: tuple = (800,600), cssRelativePath: str = "", debug: bool = False, parent = None):
        super().__init__()
        if cssRelativePath: self.cssStyle = self.get_style(cssRelativePath); self.cssPath = cssRelativePath
        if window:
            self.edit_widget(self, setGeometry=(600,300,winSize[0],winSize[1]), show=None, setWindowTitle=winName)
            self.setCentralWidget(self.create_widget(Qw.QStackedWidget, "stackedMenus"))
        self.debug = debug
        self.current_menu_index: int = None
    def showMenu(self, index: int, **kwargs): 
        self.get_widget("stackedMenus").setCurrentIndex(index)
        self.get_widget("stackedMenus").currentWidget().appear(**kwargs)
        self.current_menu_index = index
    def addMenu(self, *widgets):
        for widget in widgets: self.get_widget("stackedMenus").addWidget(widget)

class CMenu(CCore, Qw.QWidget):
    def __init__(self, parent: any, **kwargs):
        super().__init__(parent, **kwargs)
        if "cssRelativePath" in kwargs: self.cssStyle = self.get_style(kwargs["cssRelativePath"])
        if "debug" in kwargs: self.debug = kwargs["debug"]

    def showEvent(self, a0):
        return super().showEvent(a0)
    
    def hideEvent(self, a0):
        return super().hideEvent(a0)
    
    
    def appear(self, **kwargs): self.show()
    def setAllStyleSheet(self, ss):
        for widget in self.widgets:
            self.get_widget(widget).setStyleSheet(ss)
            if isinstance(widget, CFrame): widget.setAllStyleSheet(ss)
    def getMainWindow(self) -> CMainWindow:
        return self.parent().parent()

class Worker(QtCore.QThread):
    workerFinished = QtCore.pyqtSignal(object)
    def __init__(self, *runDatas: tuple[callable], dictionaryWorkMode: bool = False):
        super().__init__()
        self.runDatas: tuple = runDatas; self.dictionaryWorkMode = dictionaryWorkMode
        if len(runDatas) > 1 and not dictionaryWorkMode: print("WARNING: You gave more than one *args to this Worker, to allow compatibility with more than one arg, set the dictionaryWorkMode keyword to True")
    def run(self):
        if self.dictionaryWorkMode:
            joinedDatas: dict = {}
            for func in self.runDatas:
                newItems: tuple = tuple(func().items())
                joinedDatas[newItems[0][0]] = newItems[0][1]
            self.workerFinished.emit(joinedDatas)
        else: self.workerFinished.emit(self.runDatas[0]())

class AnimationPlayer(CCore):
    changedAnimationLoop = QtCore.pyqtSignal(object)
    def __init__(self, *args):
        super().__init__(*args)
        self.isPlaying = False
    def play(self): self.isPlaying = True
    def stop(self): self.isPlaying = False

class AnimationPainter(AnimationPlayer, Qw.QWidget):
    def __init__(self, parent = None, size = None):
        super().__init__(parent)
        if size: self.setMinimumSize(*size)
        self.iVariables: dict = {}
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.animation = None
    def play(self, animation: callable, oneShotTime: bool = False, duration: int = 16):
        super().play(duration)
        self.animation = animation
        if oneShotTime:
            self.timer.setSingleShot(True)
        self.timer.start(duration)
    def stop(self): super().stop(); self.timer.stop()
    def paintEvent(self, event):
        if self.animation: self.animation()
class AnimationFader(AnimationPlayer, Qw.QGraphicsOpacityEffect):
    def __init__(self, parent: any, *args):
        super().__init__(*args)
        self.setOpacity(1)
        self.setParent(parent)
        self.parent().setGraphicsEffect(self)
        self.faderPlayer = QtCore.QPropertyAnimation(self, b"opacity")
        
    def play(self, duration: int, startValue: int = 1, middleValue: int = 0, endValue: int = 1, skipEndValue: bool = False, middleFunction: callable = None,
            easingCurve: QtCore.QEasingCurve = QtCore.QEasingCurve.InOutQuad):
        self.setOpacity(startValue)
        def end_value_finished(): self.isPlaying = False; self.faderPlayer.finished.disconnect(end_value_finished)
        def unfade():
            if middleFunction: middleFunction()
            self.faderPlayer.finished.disconnect(unfade)
            if not skipEndValue: 
                self.connect_signal((self.faderPlayer, ), {"finished": end_value_finished}, True)
                self.edit_widget(self.faderPlayer, setStartValue=middleValue, setEndValue=endValue, start=None)
            else: self.isPlaying = False
        self.connect_signal((self.faderPlayer, ), {"finished":unfade}, True)
        self.edit_widget(self.faderPlayer, setDuration=duration, setEasingCurve=easingCurve, setStartValue=startValue, setEndValue=middleValue)

        self.faderPlayer.start()
        super().play()

    def stop(self): 
        self.faderPlayer.stop()
        super().stop()

class SetVar():
    def __init__(self, value: any, callback: callable):
        self._value = value
        self._callback = callback
    @property
    def value(self): return self._value
    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self._callback(self.value)

class CTextEdit(Qw.QTextEdit):
    def __init__(self, parent = None, enterConnection: callable = None, triggeredOnTextChanged: list[callable] = None):
        super().__init__(parent)
        self.enterConnection: callable = enterConnection
        self.triggeredOnTextChanged = triggeredOnTextChanged
        self.setLineWrapMode(self.WidgetWidth)
        self.textChanged.connect(self.adjustHeight)
        self.minH = None; self.maxH = None

    def adjustHeight(self):
        if not self.minH and not self.maxH:
            self.minH = self.minimumHeight(); self.maxH = self.maximumHeight()
        doc_height = self.document().size().height()
        new_height = min(max(self.minH, int(doc_height) + 10), self.maxH)
        self.setFixedHeight(new_height)
        if new_height >= self.maxH: self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        else: self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if self.triggeredOnTextChanged:
            for func in self.triggeredOnTextChanged: func()
    def keyPressEvent(self, e):
        if e.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            if self.enterConnection: self.enterConnection()
            return
        super().keyPressEvent(e)

class CTable(Qw.QTableWidget):
    def __init__(self, parent: any, rows: int = 3, columns: int = 3): super().__init__(rows, columns, parent)
    def addItem(self, x: int, y: int, text: str = ""): self.setItem(x, y, Qw.QTableWidgetItem(text))
    def setHHeaderLabels(self, items: list): self.setHorizontalHeaderLabels(items)
    def setVHeaderLabels(self, items: list): self.setVerticalHeaderLabels(items)

class CFrame(CCore, Qw.QFrame):
    #could act as a card or just a frame that contains more widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ltype = kwargs.get("layout", None)
        self.lname = kwargs.get("name", None)
        object_name = kwargs.get("object_name", None)

        if self.ltype: self.create_layout(self.ltype, self.lname)
        if object_name: self.setObjectName(object_name)

        self.setLayout(self.get_widget(self.lname, "layouts"))
    
    def setAllStyleSheet(self, ss):
        for widget in self.widgets:
            self.get_widget(widget).setStyleSheet(ss)
            if isinstance(widget, CFrame): widget.setAllStyleSheet(ss)
    
    def addToLayout(self, items, to: object = None, from_where: str = None):
        return super().addToLayout(to or self.get_widget(self.lname, "layouts"), items, from_where)
        
class PollCLineEdit(CFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, layout=Qw.QHBoxLayout, **kwargs)

        self.edit_widget(self.create_widget(kwargs.get("title_type", Qw.QLabel), "/title"))
        self.edit_widget(self.create_widget(Qw.QLineEdit, "/line-edit"))

        self.addToLayout(("/title", "/line-edit"))
    
    def setPlaceholderText(self, txt: str):
        self.get_widget("/line-edit").setPlaceholderText(txt)
    def setLineEditText(self, txt: str):
        self.get_widget("/line-edit").setText(txt)
    
    def setTitleText(self, txt: str):
        self.get_widget("/title").setText(txt)

    def getTitle(self) -> object:
        return self.get_widget("/title")
    def getLineEdit(self) -> object:
        return self.get_widget("/line-edit")
    
class CBridge(QtCore.QObject):
    def __init__(self, parent=None, value = None):
        super().__init__(parent)
        self.value = None
    
        @QtCore.pyqtSlot(type(self.value))
        def on_value_changed(value):
            self.value = value
            print("value: ", value)
        self.on_value_changed = on_value_changed
