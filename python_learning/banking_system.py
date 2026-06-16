"""
Banking Management System - Mini Project
Simple OOP implementation with JSON persistence
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque


class Customer:
    """Represents a bank customer"""
    def __init__(self, customer_id: str, name: str, email: str) -> None:
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"Customer({self.customer_id}, {self.name})"

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }


class Transaction:
    """Represents a single transaction"""
    def __init__(self, tx_id: str, amount: float, tx_type: str, timestamp: str) -> None:
        self.tx_id = tx_id
        self.amount = amount
        self.tx_type = tx_type  # "deposit" or "withdrawal"
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"TX({self.tx_id}, {self.tx_type}, ${self.amount})"

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            "tx_id": self.tx_id,
            "amount": self.amount,
            "type": self.tx_type,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Transaction":
        """Deserialize from dictionary"""
        return Transaction(data["tx_id"], data["amount"], data["type"], data["timestamp"])


class Account:
    """Base account class"""
    def __init__(self, account_id: str, customer: Customer, account_type: str, initial_balance: float = 0.0) -> None:
        self.account_id = account_id
        self.customer = customer
        self.account_type = account_type
        self._balance = initial_balance
        self.transactions: deque = deque(maxlen=100)

    @property
    def balance(self) -> float:
        """Get current balance"""
        return self._balance

    def deposit(self, amount: float) -> bool:
        """Deposit money"""
        if amount <= 0:
            return False
        self._balance += amount
        tx = Transaction(f"TX{len(self.transactions)+1}", amount, "deposit", datetime.now().isoformat())
        self.transactions.append(tx)
        return True

    def withdraw(self, amount: float) -> bool:
        """Withdraw money"""
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        tx = Transaction(f"TX{len(self.transactions)+1}", amount, "withdrawal", datetime.now().isoformat())
        self.transactions.append(tx)
        return True

    def get_recent_transactions(self, limit: int = 5) -> List[Transaction]:
        """Get recent transactions"""
        return list(self.transactions)[-limit:]

    def to_dict(self) -> Dict:
        """Serialize account"""
        return {
            "account_id": self.account_id,
            "customer_id": self.customer.customer_id,
            "account_type": self.account_type,
            "balance": self._balance,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }


class SavingsAccount(Account):
    """Savings account with interest"""
    def __init__(self, account_id: str, customer: Customer, initial_balance: float = 0.0, interest_rate: float = 0.02) -> None:
        super().__init__(account_id, customer, "savings", initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        """Apply monthly interest"""
        interest = self._balance * self.interest_rate / 12
        self.deposit(interest)

    def to_dict(self) -> Dict:
        """Serialize with interest rate"""
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data


class CheckingAccount(Account):
    """Checking account with fees"""
    def __init__(self, account_id: str, customer: Customer, initial_balance: float = 0.0, monthly_fee: float = 10.0) -> None:
        super().__init__(account_id, customer, "checking", initial_balance)
        self.monthly_fee = monthly_fee

    def deduct_monthly_fee(self) -> None:
        """Deduct monthly fee"""
        if self._balance >= self.monthly_fee:
            self._balance -= self.monthly_fee
            tx = Transaction(f"TX{len(self.transactions)+1}", self.monthly_fee, "fee", datetime.now().isoformat())
            self.transactions.append(tx)

    def to_dict(self) -> Dict:
        """Serialize with fee"""
        data = super().to_dict()
        data["monthly_fee"] = self.monthly_fee
        return data


class Bank:
    """Main bank system"""
    def __init__(self) -> None:
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}

    def add_customer(self, customer_id: str, name: str, email: str) -> Customer:
        """Add a new customer"""
        customer = Customer(customer_id, name, email)
        self.customers[customer_id] = customer
        return customer

    def create_account(self, account_id: str, customer_id: str, account_type: str, initial_balance: float = 0.0) -> Optional[Account]:
        """Create a new account"""
        if customer_id not in self.customers:
            return None
        customer = self.customers[customer_id]

        if account_type == "savings":
            account = SavingsAccount(account_id, customer, initial_balance)
        elif account_type == "checking":
            account = CheckingAccount(account_id, customer, initial_balance)
        else:
            account = Account(account_id, customer, account_type, initial_balance)

        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        return self.accounts.get(account_id)

    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        """Transfer between accounts"""
        from_acc = self.accounts.get(from_account_id)
        to_acc = self.accounts.get(to_account_id)

        if not from_acc or not to_acc:
            return False

        if from_acc.withdraw(amount):
            to_acc.deposit(amount)
            return True
        return False

    def save_to_json(self, filename: str) -> None:
        """Save bank state to JSON"""
        data = {
            "customers": {cid: c.to_dict() for cid, c in self.customers.items()},
            "accounts": {aid: a.to_dict() for aid, a in self.accounts.items()},
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, filename: str) -> None:
        """Load bank state from JSON"""
        with open(filename, "r") as f:
            data = json.load(f)

        for cid, c_data in data.get("customers", {}).items():
            self.add_customer(c_data["customer_id"], c_data["name"], c_data["email"])

        for aid, a_data in data.get("accounts", {}).items():
            account_type = a_data["account_type"]
            self.create_account(
                a_data["account_id"],
                a_data["customer_id"],
                account_type,
                a_data["balance"],
            )


# Simple demo
if __name__ == "__main__":
    bank = Bank()

    # Create customers
    customer1 = bank.add_customer("C001", "Alice", "alice@email.com")
    customer2 = bank.add_customer("C002", "Bob", "bob@email.com")

    # Create accounts
    savings = bank.create_account("SA001", "C001", "savings", 1000)
    checking = bank.create_account("CA001", "C001", "checking", 500)
    bob_account = bank.create_account("CA002", "C002", "checking", 2000)

    # Perform transactions
    savings.deposit(300)
    savings.withdraw(100)
    checking.deduct_monthly_fee()

    # Transfer
    bank.transfer("CA002", "SA001", 500)

    # Save to JSON
    print(f"Savings account balance: ${savings.balance}")
    print(f"Bob's account balance: ${bob_account.balance}")
    print(f"Recent transactions (Savings): {savings.get_recent_transactions(3)}")

    bank.save_to_json("bank_data.json")
    print("\nBank data saved to bank_data.json")
