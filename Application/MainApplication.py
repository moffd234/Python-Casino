from Application.Casino.Casino import Casino
from Application.Casino.Accounts.db import init_db

if __name__ == '__main__':
    init_db()
    casino = Casino()
    casino.run()