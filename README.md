# Python CLI Casino
Welcome to the Python CLI Casino, a Python application that allows you to play in a virtual casino. Users can create accounts, manage funds, and enjoy a variety of games from their command line.

## Tech used:
-  **Python** - Core language
-  **SQLite** - Lightweight database for storing account info
-  **unittest** - Python testing framework for unit testing
-  **CSV** - Used to read/write account data for lightweight persistence
-  **Custom Console Wrapper** - For stylized colored input/output in the terminal
-  **GitHub Actions** - Automates testing and workflows for CI/CD
-  **GitHub Projects (Kanban)** - Organizes tasks and development roadmap using a Kanban board

## Features

### Games  
**Available Games**
-  Number Guess — Guess the number and win!
-  Trivia Game — Test your general knowledge.
-  Tic-Tac-Toe — Classic 3x3 strategy showdown.
-  Coin Flip — Choose heads or tails, test your luck!
-  Rock-Paper-Scissors
-  Slot Machine
-  Blackjack *(coming soon!)*

### Account Management
- Create, login, and delete accounts  
- Check balances  
- Add funds  
- Reset password  

## Optimizations

One performance improvement made was caching the available quiz categories locally after each successful API request. 
Initially, the game fetched the list of categories from the API every time a user started a new quiz, 
which added unnecessary latency and repeated network calls. 
By storing the categories in a csv and reusing them for subsequent games played within the next few minutes, 
I eliminated redundant API requests. Allowing for reduced game time, and improved user experience while still ensuring they can get new questions if ones are added.

## Lessons Learned:

This project allowed me to explore many new technologies and aspects of programming. Before this project I had struggled with the 
concept of mocking in unit test; however, when testing the console wrapper and other methods I finally understood the concept and some of the
reasons why it is needed. Another major lesson learned was managing a user account from handling the password to managing
the database of UserAccounts. 

## Installation

```bash
# Clone the repository
git clone https://github.com/moffd234/Python-Casino.git
cd Python-Casino

# Set up a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
