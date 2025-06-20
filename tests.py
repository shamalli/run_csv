import pytest
from run_csv import read_csv, filter_data, aggregate_data, sort_data, parse_input_args

@pytest.fixture(scope="module")
def data():
    return read_csv("products.csv")

def test_read_data(data):
    assert len(data) == 10

class InputArgs:
    def __init__(self, where, aggregate, order_by):
        self.where = where
        self.aggregate = aggregate
        self.order_by = order_by

args1 = InputArgs("brand=xiaomi", "rating=avg", False)
args2 = InputArgs("price>199", "rating=max", False)
args3 = InputArgs("price<199", "rating=min", False)
args4 = InputArgs("price>199", False, "rating=desc")

@pytest.mark.parametrize("args, expected_out", [
    (args1, ["brand", "=", "xiaomi", "rating", "avg", False, False]),
    (args2, ["price", ">", "199", "rating", "max", False, False]),
    (args3, ["price", "<", "199", "rating", "min", False, False]),
    (args4, ["price", ">", "199", False, False, "rating", "desc"]),
])
def test_parse_input_args(args, expected_out):
    assert parse_input_args(args) == expected_out

@pytest.mark.parametrize("column, operation, value, expected_count", [
    ("brand", "=", "apple", 4),
    ("price", ">", "199", 8),
    ("rating", ">", "4.4", 6),
])
def test_filter_data(data, column, operation, value, expected_count):
    assert len(filter_data(data, column, operation, value)) == expected_count

def test_aggregate_data_avg(data):
    result = aggregate_data(data, "rating", "avg")
    expected = (4.9 + 4.8 + 4.6 + 4.7 + 4.2 + 4.4 + 4.1 + 4.6 + 4.1 + 4.5) / 10
    assert result == pytest.approx(expected)

def test_aggregate_data_max(data):
    result = aggregate_data(data, "price", "max")
    assert result == 1199

def test_aggregate_data_min(data):
    result = aggregate_data(data, "price", "min")
    assert result == 149

def test_sort_data(data):
    column = "rating"
    dest = "asc"

    sorted_data = sort_data(data, column, dest)

    def compare_vals(x, nx):
        if dest == "asc":
            return x <= nx
        elif dest == "desc":
            return x >= nx

    assert all(compare_vals(sorted_data[i][column], sorted_data[i+1][column]) for i in range(len(sorted_data) - 1))