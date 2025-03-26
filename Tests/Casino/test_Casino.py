import unittest
from Application.Casino.Casino import *

class test_Casino(unittest.TestCase):

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
        actual: str = print_welcome()
        self.assertEqual(expected.strip(), actual.strip())