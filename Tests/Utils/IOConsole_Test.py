import unittest
from unittest.mock import patch

from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole


class IO_Console_Tests(unittest.TestCase):

    def setUp(self):
        self.console = IOConsole()

    def test_constructor_no_color(self):
        subject = IOConsole()
        self.assertEqual(subject.color, ANSI_COLORS.RED.value)

    def test_constructor_blue(self):
        subject = IOConsole(color=ANSI_COLORS.BLUE)
        self.assertEqual(subject.color, ANSI_COLORS.BLUE.value)

    def test_constructor_type_error(self):
        with self.assertRaises(TypeError):
            IOConsole(color="red")

    @patch("builtins.input", return_value="test input")
    def test_get_string_input(self, mock_input):
        subject = self.console.get_string_input("Some Prompt")
        self.assertEqual(subject, "test input")
        self.assertTrue(isinstance(subject, str))

    patch("builtins.input", return_value="test input")  # Mock user input

    @patch("builtins.input", return_value="exit")
    def test_exit_called_with_code_0(self, mock_input):
        with self.assertRaises(SystemExit) as sys_exit:
            self.console.get_string_input("Enter something: ")

        self.assertEqual(sys_exit.exception.code, 0)