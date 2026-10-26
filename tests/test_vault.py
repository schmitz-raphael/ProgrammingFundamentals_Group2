"""Tests for VaultRoom."""
from escaperoom.rooms.vault import VaultRoom
from tests.helpers import RoomTest


class TestVault(RoomTest):
    def setUp(self):
        super().setUp()
        self.room = VaultRoom()

    def test_spacing_preserved(self):
        match = VaultRoom.find_SAFE.search("x SAFE { 10 - 20 - 30 } y")
        self.assertEqual(match.group(0), "SAFE { 10 - 20 - 30 }")

    def test_finds_valid_candidate(self):
        path = self.make_file("vault_dump.txt", "SAFE{1-2-4}\nnoise\nSAFE { 10 - 20 - 30 }\n")
        self.run_room(self.room, path)
        self.assertEqual(self.gamestate.tokens["SAFE"], "10-20-30")
        self.assertEqual(self.transcriptor.lines[1], 'EVIDENCE[SAFE].MATCH="SAFE { 10 - 20 - 30 }"')

    def test_no_candidate(self):
        path = self.make_file("vault_dump.txt", "SAFE{1-2-4}\nnoise\n")
        self.run_room(self.room, path)
        self.assertEqual(self.transcriptor.lines, [])