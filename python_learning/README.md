# Python Learning Portfolio
## Project Structure

This is a demonstration of Python fundamentals, testing, and OOP concepts.

### Files:
- **01_core_fundamentals.py** - Data types, control flow, functions, comprehensions, exceptions
- **02_testing_tooling.py** - Pytest patterns, type hints, mocking examples
- **03_oop_advanced.py** - Classes, inheritance, magic methods, generators, context managers, data structures
- **banking_system.py** - Mini-project: Banking system with OOP (no CLI, JSON persistence)
- **test_banking_system.py** - 20+ tests with pytest fixtures, parametrization

### Setup:
```bash
pip install -r requirements.txt
```

### Run:
```bash
# Run demo scripts
python 01_core_fundamentals.py
python 02_testing_tooling.py
python 03_oop_advanced.py
python banking_system.py

# Run tests
pytest test_banking_system.py -v
pytest test_banking_system.py --cov

# Code quality
black *.py
flake8 *.py
mypy *.py
isort *.py
```

### What's Covered:
✅ Data types, variables, operators, control flow  
✅ Functions (args, kwargs, defaults)  
✅ Lambda, map, filter, comprehensions  
✅ Exception handling  
✅ Classes, inheritance, encapsulation  
✅ Magic methods (__str__, __repr__, __eq__)  
✅ Properties and decorators  
✅ Generators and iterators  
✅ Context managers  
✅ Data structures (deque, defaultdict)  
✅ pytest fixtures and parametrization  
✅ Type hints and mypy  
✅ JSON serialization/deserialization  
✅ Code quality tools (black, flake8, isort)  

### Test Coverage:
Run `pytest --cov` to see test coverage (target >80%)
