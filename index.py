import random
import datetime
import string

def generate_realistic_data():
    open_price = random.uniform(50, 150)
    high_price = random.uniform(open_price, open_price * 1.1)  # High is always >= open
    low_price = random.uniform(open_price * 0.9, open_price)  # Low is always <= open
    close_price = random.uniform(low_price, high_price)  # Close is between low and high
    volume = random.uniform(10000, 1000000)  # Realistic volume
    return [open_price, high_price, low_price, close_price, volume]

def generate_sequential_dates(start_date, end_date, num_dates):
    delta = (end_date - start_date) // num_dates
    return [start_date + i * delta for i in range(num_dates)]

def generate_random_ticker():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        # Write the header
        f.write('ticker,date,open,high,low,close,volume\n')
        for row in data:
            f.write(','.join(str(value) for value in row) + '\n')

# Example usage
num_companies = 5
num_dates_per_company = 365 * 10  # 10 years worth of daily data
start_date = datetime.datetime(2014, 1, 1)
end_date = datetime.datetime(2024, 1, 1)

# Generate tickers
tickers = [generate_random_ticker() for _ in range(num_companies)]

# Generate sequential dates
dates = generate_sequential_dates(start_date, end_date, num_dates_per_company)

data = []
for date in dates:
    # Shuffle tickers for each day to mix data
    shuffled_tickers = random.sample(tickers, len(tickers))
    for ticker in shuffled_tickers:
        values = generate_realistic_data()  # Generate realistic OHLCV data
        data.append([ticker, date.strftime('%Y-%m-%d')] + values)

write_to_file('trading_data.txt', data)
