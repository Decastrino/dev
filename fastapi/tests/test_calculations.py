import pytest
from app.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, res", [
    (2, 3, 5), (4, 5, 9), (10, 2, 12)
])
def test_add(num1, num2, res):
    print("Running test_add")
    assert add(num1, num2) == res
    
def test_subtract():
    assert subtract(12,3) == 9
    
def test_multiply():
    assert multiply(2,3) == 6
    
def test_divide():
    assert divide(10,2) == 5
    
if __name__ == "__main__":
    # test_add()
    test_subtract()
    test_multiply()
    test_divide()
    