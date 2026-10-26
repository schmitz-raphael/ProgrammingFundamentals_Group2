"""Tests for DNSRoom."""
import base64
import codecs
import unittest

from escaperoom.rooms.dns import DNSRoom
from tests.helpers import RoomTest


def b64(text):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def rot13_b64(text):
    return codecs.encode(b64(text), "rot_13")


CONFIG = "\n".join([
    "# DNS hints",
    f"token_tag=b64:{b64('3')}",
    f"hint1=b64:{b64('decoy line ending with WRONG.')}",
    f"hint3=rot13+b64:{rot13_b64('the real token is ALPHA42.')}",
    "other=plain:xxxx",
    "no_equals_sign_here",
]) + "\n"


class TestDNSHelpers(unittest.TestCase):
    def setUp(self):
        self.room = DNSRoom()

    def test_is_valid_line(self):
        self.assertTrue(self.room.is_valid_line("key=value"))
        self.assertFalse(self.room.is_valid_line("# comment=ignored"))
        self.assertFalse(self.room.is_valid_line("no equals sign"))

    def test_parse_line_splits_on_first_equals(self):
        self.assertEqual(self.room.parse_line("a = b=c"), ("a", "b=c"))

    def test_decode_b64(self):
        self.assertEqual(self.room.decode("b64", b64("hello")), "hello")

    def test_decode_rot13_b64(self):
        self.assertEqual(self.room.decode("rot13+b64", rot13_b64("hello")), "hello")

    def test_find_hint(self):
        self.assertEqual(self.room.find_hint({"token_tag": ("b64", "3")}), "hint3")

    def test_extract_token(self):
        self.assertEqual(self.room.extract_token("the real token is ALPHA42."), "ALPHA42")


class TestDNSSolve(RoomTest):
    def setUp(self):
        super().setUp()
        self.room = DNSRoom()

    def test_full_scenario(self):
        self.run_room(self.room, self.make_file("dns.cfg", CONFIG))
        self.assertEqual(self.gamestate.tokens["DNS"], "ALPHA42")
        self.assertEqual(self.transcriptor.lines, [
            "TOKEN[DNS]=ALPHA42",
            "EVIDENCE[DNS].KEY=hint3",
            "EVIDENCE[DNS].ENCODING=rot13+b64",
            "EVIDENCE[DNS].DECODED_LINE=the real token is ALPHA42.",
        ])

    def test_wrong_file_name_is_rejected(self):
        output = self.run_room(self.room, self.make_file("other.cfg", CONFIG))
        self.assertIn("no such item", output)
        self.assertEqual(self.transcriptor.lines, [])