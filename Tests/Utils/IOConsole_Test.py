import unittest

from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole


class IO_Console_Tests(unittest.TestCase):

    def test_constructor_no_color(self):
        subject = IOConsole()
        self.assertEqual(subject.color, ANSI_COLORS.RED)

    def test_constructor_blue(self):
        subject = IOConsole(color=ANSI_COLORS.BLUE)
        self.assertEqual(subject.color, ANSI_COLORS.BLUE)

    def test_constructor_type_error(self):
        with self.assertRaises(TypeError):
            IOConsole(color="red")
