from app.utils.CustomPyQt import SetVar, create_timer
class CodeManager():
    def __init__(self):
        self.codes = {

        }
        self.auto_save: bool = False
        self._auto_save_timer = create_timer(interval=250)

        self.on_code_changed_callbacks: list = []
    
    def toggle_auto_save(self):
        new_value = not self.auto_save
        self._auto_save_timer.start() if new_value else self._auto_save_timer.stop()
        self.auto_save = new_value
        print(f"INFO: auto-save state: {self.auto_save}")

    def on_code_changed(self):
        for callback in self.on_code_changed_callbacks:
            callback()
        # print("Code: ", self.codes) #debug

    def code_exists(self, name: str) -> bool:
        return name in self.codes

    def update_code(self, name: str, code: str) -> None:
        self.codes[name] = code
        self.on_code_changed()

    def delete_code(self, name: str) -> str:
        if self.code_exists(name):
            code = self.codes[name]
            del self.codes[name]
            self.on_code_changed()
            return code

    def get_code(self, name: str) -> str:
        return self.codes[name]

code_manager = CodeManager()