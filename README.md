
# no Arguments
python run_csv.py --file products.csv

# filter int Arguments
python run_csv.py --file products.csv --where "price=199"

# filter float Arguments
python run_csv.py --file products.csv --where "rating<4.4"

# filter string Arguments
python run_csv.py --file products.csv --where "brand>poco"

# filter and aggregate
python run_csv.py --file products.csv --where "brand=xiaomi" --aggregate "rating=avg"

# filter and sorting
python run_csv.py --file products.csv --where "rating>4.4" --order-by "rating=asc"