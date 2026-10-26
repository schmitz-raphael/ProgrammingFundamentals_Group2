"""Shared helpers for the room tests."""
import contextlib
import io
import os
import tempfile
import unittest

from escaperoom.Engine.gamestate import GameState


class LikeTranscriptor:
    """Stand-in for Transcriptor: stores the lines written to it."""

    def __init__(self):
        self.lines = []

    def write_line(self, line):
        self.lines.append(line)


class RoomTest(unittest.TestCase):
    """Base class: real GameState, fake transcriptor, temp folder."""

    def setUp(self):
        self.gamestate = GameState()
        self.transcriptor = LikeTranscriptor()
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = folder.name

    def make_file(self, name, text):
        """Create a file in the temp folder and return its path."""
        path = os.path.join(self.folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path.replace("\\", "/")  # forward slashes: DNSRoom splits on "/"

    def run_room(self, room, path):
        """Run room.solve and return what it printed."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            room.solve(self.gamestate, self.transcriptor, path)
        return out.getvalue()