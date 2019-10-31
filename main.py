import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}

url = 'https://www.cian.ru/sale/flat/212838279/'

page = requests.get(url, headers = headers).text

# with open('page.html', 'w') as f:
#     f.write(page)

# with open('page.html') as f:
#     page = f.read()

# ---------------------------------------------

from bs4 import BeautifulSoup
soup = BeautifulSoup(page, 'lxml')

address = soup.find('div', {'class': 'a10a3f92e9--geo--18qoo'}).find('span').get('content')
print(address)

metros = list(map(lambda x: x.find('a').text, soup.find_all('li', {'class': 'a10a3f92e9--underground--kONgx'})))
print(metros)

result = soup.find_all('div', {'class': 'a10a3f92e9--info--2ywQI'})
main_info = {}
for info in result:
    main_info.update({
        info.find('div', {'class': 'a10a3f92e9--info-title--mSyXn'}).text: info.find('div', {'class': 'a10a3f92e9--info-text--2uhvD'}).text
    })
print(main_info)

result = soup.find_all('li', {'class': 'a10a3f92e9--item--_ipjK'})
general_info = {}
for info in result:
    general_info.update({
        info.find('span', {'class': 'a10a3f92e9--name--3bt8k'}).text: info.find('span', {'class': 'a10a3f92e9--value--3Ftu5'}).text
    })
print(general_info)

result = soup.find_all('div', {'class': 'a10a3f92e9--item--2Ig2y'})
building_info = {}
for info in result:
    building_info.update({
        info.find('div', {'class': 'a10a3f92e9--name--22FM0'}).text: info.find('div', {'class': 'a10a3f92e9--value--38caj'}).text
    })
print(building_info)

price = soup.find('span', {'class': 'a10a3f92e9--price_value--1iPpd'}).find('span').text
print(price)

update_time = soup.find('div', {'class': 'a10a3f92e9--container--3nJ0d'}).text
print(update_time)

offer_id = url.split('/')[-2]
print(offer_id)