class Controller:
    def __init__(self, engine):
        self.commands = {}
        self.engine = engine

    def register(self, keyword, command):
        self.commands[keyword] = command

    def execute(self, command_keyword, arguments):
        if self.commands[command_keyword]:
            self.commands[command_keyword].run()