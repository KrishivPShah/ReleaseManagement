"""
Core Python Fundamentals Demo
Simple examples of: data types, variables, control flow, functions, comprehensions, exceptions
"""

# ============ DATA TYPES & VARIABLES ============
name = "Alice"  # str
age = 25  # int
balance = 1500.50  # float
is_active = True  # bool
data = b"binary"  # bytes

print(f"Name: {name}, Age: {age}, Balance: {balance}")


# ============ OPERATORS & CONTROL FLOW ============
def check_age(age):
    """Simple if/else example"""
    if age >= 18:
        return "Adult"
    else:
        return "Minor"


print(f"{name} is {check_age(age)}")

# For loop example
for i in range(1, 4):
    print(f"Loop iteration: {i}")

# While loop example
count = 0
while count < 3:
    count += 1
    print(f"Count: {count}")


# ============ FUNCTIONS: ARGS, KWARGS, DEFAULTS ============
def add(a, b=5):
    """Function with default argument"""
    return a + b


print(f"add(10) = {add(10)}")
print(f"add(10, 3) = {add(10, 3)}")


def greet(*args, **kwargs):
    """Function with *args and **kwargs"""
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")


greet("Hello", "World", name="Alice", age=25)


# ============ LAMBDA, MAP, FILTER ============
numbers = [1, 2, 3, 4, 5]

# Lambda with map
squared = list(map(lambda x: x**2, numbers))
print(f"Squared: {squared}")

# Lambda with filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")


# ============ LIST COMPREHENSIONS ============
# Simple comprehension
cubes = [x**3 for x in numbers]
print(f"Cubes: {cubes}")

# Comprehension with condition
greater_than_2 = [x for x in numbers if x > 2]
print(f"Greater than 2: {greater_than_2}")

# Nested comprehension
matrix = [[1, 2], [3, 4]]
flattened = [val for row in matrix for val in row]
print(f"Flattened: {flattened}")


# ============ EXCEPTION HANDLING ============
def safe_divide(a, b):
    """Exception handling example"""
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Invalid types for division")
        return None
    finally:
        print("Division attempt completed")


result = safe_divide(10, 2)
print(f"Result: {result}")
result = safe_divide(10, 0)
