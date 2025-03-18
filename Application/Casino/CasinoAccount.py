class CasinoAccount:
    def __init__(self, username: str, password: str, balance: float=0.00):
        self.username = username
        self.password = password
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")

        self._balance = value
