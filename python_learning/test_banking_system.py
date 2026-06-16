"""
Test suite for Banking Management System
Using pytest, fixtures, parametrization, mocking
"""

import pytest
import json
import os
from banking_system import Bank, Customer, Account, SavingsAccount, CheckingAccount, Transaction


@pytest.fixture
def bank():
    """Fixture providing a fresh bank instance"""
    return Bank()


@pytest.fixture
def customer(bank):
    """Fixture providing a customer"""
    return bank.add_customer("C001", "Alice", "alice@email.com")


@pytest.fixture
def savings_account(bank, customer):
    """Fixture providing a savings account"""
    return bank.create_account("SA001", customer.customer_id, "savings", 1000)


@pytest.fixture
def checking_account(bank, customer):
    """Fixture providing a checking account"""
    return bank.create_account("CA001", customer.customer_id, "checking", 500)


class TestCustomer:
    """Test Customer class"""

    def test_customer_creation(self, customer):
        """Test customer object creation"""
        assert customer.customer_id == "C001"
        assert customer.name == "Alice"
        assert customer.email == "alice@email.com"

    def test_customer_to_dict(self, customer):
        """Test customer serialization"""
        data = customer.to_dict()
        assert data["customer_id"] == "C001"
        assert data["name"] == "Alice"


class TestTransaction:
    """Test Transaction class"""

    def test_transaction_creation(self):
        """Test transaction object creation"""
        tx = Transaction("TX001", 100, "deposit", "2024-01-01T10:00:00")
        assert tx.tx_id == "TX001"
        assert tx.amount == 100
        assert tx.tx_type == "deposit"

    def test_transaction_serialization(self):
        """Test transaction to_dict"""
        tx = Transaction("TX001", 100, "deposit", "2024-01-01T10:00:00")
        data = tx.to_dict()
        assert data["tx_id"] == "TX001"
        assert data["amount"] == 100

    def test_transaction_deserialization(self):
        """Test transaction from_dict"""
        data = {"tx_id": "TX001", "amount": 100, "type": "deposit", "timestamp": "2024-01-01"}
        tx = Transaction.from_dict(data)
        assert tx.tx_id == "TX001"
        assert tx.amount == 100


class TestAccount:
    """Test Account class"""

    def test_account_creation(self, savings_account):
        """Test account creation"""
        assert savings_account.balance == 1000
        assert savings_account.account_type == "savings"

    def test_deposit(self, savings_account):
        """Test deposit functionality"""
        assert savings_account.deposit(200) is True
        assert savings_account.balance == 1200

    def test_deposit_invalid(self, savings_account):
        """Test invalid deposits"""
        assert savings_account.deposit(0) is False
        assert savings_account.deposit(-100) is False
        assert savings_account.balance == 1000

    def test_withdraw(self, savings_account):
        """Test withdrawal"""
        assert savings_account.withdraw(300) is True
        assert savings_account.balance == 700

    def test_withdraw_insufficient_funds(self, savings_account):
        """Test withdrawal with insufficient funds"""
        assert savings_account.withdraw(2000) is False
        assert savings_account.balance == 1000

    @pytest.mark.parametrize("amount,expected", [(100, 900), (500, 500), (1000, 0)])
    def test_withdraw_parametrized(self, savings_account, amount, expected):
        """Test multiple withdrawal amounts"""
        savings_account.withdraw(amount)
        assert savings_account.balance == expected

    def test_recent_transactions(self, savings_account):
        """Test getting recent transactions"""
        savings_account.deposit(100)
        savings_account.withdraw(50)
        savings_account.deposit(200)

        recent = savings_account.get_recent_transactions(2)
        assert len(recent) == 2
        assert recent[0].tx_type == "withdrawal"
        assert recent[1].tx_type == "deposit"


class TestSavingsAccount:
    """Test SavingsAccount class"""

    def test_savings_account_creation(self, bank, customer):
        """Test savings account with interest"""
        account = bank.create_account("SA002", customer.customer_id, "savings", 1000)
        assert account.interest_rate == 0.02

    def test_apply_interest(self, bank, customer):
        """Test interest application"""
        account = SavingsAccount("SA003", customer, 1000, 0.02)
        initial_balance = account.balance
        account.apply_interest()
        assert account.balance > initial_balance


class TestCheckingAccount:
    """Test CheckingAccount class"""

    def test_checking_account_creation(self, bank, customer):
        """Test checking account with fee"""
        account = bank.create_account("CA003", customer.customer_id, "checking", 500)
        assert account.monthly_fee == 10.0

    def test_deduct_monthly_fee(self, checking_account):
        """Test monthly fee deduction"""
        initial_balance = checking_account.balance
        checking_account.deduct_monthly_fee()
        assert checking_account.balance == initial_balance - 10


class TestBank:
    """Test Bank class"""

    def test_bank_creation(self, bank):
        """Test bank initialization"""
        assert len(bank.customers) == 0
        assert len(bank.accounts) == 0

    def test_add_customer(self, bank):
        """Test adding a customer"""
        customer = bank.add_customer("C002", "Bob", "bob@email.com")
        assert "C002" in bank.customers
        assert customer.name == "Bob"

    def test_create_account(self, bank, customer):
        """Test account creation"""
        account = bank.create_account("SA001", customer.customer_id, "savings", 1000)
        assert "SA001" in bank.accounts
        assert account.balance == 1000

    def test_create_account_invalid_customer(self, bank):
        """Test account creation with invalid customer"""
        account = bank.create_account("SA001", "INVALID", "savings", 1000)
        assert account is None

    def test_get_account(self, bank, savings_account):
        """Test retrieving an account"""
        retrieved = bank.get_account("SA001")
        assert retrieved == savings_account

    def test_transfer(self, bank, customer):
        """Test transfer between accounts"""
        from_acc = bank.create_account("SA001", customer.customer_id, "savings", 1000)
        to_acc = bank.create_account("CA001", customer.customer_id, "checking", 500)

        assert bank.transfer("SA001", "CA001", 200) is True
        assert from_acc.balance == 800
        assert to_acc.balance == 700

    def test_transfer_insufficient_funds(self, bank, customer):
        """Test transfer with insufficient funds"""
        from_acc = bank.create_account("SA001", customer.customer_id, "savings", 100)
        to_acc = bank.create_account("CA001", customer.customer_id, "checking", 500)

        assert bank.transfer("SA001", "CA001", 200) is False
        assert from_acc.balance == 100

    def test_transfer_invalid_account(self, bank, customer):
        """Test transfer with invalid account"""
        acc = bank.create_account("SA001", customer.customer_id, "savings", 1000)
        assert bank.transfer("SA001", "INVALID", 100) is False

    def test_save_load_json(self, bank, customer):
        """Test JSON persistence"""
        account = bank.create_account("SA001", customer.customer_id, "savings", 1000)
        account.deposit(200)

        # Save
        bank.save_to_json("test_bank.json")
        assert os.path.exists("test_bank.json")

        # Load in new bank
        new_bank = Bank()
        new_bank.load_from_json("test_bank.json")

        assert "C001" in new_bank.customers
        assert "SA001" in new_bank.accounts
        loaded_account = new_bank.get_account("SA001")
        assert loaded_account.balance == 1200

        # Cleanup
        os.remove("test_bank.json")
