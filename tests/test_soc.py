"""Tests for SOCRoom."""
from escaperoom.rooms.soc import SOCRoom
from tests.helpers import RoomTest


def example_line(status="Failed", ip="192.168.1.1", timestamp="2026-10-05T09:00:21Z",
                 pid="sshd[1234]:"):
    return f"{timestamp} myhost {pid} {status} password for user from {ip} port 23452 protocol 2"


class TestSOC(RoomTest):
    def setUp(self):
        super().setUp()
        self.room = SOCRoom()

    def test_valid_line(self):
        self.assertTrue(self.room.valid_record(example_line().split()))

    def test_malformed_lines(self):
        bad = [example_line(timestamp="2026-10-05T99:99:99Z"),
               example_line(ip="999.1.1.1"),
               example_line(pid="sshd[abcd]:")]
        for line in bad:
            with self.subTest(line=line):
                self.assertFalse(self.room.valid_record(line.split()))

    def test_token_and_skipped(self):
        lines = ([example_line(ip="192.168.1.1")] * 3 + [example_line(ip="192.168.1.2")]
                 + [example_line(ip="192.168.1.3")] * 2
                 + [example_line(status="Accepted", ip="192.168.1.4")] * 3
                 + ["malformed line"] * 2
                 + [example_line(ip="999.1.1.1"), example_line(pid="sshd[abcd]:")])
        self.run_room(self.room, [l for l in lines] and self.make_file("auth.log", "\n".join(lines) + "\n"))
        self.assertEqual(self.gamestate.tokens["KEYPAD"], "16")
        self.assertEqual(self.transcriptor.lines[2], "EVIDENCE[KEYPAD].COUNT=6")
        self.assertEqual(self.transcriptor.lines[4], "EVIDENCE[KEYPAD].MALFORMED_SKIPPED=4")

    def test_no_failed_records(self):
        path = self.make_file("auth.log", example_line(status="Accepted") + "\n")
        self.run_room(self.room, path)
        self.assertEqual(self.transcriptor.lines, [])