import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import psycopg2
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
import logging
import sys
import os
import re
import random
from settings_local import *



class CianParser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=path_to_driver, options=options)
    # driver = webdriver.Firefox(executable_path=path_to_driver, options=options)

    street_names = {
        'ул.': 'улица',
        'пер.': 'переулок',
        'ш.': 'шоссе',

        'просп.': 'проспект',
        'бул.': 'бульвар',
        'деревня': 'деревня'
    }
    district_names = ['р-н', 'деревня', 'поселение', 'поселок']
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }
    building_types = {
        'Деревянный': 'WOOD',
        'Кирпичный': 'BRICK',
        'Монолитный': 'MONOLIT',
        'Панельный': 'PANEL',
        'Монолитно-кирпичный': 'MONOLIT_BRICK',
        'Блочный': 'BLOCK'
    }
    flat_types = ['SECONDARY', 'NEW_FLAT']

    def str_prepare(self, s):
        return s.replace('ё', 'е').replace('Ё', 'Е')

    def is_closed(self, url):
        soup = self.captcha_check(url)

        try:
            soup.find('div', {'class': 'a10a3f92e9--container--1In69'}).text
            return True
        except:
            return False

    def parse_flat_info(self, url):

        soup = self.captcha_check(url)

        try:
            address = soup.find('div', {'class': 'a10a3f92e9--geo--18qoo'}).find('span').get('content').split(',')
            address = [i.strip() for i in address]

            try:
                image = soup.find_all('img', {'class': 'fotorama__img'})[0].get('src')
            except:
                image = 'fail'
            rooms_info = soup.find('h1', {'class': 'a10a3f92e9--title--2Widg'}).text.split(',')[0].lower()

            metros_response = soup.find_all('li', {'class': 'a10a3f92e9--underground--kONgx'})
            metros = {}
            for metro in metros_response:
                metros.update({
                    self.str_prepare(metro.find('a').text): metro.find('span').text
                })

            main_info_response = soup.find_all('div', {'class': 'a10a3f92e9--info--3XiXi'})
            # print(main_info_response)
            main_info = {}
            for info in main_info_response:
                main_info.update({
                    info.find('div', {'class': 'a10a3f92e9--info-title--2bXM9'}).text: info.find('div', {
                        'class': 'a10a3f92e9--info-value--18c8R'}).text
                })

            agency_response = soup.find_all('h2', {'class': 'a10a3f92e9--title--2gUWg'})
            if agency_response:
                # if agency_response[0].text.split(' ')[0] == 'ID' and agency_response[0].text.split(' ')[1].isdigit():
                #     agency = None
                # else:
                    agency = agency_response[0].text
            else:
                agency = None

            is_rented = True
            is_rented_info = soup.find_all('span', {'class': 'a10a3f92e9--status--NCVlN'})
            if is_rented_info:
                is_rented = False if 'сдача' in is_rented_info[0].text else True

            general_info_response = soup.find_all('li', {'class': 'a10a3f92e9--item--_ipjK'})
            general_info = {}
            for info in general_info_response:
                general_info.update({
                    info.find('span', {'class': 'a10a3f92e9--name--3bt8k'}).text: info.find('span', {
                        'class': 'a10a3f92e9--value--3Ftu5'}).text
                })

            building_info_response = soup.find_all('div', {'class': 'a10a3f92e9--item--2Ig2y'})
            building_info = {}
            for info in building_info_response:
                building_info.update({
                    info.find('div', {'class': 'a10a3f92e9--name--22FM0'}).text: info.find('div', {
                        'class': 'a10a3f92e9--value--38caj'}).text
                })

            real_price = soup.find('span', {'class': 'a10a3f92e9--price_value--1iPpd'}).find('span').text

            history_prices_response = soup.find_all('tr', {'class': 'price_history_widget-history-event-nK20eRdJ'})
            history_prices = {}
            for info in history_prices_response:
                history_prices.update({
                    info.find('td', {'class': 'price_history_widget-event-date-At3o0vWR'}).text:
                        info.find('td', {'class': 'price_history_widget-event-price-1hxoWz1dS'}).text
                })

            logging.info(' waiting ')

            self.driver.find_element_by_class_name('a10a3f92e9--container--1wUf1').click()
            import time
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            date = soup.find('div', {'class': 'a10a3f92e9--information--AyP9e'}).find('div').text.split(' ')[-1].strip()

            day = int(date.split('.')[0])
            month = int(date.split('.')[1])
            year = int(date.split('.')[2])

            created_at = str(datetime(year, month, day))

            logging.info(' DATE ' + created_at)

            # update_time = soup.find('div', {'class': 'a10a3f92e9--container--3nJ0d'}).text

            offer_id = url.split('/')[-2]

            # -------------------
            # Data transformation to correct type
            for metro, data in metros.items():
                metro_address = ''
                try:
                    token = tokens[random.randint(0, len(tokens) - 1)]
                    # print(token, flush=True)
                    metro_address = address[0] + ',метро ' + metro
                    coords_response = requests.get(
                        f'https://geocode-maps.yandex.ru/1.x/?apikey={token}&format=json&geocode={metro_address}',
                        timeout=10).text
                    coords = \
                        json.loads(coords_response)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                            'Point'][
                            'pos']
                    longitude, latitude = coords.split(' ')
                    metro_longitude = float(longitude)
                    metro_latitude = float(latitude)
                except IndexError:
                    logging.info(' bad address for yandex-api ' + metro_address)
                    metro_longitude = 0
                    metro_latitude = 0
                metros.update({
                    metro: {
                        'time_to_metro': sum([int(i) if i.isdigit() else 0 for i in data.split(' ')]),
                        'transport_type': 'ON_FOOT' * int('пешком' in data.split(' ')) or 'ON_TRANSPORT',
                        'metro_longitude': metro_longitude,
                        'metro_latitude': metro_latitude
                    }
                })

            city = address[0]

            district = ''
            for district_name in self.district_names:
                for address_piece in address:
                    if district_name in address_piece:
                        if district_name in address_piece.split(' ')[0]:
                            district = ' '.join(address_piece.split(' ')[1:])
                        elif district_name in address_piece.split(' ')[-1]:
                            district = ' '.join(address_piece.split(' ')[:-1])
                        else:
                            district = ' '.join(address_piece)
                        break
                if district:
                    break

            district = self.str_prepare(district)

            street = []
            for i in address[-2].split(' '):
                if i in self.street_names:
                    street.append(self.street_names[i])
                else:
                    street.append(i)
            street = ' '.join(street)
            house_number = address[-1]

            full_sq = float(main_info['Общая'].split('\xa0')[0].replace(',', '.'))
            kitchen_sq = -1
            life_sq = -1
            if 'Жилая' in main_info:
                life_sq = float(main_info['Жилая'].split('\xa0')[0].replace(',', '.'))
            if 'Кухня' in main_info:
                kitchen_sq = float(main_info['Кухня'].split('\xa0')[0].replace(',', '.'))

            floor = int(main_info['Этаж'].split(' ')[0])
            max_floor = int(main_info['Этаж'].split(' ')[-1])
            flats_count = -1
            built_year = -1
            if 'Построен' in main_info:
                built_year = int(main_info['Построен'])
            elif 'Год постройки' in building_info:
                built_year = int(building_info['Год постройки'])

            rent_quarter = None
            rent_year = None
            if 'Срок сдачи' in main_info:
                if 'кв' in main_info['Срок сдачи']:
                    rent_quarter = int(main_info['Срок сдачи'].split(' кв. ')[0])
                    rent_year = int(main_info['Срок сдачи'].split(' кв. ')[1])
                else:
                    rent_year = int(main_info['Срок сдачи'])

            is_apartment = True
            closed = False

            renovation = False
            renovation_type = None
            if 'Ремонт' in general_info:
                renovation_type = general_info['Ремонт']
                if general_info['Ремонт'] != 'Без ремонта':
                    renovation = True

            windows_view = general_info.get('Вид из окон')


            building_type_str = 'UNKNOWN'
            if 'Тип дома' in building_info:
                if building_info['Тип дома'] in self.building_types:
                    building_type_str = self.building_types[building_info['Тип дома']]

            has_elevator = False
            if 'Лифты' in building_info:
                if building_info['Лифты'] != 'Нет':
                    has_elevator = True

            real_price = [str(datetime.now()), int(''.join(real_price.split()[:-1]))]
            prices = []
            for date, price in history_prices.items():
                date = date.split(' ')
                if date[0] == 'сегодня':
                    day = datetime.now().day
                    month = datetime.now().month
                elif date[0] == 'вчера':
                    day = (datetime.now() - timedelta(hours=24)).day
                    month = (datetime.now() - timedelta(hours=24)).month
                elif date[0] == 'позавчера':
                    day = (datetime.now() - timedelta(hours=48)).day
                    month = (datetime.now() - timedelta(hours=48)).month
                else:
                    day = int(date[0])
                    month = int(self.months[date[1]])
                time = date[-1]
                if ':' in time:
                    hours = int(date[-1].split(':')[0])
                    minutes = int(date[-1].split(':')[1])
                    prices.append(
                        [str(datetime(datetime.now().year, month, day, hours, minutes)),
                         int(''.join(price.split()[:-1]))])
                else:
                    year = int(time)
                    prices.append([str(datetime(year, month, day)), int(''.join(price.split()[:-1]))])
            prices.append(real_price)

            if address[0] == 'Москва' or address[0] == 'Санкт-Петербург':
                address = ', '.join(['Россия', city, street, house_number])
            else:
                address = ', '.join(['Россия', address[0], address[1], street, house_number])
            address = self.str_prepare(address)

            try:
                rooms_count = int(''.join([i for i in rooms_info.split(' ')[0] if i.isdigit()]))
            except ValueError:
                rooms_count = -1

            try:
                token = tokens[random.randint(0, len(tokens)-1)]
                coords_response = requests.get(
                    f'https://geocode-maps.yandex.ru/1.x/?apikey={token}&format=json&geocode={address}',
                    timeout=10).text
                coords = \
                    json.loads(coords_response)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                        'Point'][
                        'pos']
                longitude, latitude = coords.split(' ')
                longitude = float(longitude)
                latitude = float(latitude)
            except IndexError:
                logging.info(' bad address for yandex-api ' + address)
                return False


            result = {
                'image': image,
                'offer_id': offer_id,
                'rooms_count': rooms_count,
                'district': district,
                'address': address,
                'full_sq': full_sq,
                'life_sq': life_sq,
                'kitchen_sq': kitchen_sq,
                'floor': floor,
                'max_floor': max_floor,
                'flats_count': flats_count,
                'built_year': built_year,
                'is_apartment': is_apartment,
                'closed': closed,
                'renovation': renovation,
                'building_type_str': building_type_str,
                'has_elevator': has_elevator,
                'prices': prices,
                'metros': metros,
                'longitude': longitude,
                'latitude': latitude,
                'created_at': created_at,
                'agency': agency,
                'is_rented': is_rented,
                'rent_quarter': rent_quarter,
                'rent_year': rent_year,
                'renovation_type': renovation_type,
                'windows_view': windows_view
            }

            return result
        except Exception as error:
            logging.info(str(error))
            return False


    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def captcha_check(self, url):
        try:
            logging.info(url)
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            if soup.find('div', {'id': 'captcha'}):
                logging.info(' captcha... sleeping')
                time.sleep(600)
                self.captcha_check(url)
            else:
                return soup
        except TimeoutException:
            logging.info(' connection fail... RESTARTING APP')
            time.sleep(100)
            self.driver.quit()
            time.sleep(100)
            self.restart()
        except:
            logging.info(' connection fail... RESTARTING APP, UNKNOWN ERROR')
            time.sleep(100)
            self.driver.quit()
            time.sleep(100)
            self.restart()

    def get_flats_url(self, url):
        soup = self.captcha_check(url)
        try:
            pages_response = soup.find_all('a', {'class': 'c6e8ba5398--header--1fV2A'})
            pages_url = [page.get('href') for page in pages_response]
        except:
            pages_url = []
        try:
            next_page_response = soup.find('ul', {'class': '_93444fe79c--list--HEGFW'}).find_all('li')
        except:
            return pages_url, 0
        my_page = soup.find('li', {'class': '_93444fe79c--list-item--2KxXr _93444fe79c--list-item--active--3dOSi'})
        try:
            if my_page == next_page_response[-1]:
                next_page_number = 0
            else:
                next_page_number = int(my_page.find('span').text) + 1

        except:
            next_page_number = 0

        time.sleep(7)

        return pages_url, next_page_number

    def parse(self, url, whole_parsed_count, whole_saved_count, whole_count):
        page_number = 1
        next_page_number = 1
        count = 0
        parsed_count = 0
        saved_count = 0
        flat_type = int(re.findall(r'object_type%5B0%5D=(\d)', url)[0])
        city_id = int(re.findall(r'region=(\d)', url)[0])
        while (page_number == next_page_number):
            time.sleep(2)
            res_url = url.format(page_number)
            logging.info(' ' + str(res_url))
            page_number += 1
            new_urls, next_page_number = self.get_flats_url(res_url)

            logging.info(' ' + str(len(new_urls)))
            for flat_url in new_urls:
                result = None
                result = self.parse_flat_info(flat_url)
                if result:
                    result['flat_type'] = self.flat_types[flat_type-1]
                    result['city_id'] = city_id
                    logging.info(' parsed ok')
                    logging.info(' ' + str(result))
                    parsed_count += 1
                    whole_parsed_count += 1
                else:
                    logging.info(' fail in parsing ' + str(flat_url))
                if result:
                    try:
                        response = requests.post(saving_api_url + '/api/save/', json=json.dumps(result),
                                                 timeout=10).content
                        if json.loads(response)['result']:
                            logging.info(' saved ok')
                            saved_count += 1
                            whole_saved_count += 1
                        else:
                            logging.info(' fail in saving')
                    except:
                        logging.info(' fail in post query')
                        time.sleep(10)
                logging.info('')
                count += 1
                whole_count += 1


            logging.info(' end for page ' + str(count) + ' parsed ' + str(parsed_count) + ' saved ' + str(saved_count))
            logging.info(
                ' the whole parsing info ' + str(whole_count) + ' parsed ' + str(whole_parsed_count) + ' saved ' + str(
                    whole_saved_count))

        return whole_parsed_count, whole_saved_count, whole_count


    def flats_closing_check(self):
        response = requests.get(saving_api_url + '/api/flats/').content
        offers = json.loads(response)['result']

        for offer in offers:
            time.sleep(1)
            result = self.is_closed('https://www.cian.ru/sale/flat/' + str(offer[0]))
            if result:
                try:
                    logging.info(' CLOSED')
                    logging.info(str(offer[0]))
                    response = requests.post(saving_api_url + '/api/closing/',
                                             json=json.dumps([str(offer[0])])).content
                    logging.info(' ' + str(json.loads(response)['result']))
                except:
                    logging.info(' save api connection fail, sleep 60')
                    time.sleep(60)
            else:
                logging.info(' opened')

        return


if __name__ == '__main__':
    print('params', sys.argv, flush=True)
    urls = {
        'msk': 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&maxtarea={maxtarea}&mintarea={mintarea}&object_type%5B0%5D={type}&offer_type=flat&p={page}&region=1',
        'spb': 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&maxtarea={maxtarea}&mintarea={mintarea}&object_type%5B0%5D={type}&offer_type=flat&p={page}&region=2'
    }
    parse_types = {
        'sec': 1,
        'new': 2
    }

    url_for_start = urls[sys.argv[1]]
    parse_type = parse_types[sys.argv[2]]
    try:
        cycle = int(sys.argv[3])
        logging.basicConfig(filename='closer.log', level=logging.INFO)
    except:
        cycle = 1
        logging.basicConfig(filename=sys.argv[1] + '_' + sys.argv[2] + '2.log', level=logging.INFO)


    parser = CianParser()

    # cycle = random.randint(0, 1)

    while True:

        # cycle += 1

        if cycle % 2 != 0:

            mintareas = [i for i in range(11, 110)] + [i for i in range(110, 150, 5)] \
                        + [i for i in range(150, 200, 10)] + [i for i in range(200, 250, 25)] + [250, 400]
            maxtareas = [i for i in range(11, 110)] + [i for i in range(115, 155, 5)] \
                        + [i for i in range(160, 210, 10)] + [i for i in range(225, 275, 25)] + [400, 3000]
            whole_parsed_count = 0
            whole_saved_count = 0
            whole_count = 0

            for mintarea, maxtarea in zip(mintareas, maxtareas):
                for i in range(2, 0, -1):
                    # logging.info('type ' + str(i))
                    url = url_for_start.format(
                        maxtarea=maxtarea,
                        mintarea=mintarea,
                        type=i,
                        page=1
                    )
                    url = url.replace('p=1', 'p={}')
                    logging.info(' parsing from ' + str(mintarea) + ' to ' + str(maxtarea))
                    whole_parsed_count, whole_saved_count, whole_count = parser.parse(url, whole_parsed_count,
                                                                                      whole_saved_count,
                                                                                      whole_count)
                logging.info('')

                time.sleep(10)
            print('All flats parsed')

        else:

            parser.flats_closing_check()
            print('All flats checked')

        print('next step')
        time.sleep(60)
