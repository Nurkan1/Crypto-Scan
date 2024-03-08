from datetime import datetime
import requests
import time
from colorama import Fore, Style

def print_explanation():
    """
    Prints an explanation of the program.
    """
    print('='*100)  # Prints a horizontal line at the top
    print("\nThis program scans the top cryptocurrencies from the CoinGecko API,")
    print("gathers information about each one, such as its name, symbol, price in USD,")
    print("change over the last 24 hours, and market cap, and then prints these details to the console.\n")
    print('='*100)  # Prints a horizontal line at the bottom

def fetch_top_50_cryptocurrencies():
    """
    Fetches the top 50 cryptocurrencies from the CoinGecko API.
    """
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        cryptocurrencies = [crypto['id'] for crypto in data]
        return cryptocurrencies
    except requests.exceptions.RequestException:
        return []

original_cryptocurrencies = ['bitcoin', 'ethereum', 'tether', 'solana', 'ripple', 'cardano', 'avalanche', 'polkadot', 'dogecoin', 'shiba-inu', 'terra-luna', 'binancecoin', 'chainlink', 'litecoin', 'stellar', 'cosmos', 'tezos', 'bitcoin-cash', 'tron', 'matic']

def fetch_cryptocurrency_data(cryptocurrency):
    """
    Fetches data for a specific cryptocurrency from the CoinGecko API.
    """
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{cryptocurrency}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        name = data['name']
        symbol = data['symbol'].upper()
        price_usd = data['market_data']['current_price']['usd']
        change_24h = data['market_data']['price_change_percentage_24h']
        market_cap = data['market_data']['market_cap']['usd']
        return name, symbol, price_usd, change_24h, market_cap
    except requests.exceptions.RequestException:
        return None, None, None, None, None
    except KeyError:
        return None, None, None, None, None

def print_data(name, symbol, price_usd, change_24h, market_cap):
    """
    Prints the data of a cryptocurrency.
    """
    print('\nNurSoftware')
    print('='*20)
    print(f'{Fore.CYAN}Name: {name}')
    print(f'Symbol: {symbol}')
    print(f'Price USD: ${price_usd}')
    change_24h_text = f'{Fore.GREEN if change_24h >= 0 else Fore.RED}{change_24h}%'
    print(f'24h Change: {change_24h_text}')
    print(f'Market Cap: ${market_cap}{Style.RESET_ALL}')
    print('='*20)
    print_time_date()  # Print the time and date just below the logo
    

def print_time_date():
    """
    Prints the current time and date in a different style and color.
    """
    now = datetime.now()
    time_date = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f'{Fore.YELLOW}{Style.BRIGHT}Time and Date: {time_date}{Style.RESET_ALL}')

def scan_cryptocurrencies(wait_time=1):
    """
    Scans cryptocurrencies and displays their data on the console.
    """
    try:
        cryptocurrencies = list(set(original_cryptocurrencies + fetch_top_50_cryptocurrencies()))
        minute_counter = 0
        while True:
            for cryptocurrency in cryptocurrencies:
                name, symbol, price_usd, change_24h, market_cap = fetch_cryptocurrency_data(cryptocurrency)
                if name is not None:
                    print_data(name, symbol, price_usd, change_24h, market_cap)
                    time.sleep(wait_time)
                    minute_counter += wait_time
                    # Print the date and time every 5 minutes
                    if minute_counter >= 300:
                        print_time_date()
                        minute_counter = 0
    except KeyboardInterrupt:
        print("Cryptocurrency scan stopped.")

if __name__ == "__main__":
    print_explanation()
    scan_cryptocurrencies()

