import unittest
from unittest.mock import patch

from Application.Casino.Casino import *

class test_Casino(unittest.TestCase):

    @patch("Application.Casino.AccountManager.read_from_csv", return_value=[])
    def setUp(self, mock_read_from_csv):
        self.casino = Casino()

    def test_print_welcome(self):
        expected: str = r"""[34m
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888 
        """
        actual: str = self.casino.print_welcome()
        self.assertEqual(expected.strip(), actual.strip())

    @patch("Application.Casino.AccountManager.AccountManager.get_account",
           return_value=CasinoAccount("test_username", "test_password", 0.0))
    @patch("Application.Utils.IOConsole.IOConsole.get_string_input", side_effect=["test_username", "test_password"])
    def test_handle_login(self, mock_inputs, mock_get_account):
        account: CasinoAccount = self.casino.handle_login()

        expected_username = "test_username"
        expected_password = "test_password"
        expected_balance = 0.0

        actual_username = account.username
        actual_password = account.password
        actual_balance = account.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)
