import os.path
import unittest

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.db import init_db


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.session = init_db(in_memory=True)
        self.manager = AccountManager(session=self.session)


    def tearDown(self):
        if hasattr(self.manager, 'session'):
            self.manager.session.close()

        if os.path.exists("casino.db"):
            os.remove("casino.db")

        if os.path.exists("category_cache.txt"):
            os.remove("category_cache.txt")