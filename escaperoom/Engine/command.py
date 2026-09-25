class Command:
    def run(self, engine):
        raise NotImplementedError



class LookCommand (Command):
    def run(self, engine):
        print(engine.gamestate.currentRoom.description)