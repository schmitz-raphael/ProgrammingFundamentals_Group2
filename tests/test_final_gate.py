"""Tests for FinalGate."""
import hashlib
import hmac

from escaperoom.rooms.gate import FinalGate
from tests.helpers import RoomTest

CONFIG = "group_id=G7\ntoken_order=SAFE,KEYPAD,DNS,PID\nhmac_key=secretkey\n"
TOKENS = {"KEYPAD": "54", "SAFE": "10-20-30", "DNS": "ALPHA42", "PID": 5}


def expected_hmac(key, msg):
    return hmac.new(key.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()


class TestFinalGate(RoomTest):
    def setUp(self):
        super().setUp()
        self.room = FinalGate()

    def test_message_and_hmac(self):
        self.gamestate.tokens.update(TOKENS)
        self.run_room(self.room, self.make_file("final_gate.txt", CONFIG))
        msg = "G7|10-20-30-54-ALPHA42-5"
        self.assertEqual(self.transcriptor.lines, [
            "FINAL_GATE=PENDING",
            f"MSG=<{msg}>",
            f"HMAC=<{expected_hmac('secretkey', msg)}>",
        ])

    def test_token_order_comes_from_the_file(self):
        self.gamestate.tokens.update(TOKENS)
        cfg = "group_id=G7\ntoken_order=PID,DNS,KEYPAD,SAFE\nhmac_key=secretkey\n"
        self.run_room(self.room, self.make_file("final_gate.txt", cfg))
        self.assertEqual(self.transcriptor.lines[1], "MSG=<G7|5-ALPHA42-54-10-20-30>")

    def test_not_enough_tokens(self):
        self.gamestate.tokens["SAFE"] = "1-2-3"
        output = self.run_room(self.room, self.make_file("final_gate.txt", CONFIG))
        self.assertIn("not in possession", output)
        self.assertEqual(self.transcriptor.lines, [])