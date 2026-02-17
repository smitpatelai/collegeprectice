

INITIAL_BALANCE = 1000000000000000
PIN = 3655
MAX_ATTEMPTS = 3

transactions = []

def authenticate_pin():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        user_pin = int(input("Enter your ATM PIN: "))
        if user_pin == PIN:
            print("Login Successful ^")
            return True
        else:
            attempts += 1
            print(f"Incorrect PIN! Attempts left: {MAX_ATTEMPTS - attempts}")

    print("Card Blocked!!!")
    return False
def show_menu():
    print("\n====== MINI ATM MENU ======")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Mini Statement")
    print("5. Exit")

def check_balance(balance):
    print(f"Available Balance: ₹{balance}")


def deposit(balance):
    amount = float(input("Enter deposit amount: "))

    if amount <= 0:
        print("Invalid amount. Deposit must be greater than 0.")
    else:
        balance += amount
        transactions.append(f"Deposited: {amount}")

        if len(transactions) > 5:
            transactions.pop(0)

        print("Deposit Successful!")
        print("Updated Balance: ₹", balance)

    return balance


def withdraw(balance):
    amount = float(input("Enter withdrawal amount: "))

    if amount <= 0:
        print("Invalid amount. Withdrawal must be greater than 0.")
    elif amount > balance:
        print("Insufficient Balance.")
    elif balance - amount < 500:
        print("Minimum balance of ₹500 must be maintained.")
    else:
        balance -= amount
        transactions.append(f"Withdrawn: ₹{amount}")

        # Keep only last 5 transactions
        if len(transactions) > 5:
            transactions.pop(0)

        print("Withdrawal Successful!")
        print("Updated Balance: ₹", balance)

    return balance

def mini_statement(transactions):
    print("\n----- Last 5 Transactions -----")
    if not transactions:
        print("No transactions yet.")
    else:
        for t in transactions:
            print(t)


def main():
    balance = INITIAL_BALANCE

    if authenticate_pin():
        while True:
            show_menu()
            choice = input("Select option (1-5): ")

            if choice == "1":
                check_balance(balance)
            elif choice == "2":
                balance = deposit(balance)
            elif choice == "3":
                balance = withdraw(balance)
            elif choice == "4":
                mini_statement(transactions)
            elif choice == "5":
                print("Thank You For Using Patel ATM.")
                break
            else:
                print("Invalid choice. Please select 1-5.")


main()