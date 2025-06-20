import argparse
import csv
from tabulate import tabulate

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_data(data, column, operation, value):
    def compare_vals_in_row(row):
        row_value = row[column]
        
        # from str to numbers
        if row_value.replace('.', '', 1).isdigit():
            row_value = float(row_value)
            value_compare = float(value)
        else:
            value_compare = value

        if operation == '=':
            return row_value == value_compare
        elif operation == '>':
            return row_value > value_compare
        elif operation == '<':
            return row_value < value_compare
        else:
            raise ValueError(f"Unsupported filter operator: {operation}")

    return [row for row in data if compare_vals_in_row(row)]

def aggregate_data(data, column, operation):
    values = [float(row[column]) for row in data]
    
    if operation == 'avg':
        return sum(values) / len(values)
    elif operation == 'min':
        return min(values)
    elif operation == 'max':
        return max(values)
    else:
        raise ValueError(f"Unsupported aggregation: {operation}")
    
def sort_data(data, sorting_column, dest = 'desc'):
    if dest == 'desc':
        rev = True
    elif dest == 'asc':
        rev = False
    else:
        raise ValueError(f"Unsupported destination: {dest}")
    
    return sorted(data, key=lambda d: d[sorting_column], reverse=rev)

def parse_input_args(args):
    filter_column = filter_operation = filter_value = False
    if args.where:
        operations = ['=', '>', '<']

        for op in operations:
            if op in args.where:
                where = args.where.split(op)
                if len(where) == 2:
                    filter_operation = op
                    filter_column = where[0]
                    filter_value = where[1]
                    break
    
    aggregate_column = aggregate_func = False
    if args.aggregate:
        aggregate = args.aggregate.split('=')
        if len(aggregate) == 2:
            aggregate_column = aggregate[0]
            aggregate_func = aggregate[1]

    sorting_column = sorting_dest = False
    if args.order_by:
        sorting = args.order_by.split('=')
        if len(sorting) == 2:
            sorting_column = sorting[0]
            sorting_dest = sorting[1]
    
    return [
        filter_column,
        filter_operation,
        filter_value,
        aggregate_column,
        aggregate_func,
        sorting_column,
        sorting_dest
    ]

def main():
    parser = argparse.ArgumentParser(description='CSV filter and aggregator tool')
    parser.add_argument('--file', help='Path to CSV file')
    
    # Filtering
    parser.add_argument('--where', help='Filtering')

    # Aggregation
    parser.add_argument('--aggregate', help='Aggregation')

    # Sorting
    parser.add_argument('--order-by', help='Order By')

    args = parser.parse_args()

    data = read_csv(args.file)

    filter_column, filter_operation, filter_value, aggregate_column, aggregate_func, sorting_column, sorting_dest = parse_input_args(args);

    if filter_column and filter_operation and filter_value:
        data = filter_data(data, filter_column, filter_operation, filter_value)

    if sorting_column and sorting_dest:
        data = sort_data(data, sorting_column, sorting_dest);

    if aggregate_column and aggregate_func:
        result = aggregate_data(data, aggregate_column, aggregate_func)
        f_result = "{:.2f}".format(result)
        print(tabulate([{aggregate_func: f_result}], headers='keys', tablefmt='grid'))
    else:
        print(tabulate(data, headers='keys', tablefmt='grid'))

if __name__ == '__main__':
    main()