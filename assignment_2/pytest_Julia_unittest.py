import pytest
from JuliaSet import calc_pure_python

@pytest.fixture(scope='session')
def get_julia_test_data():
        test_data = [
        (100, 100, 131532), (500, 100, 3278808), (1000, 100, 13113340),
        (100, 200, 233136), (500, 200, 5798200), (1000, 200, 23186920),
        (100, 300, 334236), (500, 300, 8306884), (1000, 300, 33219980)
                 ]
        return test_data
@pytest.fixture(autouse=True)
def setup_and_teardown():
        print('\nFetching data from db')    
        yield
        print('\nSaving test run data in db')
def test_julia(get_julia_test_data):
        for data in get_julia_test_data:
                result, _ = calc_pure_python(desired_width=data[0], max_iterations=data[1])
                expected = data[2]
                assert result[0] == expected