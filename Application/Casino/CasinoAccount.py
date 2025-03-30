import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class CasinoAccount:
    def __init__(self, username: str, password: str, balance: float=0.00):
        self.username = username
        self.password = password
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")

        self._balance = value

    def add_winnings(self, wager: float) -> float:
        if wager <= 0:
            raise ValueError("Wager must be positive")

        self._balance += wager
        logging.debug(f"{self.username} added {wager} to balance. New balance: {self._balance}")
        return self._balance

    def subtract_losses(self, wager) -> float:
        if wager <= 0:
            raise ValueError("Wager must be positive")
        if wager > self._balance:
            raise ValueError(f"Insufficient funds! Available: {self._balance}, Tried to subtract: {wager}")

        self._balance -= wager
        logging.debug(f"{self.username} subtracted {wager} to balance. New balance: {self._balance}")
        return self._balance