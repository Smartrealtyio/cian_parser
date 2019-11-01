import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}

url = 'https://www.cian.ru/sale/flat/194326031/'

# page = requests.get(url, headers = headers).text

# with open('page.html', 'w') as f:
#     f.write(page)

with open('page.html') as f:
    page = f.read()

# ---------------------------------------------
# query

yand_api_token = '31a6ed51-bc46-4d1d-9ac9-e3c2e22d2628'

from bs4 import BeautifulSoup

soup = BeautifulSoup(page, 'lxml')

address = soup.find('div', {'class': 'a10a3f92e9--geo--18qoo'}).find('span').get('content').split(',')
address = [i.strip() for i in address]
print(address)

metros = list(map(lambda x: x.find('a').text, soup.find_all('li', {'class': 'a10a3f92e9--underground--kONgx'})))
print(metros)

main_info_response = soup.find_all('div', {'class': 'a10a3f92e9--info--2ywQI'})
main_info = {}
for info in main_info_response:
    main_info.update({
        info.find('div', {'class': 'a10a3f92e9--info-title--mSyXn'}).text: info.find('div', {
            'class': 'a10a3f92e9--info-text--2uhvD'}).text
    })
print(main_info)

general_info_response = soup.find_all('li', {'class': 'a10a3f92e9--item--_ipjK'})
general_info = {}
for info in general_info_response:
    general_info.update({
        info.find('span', {'class': 'a10a3f92e9--name--3bt8k'}).text: info.find('span', {
            'class': 'a10a3f92e9--value--3Ftu5'}).text
    })
print(general_info)

building_info_response = soup.find_all('div', {'class': 'a10a3f92e9--item--2Ig2y'})
building_info = {}
for info in building_info_response:
    building_info.update({
        info.find('div', {'class': 'a10a3f92e9--name--22FM0'}).text: info.find('div', {
            'class': 'a10a3f92e9--value--38caj'}).text
    })
print(building_info)

real_price = soup.find('span', {'class': 'a10a3f92e9--price_value--1iPpd'}).find('span').text
print(real_price)

history_prices_response = soup.find_all('tr', {'class': 'price_history_widget-history-event-nK20eRdJ'})
history_prices = {}
for info in history_prices_response:
    history_prices.update({
        info.find('td', {'class': 'price_history_widget-event-date-At3o0vWR'}).text:
        info.find('td', {'class': 'price_history_widget-event-price-1hxoWz1dS'}).text
    })
print(history_prices)

update_time = soup.find('div', {'class': 'a10a3f92e9--container--3nJ0d'}).text
print(update_time)

offer_id = url.split('/')[-2]
print(offer_id)


coords_response = requests.get(
    f'https://geocode-maps.yandex.ru/1.x/?apikey={yand_api_token}&format=json&geocode={"".join(address)}').text
coords = json.loads(coords_response)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
longitude, latitude = coords.split(' ')
print(longitude)
print(latitude)

# preparation
street_names = {
    'ул.': 'улица',
    'пер.': 'переулок',
    'ш.': 'шоссе',
    'просп.': 'проспект',
    'бул.': 'бульвар'
}

city = address[0]
district = address[2].split(' ')[1]
street = []
for i in address[3].split(' '):
    if i in street_names:
        street.append(street_names[i])
    else:
        street.append(i)
street = ' '.join(street)
house_number = address[-1]
print(city, district, street, house_number)

full_sq = main_info['Общая'].split(' ')[0].replace(',', '.')
kitchen_sq = -1
life_sq = -1
if 'Жилая' in main_info:
    life_sq = main_info['Жилая'].split(' ')[0].replace(',', '.')
if 'Кухня' in main_info:
    kitchen_sq = main_info['Кухня'].split(' ')[0].replace(',', '.')

floor = main_info['Этаж'].split(' ')[0]
max_floor = main_info['Этаж'].split(' ')[-1]
flats_count = -1
built_year = -1
if 'Построен' in main_info:
    built_year = main_info['Построен']
elif 'Год постройки' in building_info:
    built_year = building_info['Год постройки']

is_apartment = True

renovation = False
if 'Ремонт' in general_info:
    renovation = True

building_type_str = 'UNKNOWN'
if 'Тип дома' in building_info:
    building_type_str = building_info['Тип дома']

has_elevator = False
if 'Лифты' in building_info:
    has_elevator = building_info['Лифты']





