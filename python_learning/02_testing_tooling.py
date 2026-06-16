"""
Testing & Tooling Patterns Demo
Pytest fixtures, parametrization, type hints, mocking
"""

from typing import List
import pytest
from unittest.mock import Mock, patch


# ============ TYPE HINTS ============
def add_numbers(a: int, b: int) -> int:
    """Function with type hints"""
    return a + b


def process_list(items: List[str]) -> List[str]:
    """Type hints with generics"""
    return [item.upper() for item in items]


print(f"add_numbers(5, 3) = {add_numbers(5, 3)}")
print(f"process_list(['a', 'b']) = {process_list(['a', 'b'])}")


# ============ PYTEST FIXTURES ============
class TestFixtures:
    """Examples of pytest fixtures"""

    @pytest.fixture
    def sample_list(self):
        """Fixture providing test data"""
        return [1, 2, 3, 4, 5]

    @pytest.fixture
    def database_mock(self):
        """Fixture providing a mock"""
        return Mock()

    def test_with_fixture(self, sample_list):
        """Test using fixture"""
        assert sum(sample_list) == 15
        assert len(sample_list) == 5


# ============ PARAMETRIZATION ============
class TestParametrization:
    """Examples of parametrized tests"""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 5, 5),
        (-1, 1, 0),
        (10, -5, 5),
    ])
    def test_add_multiple_cases(self, a, b, expected):
        """Parametrized test with multiple inputs"""
        assert add_numbers(a, b) == expected


# ============ MOCKING EXAMPLE ============
class DataService:
    """Service that depends on external API"""
    def __init__(self, api_client):
        self.api_client = api_client

    def get_user_age(self, user_id: int) -> int:
        """Get age from external API"""
        response = self.api_client.fetch_user(user_id)
        return response["age"]


class TestMocking:
    """Examples of mocking"""

    def test_data_service_with_mock(self):
        """Test using mocked dependency"""
        mock_api = Mock()
        mock_api.fetch_user.return_value = {"age": 30}

        service = DataService(mock_api)
        age = service.get_user_age(123)

        assert age == 30
        mock_api.fetch_user.assert_called_once_with(123)

    @patch("builtins.open")
    def test_file_operation(self, mock_open):
        """Test file operations with patch"""
        mock_open.return_value.read.return_value = "file content"

        with open("test.txt") as f:
            content = f.read()

        assert content == "file content"
        mock_open.assert_called_once_with("test.txt")


# ============ EXCEPTION TESTING ============
class TestExceptions:
    """Examples of testing exceptions"""

    def test_value_error(self):
        """Test that exception is raised"""
        with pytest.raises(ValueError):
            int("not a number")

    def test_assertion_error(self):
        """Test assertion failures"""
        with pytest.raises(AssertionError):
            assert False, "This should fail"


if __name__ == "__main__":
    print("\nRun with: pytest 02_testing_tooling.py -v")
