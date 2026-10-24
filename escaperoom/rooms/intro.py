

from escaperoom.Engine.gamestate import GameState
from escaperoom.rooms.base import Room
from escaperoom.transcript import Transcriptor


class IntroRoom (Room):
    def __init__(self):
        super().__init__("intro",
                          "A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final.",
                            "You should check outer the other rooms.",
                            "Intro Lobby")

    def solve(state: GameState, transcriptor: Transcriptor, item_name: str):
          print("You can't do that here. Consider moving to a different room.")