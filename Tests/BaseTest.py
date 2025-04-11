import os.path
import unittest

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.db import init_db


class BaseTset(unittest.TestCase):

    def setUp(self):
        init_db()
        self.manager = AccountManager()


    def tearDown(self):
        if hasattr(self.manager, 'session'):
            self.manager.session.close()

        if os.path.exists("accounts.csv"):
            os.remove("accounts.csv")

        if os.path.exists("casino.db"):
            os.remove("casino.db")