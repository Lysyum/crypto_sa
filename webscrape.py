import pandas as pd
import requests
from bs4 import BeautifulSoup

crypto_name_list = []
crypto_market_cap_list = []
crypto_price_list = []
crypto_circulating_supply_list = []
crypto_symbol_list = []

df = pd.DataFrame()


# https://coinmarketcap.com/historical/20220327/
def scrape(date='20220327/'):
    url = 'https://coinmarketcap.com'
    webpage = requests.get(url=url)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    tr = soup.find_all('tr', attrs={'class': 'cmc-table-row'})
    count = 0
    for row in tr:
        if count == 10:
            break;
        count = count + 1
        name_column = row.find('td', attrs={
            'class': 'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__rank'})
        crypto_name = name_column.find('a', attrs={'class': 'cmc-table__column-name--symbol cmc-link'}).text.strip()
        crypto_market_cap = row.find('td', attrs={
            'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip()
        crypto_price = row.find('td', attrs={
            'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'})
        crypto_circulating_supply_and_symbol = row.find('td', attrs={
            'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).text.strip()
        crypto_circulating_supply = crypto_circulating_supply_and_symbol.split(' ')[0]
        crypto_symbol = crypto_circulating_supply_and_symbol.split(' ')[1]

        crypto_name_list.append(crypto_name)
        crypto_market_cap_list.append(crypto_market_cap)
        crypto_price_list.append(crypto_price)
        crypto_circulating_supply_list.append(crypto_circulating_supply)
        crypto_symbol_list.append(crypto_symbol)

scrape()
df['name'] = crypto_name_list
df['Market Cap'] = crypto_market_cap_list
df['Price'] = crypto_price_list
df['Circulating Supply'] = crypto_circulating_supply_list
df['Symbol'] = crypto_symbol_list

df