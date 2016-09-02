from bs4 import BeautifulSoup
from app import parse_rates

data = open('test_data_october_2016.html').read()
soup = BeautifulSoup(data, 'html.parser')

rates = parse_rates(soup)

for r in rates:
    print(r)
