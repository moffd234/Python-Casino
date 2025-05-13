import datetime
import uuid
from unittest.mock import MagicMock, patch

from Tests.BaseTest import BaseTest, TEST_QUESTIONS
from Application.Casino.Accounts.UserAccount import UserAccount


class TestAccountManager(BaseTest):

    def setUp(self):
        super().setUp()

    def test_create_account(self):
        subject = self.manager.create_account("username", "password", "test@email.com", TEST_QUESTIONS)

        expected_username = "username"
        expected_password = "password"
        expected_balance = 50.0

        actual_username = subject.username
        actual_password = subject.password
        actual_balance = subject.balance

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_password, actual_password)
        self.assertEqual(expected_balance, actual_balance)

    def test_create_account_username_exist(self):
        self.manager.create_account("test_username", "test_password", "test@email.com", TEST_QUESTIONS)
        subject = self.manager.create_account("test_username", "test_password", "test@email.com", TEST_QUESTIONS)

        self.assertIsNone(subject)

    def test_get_account(self):
        self.manager.create_account("test_username", "test_password",
                                    "test@email.com", TEST_QUESTIONS)
        expected = UserAccount("test_username", "test_password", 50.0,
                               "test@email.com", TEST_QUESTIONS)
        actual = self.manager.get_account("test_username", "test_password")

        self.assertEqual(expected.username, actual.username)
        self.assertEqual(expected.password, actual.password)
        self.assertEqual(expected.balance, actual.balance)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.security_question_one, expected.security_question_one)
        self.assertEqual(expected.security_question_two, expected.security_question_two)
        self.assertEqual(expected.security_answer_one, expected.security_answer_one)
        self.assertEqual(expected.security_answer_two, expected.security_answer_two)

    def test_get_account_none(self):
        actual: UserAccount = self.manager.get_account("this_name_won't_be_used", "secure123")

        self.assertIsNone(actual)

    def test_add_winnings_and_save(self):
        account: UserAccount = self.manager.create_account("test_username", "test_password",
                                                           "test@email.com", TEST_QUESTIONS)
        self.manager.session.commit = MagicMock()
        self.manager.add_and_save_account(account, 50.0)

        expected: float = 100
        actual: float = account.balance

        self.assertEqual(expected, actual)
        self.manager.session.commit.assert_called_once()

    def test_subtract_and_save(self):
        account: UserAccount = self.manager.create_account("test_username", "test_password",
                                                           "test@email.com", TEST_QUESTIONS)
        self.manager.session.commit = MagicMock()
        self.manager.subtract_and_save_account(account, 50.0)

        expected: float = 0
        actual: float = account.balance

        self.assertEqual(expected, actual)
        self.manager.session.commit.assert_called_once()

    @patch("sqlalchemy.orm.Session.commit")
    def test_generate_uuid(self, mock_commit):
        current_time: datetime = datetime.datetime.now(datetime.UTC)
        min_time: datetime = current_time + datetime.timedelta(minutes=14, seconds=59)
        max_time: datetime = current_time + datetime.timedelta(minutes=15, seconds=1)

        expected_token: uuid.UUID = uuid.UUID(self.manager.generate_uuid_and_store_it(self.account))
        actual_token: uuid.UUID = self.account.reset_token
        actual_expiration = self.account.reset_token_expiration

        is_time_valid: bool = min_time < actual_expiration < max_time

        mock_commit.assert_called_once()
        self.assertEqual(expected_token, actual_token)
        self.assertTrue(is_time_valid)
