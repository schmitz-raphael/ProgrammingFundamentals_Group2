
from dataclasses import dataclass, field

from escaperoom.transcript import Transcriptor

@dataclass
class GameState:
    current_room: str = "intro"
    inventory: set[str] = field(default_factory=set)
    tokens: dict[str, str] = field(default_factory=dict)

class Room:
    def __init__(self, name: str, description: str, item: str):
        self.name = name
        self.description = description
        self.item = item

    def solve(self, state: GameState, transcriptor: Transcriptor):
        raise NotImplementedError