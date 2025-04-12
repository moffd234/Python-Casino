from Application.Casino.Accounts.UserAccount import UserAccount
from Tests.BaseTest import BaseTest


class TestUserAccount(BaseTest):

    def setUp(self):
        super().setUp()
        self.account: UserAccount = UserAccount("test_username", "test_password", 50)

    def test_constructor(self):
        self.assertEqual(self.account.username, "test_username")
        self.assertEqual(self.account.password, "test_password")
        self.assertEqual(self.account.balance, 50)
