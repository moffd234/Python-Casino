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

    def test_subtract_losses(self):
        expected: float = self.account.balance - 10

        self.account.subtract_losses(10)

        self.assertEqual(self.account.balance, expected)

    def test_subtract_losses_negative(self):
        expected: str = "Wager must be positive"
        with self.assertRaises(ValueError) as ve:
            self.account.subtract_losses(-10)

        actual: str = ve.exception.args[0]
        self.assertEqual(expected, actual)

    def test_subtract_losses_negative_balance(self):
        expected: str = f"Insufficient funds! Available: {self.account.balance}, Tried to subtract: {100}"
        with self.assertRaises(ValueError) as ve:
            self.account.subtract_losses(100)

        actual: str = ve.exception.args[0]
        self.assertEqual(expected, actual)