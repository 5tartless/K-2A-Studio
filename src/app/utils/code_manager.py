class CodeManager():
    def __init__(self):
        self.codes = {

        }
        self.auto_save: bool = False
        #{name: "your code.."}

        self.on_code_changed_callbacks: list = []
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