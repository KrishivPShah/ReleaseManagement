"""
OOP & Advanced Data Structures Demo
Classes, inheritance, magic methods, generators, context managers
"""

from typing import Iterator, List
from collections import deque, defaultdict


# ============ CLASSES & BASIC OOP ============
class Person:
    """Basic class with __init__ and self"""
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        """String representation for users"""
        return f"Person({self.name}, {self.age})"

    def __repr__(self) -> str:
        """Official representation for developers"""
        return f"Person(name='{self.name}', age={self.age})"

    def __eq__(self, other: object) -> bool:
        """Check equality"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name and self.age == other.age

    def __lt__(self, other: "Person") -> bool:
        """Less than comparison"""
        return self.age < other.age


person1 = Person("Alice", 25)
person2 = Person("Bob", 30)
person3 = Person("Alice", 25)

print(str(person1))  # Uses __str__
print(repr(person1))  # Uses __repr__
print(f"person1 == person3: {person1 == person3}")  # True
print(f"person1 < person2: {person1 < person2}")  # True


# ============ INHERITANCE ============
class Employee(Person):
    """Child class inheriting from Person"""
    def __init__(self, name: str, age: int, employee_id: int, salary: float) -> None:
        super().__init__(name, age)
        self.employee_id = employee_id
        self.salary = salary

    def __str__(self) -> str:
        return f"Employee({self.name}, {self.employee_id}, ${self.salary})"

    def give_raise(self, amount: float) -> None:
        """Increase salary"""
        self.salary += amount


emp = Employee("Charlie", 35, 101, 50000)
print(str(emp))
emp.give_raise(5000)
print(f"New salary: {emp.salary}")


# ============ ENCAPSULATION & PROPERTIES ============
class BankAccount:
    """Encapsulation example with property decorators"""
    def __init__(self, account_number: str, initial_balance: float) -> None:
        self._account_number = account_number
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        """Read-only property to access balance"""
        return self._balance

    @balance.setter
    def balance(self, amount: float) -> None:
        """Setter with validation"""
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    def deposit(self, amount: float) -> None:
        """Safe deposit method"""
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> bool:
        """Safe withdrawal method"""
        if amount > self._balance:
            print("Insufficient funds")
            return False
        self._balance -= amount
        return True


account = BankAccount("123456", 1000)
print(f"Initial balance: {account.balance}")
account.deposit(500)
print(f"After deposit: {account.balance}")
account.withdraw(200)
print(f"After withdrawal: {account.balance}")


# ============ ITERATORS & GENERATORS ============
class TransactionHistory:
    """Generator example for iterating through transactions"""
    def __init__(self) -> None:
        self.transactions: List[dict] = []

    def add_transaction(self, amount: float, tx_type: str) -> None:
        """Add a transaction"""
        self.transactions.append({"amount": amount, "type": tx_type})

    def __iter__(self) -> "TransactionHistory":
        """Iterator protocol"""
        self.index = 0
        return self

    def __next__(self) -> dict:
        """Get next transaction"""
        if self.index >= len(self.transactions):
            raise StopIteration
        tx = self.transactions[self.index]
        self.index += 1
        return tx

    def recent_transactions(self, count: int) -> Iterator[dict]:
        """Generator to yield recent transactions"""
        for tx in self.transactions[-count:]:
            yield tx


history = TransactionHistory()
history.add_transaction(100, "deposit")
history.add_transaction(50, "withdrawal")
history.add_transaction(200, "deposit")

print("\nAll transactions (using iterator):")
for tx in history:
    print(f"  {tx['type']}: ${tx['amount']}")

print("\nLast 2 transactions (using generator):")
for tx in history.recent_transactions(2):
    print(f"  {tx['type']}: ${tx['amount']}")


# ============ CONTEXT MANAGERS ============
class Transaction:
    """Context manager for safe transactions"""
    def __init__(self, account: BankAccount, amount: float) -> None:
        self.account = account
        self.amount = amount
        self.success = False

    def __enter__(self) -> "Transaction":
        """Enter context"""
        print(f"Starting transaction of ${self.amount}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context"""
        if exc_type is not None:
            print(f"Transaction failed: {exc_val}")
            return False
        if self.success:
            print(f"Transaction completed successfully")
        return True

    def execute(self) -> None:
        """Execute the transaction"""
        if self.account.withdraw(self.amount):
            self.success = True


print("\nContext manager example:")
with Transaction(account, 100) as tx:
    tx.execute()


# ============ ADVANCED DATA STRUCTURES ============
# Deque for transaction history (FIFO)
print("\nDeque example (transaction queue):")
tx_queue = deque(maxlen=3)  # Keep only 3 recent transactions
tx_queue.append("TX1: +$100")
tx_queue.append("TX2: -$50")
tx_queue.append("TX3: +$200")
tx_queue.append("TX4: -$75")  # This removes TX1
print(list(tx_queue))

# DefaultDict for grouping transactions by type
print("\nDefaultDict example (group by type):")
transactions_by_type = defaultdict(list)
transactions_by_type["deposit"].append(100)
transactions_by_type["deposit"].append(200)
transactions_by_type["withdrawal"].append(50)
print(dict(transactions_by_type))
