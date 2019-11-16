import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import psycopg2
import sys
import time
from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
from selenium import webdriver


# orig_stdout = sys.stdout
# f = open('out.txt', 'a')
# sys.stdout = f
driver = webdriver.Chrome(executable_path="/Users/egor/PycharmProjects/chromedriver")

class CianParser():
    # s = requests.Session()
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language': 'en-en,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Connection': 'keep-close',
    # }

    proxies = ['95.79.36.55:44861', '213.110.230.247:8080', '109.170.96.26:8080', '193.9.245.199:8080',
               '77.236.251.234:8080', '92.53.124.209:3128', '85.143.66.138:8080', '85.143.254.20:8080',
               '91.230.11.164:8080', '82.147.120.32:35542', '94.141.60.69:8080', '37.230.147.206:8080',
               '212.33.28.51:8080',
               '195.62.70.22:8080', '188.128.63.210:8080', '217.145.150.19:42191', '212.220.1.38:8080',
               '89.22.132.57:8080',
               '95.138.228.28:8080', '77.246.237.230:80', '62.33.207.196:3128', '37.235.65.76:8080',
               '185.87.50.49:3128',
               '95.167.150.166:49464', '85.173.165.36:46330']
    proxy_number = 0
    cookies = {
        'VID': '14Z1s204aa1t00000D0Q54Xt::48707187:0-0-2829259-0:',
        'IDE': 'AHWqTUnhVBkv_NdiHLOPgnDkFFVeLjDpqjQTaPAQOaJyhgC8pLIyJkp0OD-_i8Tt',
        '__zzat140': 'MDA0dBA=Fz2+aQ==',
        '_CIAN_GK': '9ef1db87-bc4c-44b0-9ae2-cdda7342da7f',
        '_cmg_csst8yrRI': '1573137226',
        '_comagic_id8yrRI': '2441941911.3853297180.1573137225',
        '_fbp': 'fb.1.1572451342223.830816584',
        '_ga': 'GA1.2.171392150.1572451341',
        '_gcl_au': '1.1.184971591.1572451340',
        '_gid': 'GA1.2.972360331.1573729574',
        'afUserId': '19427fdc-c2b7-4f09-b377-dc520addf4c6',
        'af_id': '19427fdc-c2b7-4f09-b377-dc520addf4c6',
        'audience_serp_light': 'control',
        'cfids140': 'BwZsfMM4EtJEwniUuachwZWOz0xslwSGs+ZqOgSKiTM4ch58GaRmBP4IXKWg4qy+2x2ccuyyQOvo9o1i+P5wq5uMzaH7Te0nUusMU9ohdYmrzZ67xrjVUiQbYekRwyj3GnnE6LPvjW1KXMYeI/7V1+oFWXkPsxgvOgNAiQ==',

        'cryptouid': '15020567973508632186',
        'cryptouid_actual': '1',
        'cryptouid_sign': '45275593b8390a3146f332d6cb526ef3',
        'cto_bundle': 'SPSrP19IaTU1dVI5QlNmTzFmRFdPNWtGdG1xeWJDZFhMUWlONGFrRno5bWsyVmNLQmtjVW8lMkZHOWxtOWp1SmxiQjFIYWZvaCUyRmZ0S01wRHl3WFZjQXB0WGwyRG5VUyUyQjREdENSanlTRFBSdXNzS2d2R2EwMVl0NXRWc3pnQXAycFJZTXVrTUZsYSUyRkFnbE5VT212MUxMcUFOTDRIUSUzRCUzRA',
        'cto_lwid': '70433073-00de-4f48-90ba-68d9fa6bfd60',

        'datr': 'aOOVXcZVbleA3zPZN2Rm5sWW',
        'financeMark': 'd7580668-9ace-4f25-8546-12250bca474a',

        'fingerprint': 'e4299ef1fc8c4e1d4f42e46491769ee0',
        'flocktory-uuid': 'b586a86b-a8a8-490f-94c2-774a7345cff6-9',
        'forever_region_id': '2',
        'forever_region_name': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
        'fr': '0cV5H70AsVukSfgbh..BdXU8X..F3E.1.0.BdzTUm.',
        'incap_ses_378_2094920': 'DjqrX74r/l+yShnm0O0+BRc1zV0AAAAAsjNYCcaxcIt6G3Eei4baOg==',
        'login_mro_popup': 'meow',
        'luid1': 'i:cgfkaei:i:cgfkaei:a',
        'luid1_ts': 'faawpgq:fciymmt',
        'p': 'rEgBAGm3GAAA',

        # 'newobject_active': '1',
        # 'newobject_all': '1',
        # 'newobject_scount': '5',
        # 'pview': '2',
        'read_offers_compressed': 'EwRhwDghOBWBmIA',
        'remixdt': '0',
        'remixlang': '0',
        'remixrefkey': 'c624762e9152ba31bd',
        'remixscreen_depth': '24',
        'remixsid': 'b5aa407018c0c5575333cec63d6a61e0ccce15bf57909a94ea54d60cd86d2',
        'remixstid': '1147850838_502ed2e5a2c78a145c',
        'remixusid': 'YzZmMzYwNTc3MmFiYmRjNDM0MTc4OTI1',
        'sb': 'aOOVXS06ckZ8Cr6QlWoTT_oC',

        # 'seen_pins_compressed': 'IwhME4BYDpOB2cTlIDT0gNgKzeqURFZAWhGAGZQL95MAGRp+4dbYcADmnEyA',
        # 'serp_registration_trigger_popup': '1',
        # 'serp_stalker_banner': '1',
        'session_main_town_region_id': '2',
        'session_region_id': '4588',
        # 'sopr_session': '27de0a2e72cc4d1e',
        'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
        'tmr_detect': '0%7C1573729661057',
        'uid': '6bd19703-cd04-4eff-9eef-4cef26fe6c94',

        'tildauid': '1572958412722.492619',
        # 'tmr_detect': '0%7C1573550238782',
        'uxfb_usertype': 'searcher',

        'uxs_mig': '1',
        'uxs_uid': 'a80c0c20-fb2e-11e9-9ddd-07c33823a03f',
        'visid_incap_2094920': 'DFnzZK1SSKWpI9HYdfpSogm0uV0AAAAAQUIPAAAAAACz+QMawkB3xpw9QErHiisG'
    }
    # s.headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    # }
    # proxies = {
    #     "http": "http://user:pass@10.10.10.10:8000"
    # }
    yand_api_token = '31a6ed51-bc46-4d1d-9ac9-e3c2e22d2628'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'
    }
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

    def parse_flat_info(self, url):
        # page = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10).text
        # page = self.s.get(url, timeout=10).text
        # print(page)
        # with open('page.html') as f:
        #     page = f.read()

        # All responses

        # soup = BeautifulSoup(page, 'lxml')
        soup = self.captcha_check(url)

        address = soup.find('div', {'class': 'a10a3f92e9--geo--18qoo'}).find('span').get('content').split(',')
        address = [i.strip() for i in address]

        rooms_info = soup.find('h1', {'class': 'a10a3f92e9--title--2Widg'}).text.split(',')[0].lower()

        metros_response = soup.find_all('li', {'class': 'a10a3f92e9--underground--kONgx'})
        metros = {}
        for metro in metros_response:
            metros.update({
                metro.find('a').text: metro.find('span').text
            })

        main_info_response = soup.find_all('div', {'class': 'a10a3f92e9--info--2ywQI'})
        main_info = {}
        for info in main_info_response:
            main_info.update({
                info.find('div', {'class': 'a10a3f92e9--info-title--mSyXn'}).text: info.find('div', {
                    'class': 'a10a3f92e9--info-text--2uhvD'}).text
            })

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

        # update_time = soup.find('div', {'class': 'a10a3f92e9--container--3nJ0d'}).text

        offer_id = url.split('/')[-2]

        # -------------------
        # Data transformation to correct type
        for metro, data in metros.items():
            metros.update({
                metro: {
                    'time_to_metro': sum([int(i) if i.isdigit() else 0 for i in data.split(' ')]),
                    'transport_type': 'ON_FOOT' * int('пешком' in data.split(' ')) or 'ON_TRANSPORT'
                }
            })

        city = address[0]
        district_pieces = address[-3].split(' ')
        if district_pieces[0] in self.district_names:
            district = " ".join(district_pieces[1:])
        elif district_pieces[-1] in self.district_names:
            district = " ".join(district_pieces[:-1])
        else:
            district = " ".join(district_pieces)

        street = []
        for i in address[-2].split(' '):
            if i in self.street_names:
                street.append(self.street_names[i])
            else:
                street.append(i)
        street = ' '.join(street)
        house_number = address[-1]

        full_sq = float(main_info['Общая'].split(' ')[0].replace(',', '.'))
        kitchen_sq = -1
        life_sq = -1
        if 'Жилая' in main_info:
            life_sq = float(main_info['Жилая'].split(' ')[0].replace(',', '.'))
        if 'Кухня' in main_info:
            kitchen_sq = float(main_info['Кухня'].split(' ')[0].replace(',', '.'))

        floor = int(main_info['Этаж'].split(' ')[0])
        max_floor = int(main_info['Этаж'].split(' ')[-1])
        flats_count = -1
        built_year = -1
        if 'Построен' in main_info:
            built_year = int(main_info['Построен'])
        elif 'Год постройки' in building_info:
            built_year = int(building_info['Год постройки'])

        is_apartment = True
        closed = False

        renovation = False
        if 'Ремонт' in general_info:
            if general_info['Ремонт'] != 'Без ремонта':
                renovation = True

        building_type_str = 'UNKNOWN'
        if 'Тип дома' in building_info:
            if building_info['Тип дома'] in self.building_types:
                building_type_str = self.building_types[building_info['Тип дома']]

        has_elevator = False
        if 'Лифты' in building_info:
            if building_info['Лифты'] != 'Нет':
                has_elevator = True

        real_price = [datetime.now(), int(''.join(real_price.split()[:-1]))]
        prices = []
        for date, price in history_prices.items():
            date = date.split(' ')
            if date[0] == 'сегодня':
                day = datetime.now().day
                month = datetime.now().month
            elif date[0] == 'вчера':
                day = (datetime.now() - timedelta(hours=24)).day
                month = (datetime.now() - timedelta(hours=24)).month
            else:
                day = int(date[0])
                month = int(self.months[date[1]])
            time = date[-1]
            if ':' in time:
                hours = int(date[-1].split(':')[0])
                minutes = int(date[-1].split(':')[1])
                prices.append(
                    [datetime(datetime.now().year, month, day, hours, minutes), int(''.join(price.split()[:-1]))])
            else:
                year = int(time)
                prices.append([datetime(year, month, day), int(''.join(price.split()[:-1]))])
        prices.append(real_price)

        if address[0] == 'Москва':
            address = ', '.join(['Россия', city, street, house_number])
        else:
            address = ', '.join(['Россия', address[0], address[1], street, house_number])

        try:
            rooms_count = int(''.join([i for i in rooms_info.split(' ')[0] if i.isdigit()]))
        except ValueError:
            rooms_count = -1
        # if rooms_info == 'студия' or rooms_info == 'апартаменты-студия' or rooms_info == 'апартаменты свободной планировки':
        #     rooms_count = -1
        # else:
        #     rooms_count = int(''.join([i for i in rooms_info.split(' ')[0] if i.isdigit()]))

        result = {
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
            'metros': metros
        }

        return result

    def save_to_db(self, flat):
        try:
            conn = psycopg2.connect(host='localhost', dbname='yand_cian', user='cian_parser', password='DYqmyKe4')
            cur = conn.cursor()
        except:
            return False

        cur.execute("select id from districts where name=%s;", (flat['district'],))
        try:
            district_id = cur.fetchone()[0]
        except:
            print('district does not exist')
            conn.close()
            return False
        print('district_id', district_id)

        metro_ids = {}
        for metro in flat['metros']:
            try:
                cur.execute("select id from metros where name=%s;", (metro,))
                metro_id = cur.fetchone()[0]
                metro_ids.update({metro: metro_id})
            except:
                print('metro', metro, 'does not exist')
                # try:
                #     metro_location = 'Москва,метро '+ metro
                #     coords_response = requests.get(
                #         f'https://geocode-maps.yandex.ru/1.x/?apikey={self.yand_api_token}&format=json&geocode={metro_location}', timeout=5).text
                #     coords = \
                #     json.loads(coords_response)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                #         'Point']['pos']
                #     longitude, latitude = coords.split(' ')
                #     longitude = float(longitude)
                #     latitude = float(latitude)
                #
                #     cur.execute("""insert into metros (longitude, latitude, city_id, created_at, updated_at, metro_id, name)
                #                    values (%s, %s, %s, %s, %s, %s, %s)""", (
                #         longitude,
                #         latitude,
                #         1,
                #         datetime.now(),
                #         datetime.now(),
                #         0,
                #         metro
                #     ))
                #     print('udated', metro)
                # except:
                print('fail in updating', metro)
                continue

        try:
            coords_response = requests.get(
                f'https://geocode-maps.yandex.ru/1.x/?apikey={self.yand_api_token}&format=json&geocode={flat["address"]}',
                timeout=5).text
            coords = \
                json.loads(coords_response)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                    'Point'][
                    'pos']
            longitude, latitude = coords.split(' ')
            longitude = float(longitude)
            latitude = float(latitude)
        except IndexError:
            print('bad address for yandex-api', flat['address'])
            conn.close()
            return False

        cur.execute("select id from buildings where address=%s or longitude=%s and latitude=%s;",
                    (flat['address'], longitude, latitude))
        is_building_exist = cur.fetchone()
        if not is_building_exist:

            cur.execute(
                """insert into buildings 
                   (max_floor, building_type_str, built_year, flats_count, address, renovation, 
                    has_elevator, longitude, latitude, district_id, created_at, updated_at)
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                    flat['max_floor'],
                    flat['building_type_str'],
                    flat['built_year'],
                    flat['flats_count'],
                    flat['address'],
                    flat['renovation'],
                    flat['has_elevator'],
                    longitude,
                    latitude,
                    district_id,
                    datetime.now(),
                    datetime.now()
                ))
            cur.execute("select id from buildings where address=%s;", (flat['address'],))
            building_id = cur.fetchone()[0]
            print('building_id', building_id)
            for metro, metro_id in metro_ids.items():
                try:
                    cur.execute(
                        """insert into time_metro_buildings (building_id, metro_id, time_to_metro, transport_type, created_at, updated_at) 
                           values (%s, %s, %s, %s, %s, %s);""", (
                            building_id,
                            metro_id,
                            flat['metros'][metro]['time_to_metro'],
                            flat['metros'][metro]['transport_type'],
                            datetime.now(),
                            datetime.now()
                        ))
                except:
                    print('some new error')
                    conn.close()
                    return False
        else:
            building_id = is_building_exist[0]
            print('building already exist', building_id)

        cur.execute('select * from flats where offer_id=%s', (flat['offer_id'],))
        is_offer_exist = cur.fetchone()
        if not is_offer_exist:
            cur.execute(
                """insert into flats (full_sq, kitchen_sq, life_sq, floor, is_apartment, building_id, created_at, updated_at, offer_id, closed, rooms_total) 
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    flat['full_sq'],
                    flat['kitchen_sq'],
                    flat['life_sq'],
                    flat['floor'],
                    flat['is_apartment'],
                    building_id,
                    datetime.now(),
                    datetime.now(),
                    flat['offer_id'],
                    flat['closed'],
                    flat['rooms_count']
                ))
            cur.execute('select id from flats where offer_id=%s;', (flat['offer_id'],))
            flat_id = cur.fetchone()[0]
            print('flat_id', flat_id)
        else:
            flat_id = is_offer_exist[0]
            print('flat already exist', flat_id)

            cur.execute("""update flats 
                           set full_sq=%s, kitchen_sq=%s, life_sq=%s, floor=%s, is_apartment=%s, building_id=%s, updated_at=%s, closed=%s, rooms_total=%s 
                           where id=%s""", (
                flat['full_sq'],
                flat['kitchen_sq'],
                flat['life_sq'],
                flat['floor'],
                flat['is_apartment'],
                building_id,
                datetime.now(),
                flat['closed'],
                flat['rooms_count'],
                flat_id
            ))
            print('updated', flat_id)

        for price_info in flat['prices']:
            cur.execute('select * from prices where changed_date=%s', (price_info[0],))
            is_price_exist = cur.fetchone()
            if not is_price_exist:
                cur.execute("""insert into prices (price, changed_date, flat_id, created_at, updated_at) 
                               values (%s, %s, %s, %s, %s);""", (
                    price_info[1],
                    price_info[0],
                    flat_id,
                    datetime.now(),
                    datetime.now()
                ))

        conn.commit()
        cur.close()

        return True

    def captcha_check(self, url):
        try:
            # response = requests.get(url, headers=self.headers, timeout=10)
            driver.get(url)
            # response = requests.get(url, headers=self.headers, proxies={'http': 'http://' + self.proxies[self.proxy_number]}, timeout=10)
            # print('http://' + self.proxies[self.proxy_number])
            # soup = BeautifulSoup(response.text, 'lxml')
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # print(soup)
            if soup.find('div', {'id': 'captcha'}):
                print('captcha... sleeping')
                # self.s = requests.Session()
                # time.sleep(60 * 60)
                # print('changing proxy')
                # if self.proxy_number != len(self.proxies):
                #     self.proxy_number += 1
                # else:
                #     self.proxy_number = 0
                self.captcha_check(url)
            else:
                # self.cookies = response.cookies
                # print(self.cookies)
                return soup
        except:
            print('connection fail... sleeping 1 minute')
            # print('changing proxy')
            # if self.proxy_number != len(self.proxies):
            #     self.proxy_number += 1
            # else:
            #     self.proxy_number = 0
            # self.captcha_check(url)
            time.sleep(3)
            self.captcha_check(url)

    def get_flats_url(self, url):
        # response = self.s.get(url, self.headers, timeout=10).text
        # response = self.s.get(url, timeout=10).text
        # with open('captcha.txt', 'w') as f:
        #     f.write(response)
        # # print(response)
        # soup = BeautifulSoup(response, 'lxml')
        soup = self.captcha_check(url)
        pages_response = soup.find_all('a', {'class': 'c6e8ba5398--header--1fV2A'})
        pages_url = [page.get('href') for page in pages_response]
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
        while (page_number == next_page_number):
            time.sleep(2)
            res_url = url.format(page_number)
            print(res_url)
            page_number += 1
            new_urls, next_page_number = self.get_flats_url(res_url)

            print(*new_urls, sep='\n')
            for flat_url in new_urls:
                result = None
                try:
                    result = self.parse_flat_info(flat_url)
                    print('parsed ok')
                    print(result)
                    parsed_count += 1
                    whole_parsed_count += 1
                except:
                    print('fail in parsing ', flat_url)
                if result:
                    # try:
                    if self.save_to_db(result):
                        print('saved ok')
                        saved_count += 1
                        whole_saved_count += 1
                    else:
                        print('fail in saving')
                    # except:
                    #     print('fail in saving', flat_url, result)
                print()
                count += 1
                whole_count += 1
                if whole_count % 20 == 0:
                    print('sleep')
                    # time.sleep(30)
                # time.sleep(1)

            print('end for page', count, 'parsed', parsed_count, 'saved', saved_count)

        print('the whole parsinf info', whole_count, 'parsed', whole_parsed_count, 'saved', whole_saved_count)
        return whole_parsed_count, whole_saved_count, whole_count

    def flat_closing_check(self):
        print('start closing checking...')
        conn = psycopg2.connect(host='localhost', dbname='yand_cian', user='cian_parser', password='DYqmyKe4')
        cur = conn.cursor()
        cur.execute("select offer_id from flats;")
        offers = cur.fetchall()
        for offer in offers:
            try:
                result = self.parse_flat_info("https://www.cian.ru/sale/flat/{}/".format(offer))
                print('flat ok')
            except:
                cur.execute("update flats set closed=%s where offer_id=%s", (True, offer))
                print('flat closed')
            time.sleep(2)


parser = CianParser()

mintareas = [i for i in range(11, 110)] + [i for i in range(110, 150, 5)] + [i for i in range(150, 200, 10)] + [i for i
                                                                                                                in
                                                                                                                range(
                                                                                                                    200,
                                                                                                                    250,
                                                                                                                    25)] + [
                250, 400]
maxtareas = [i for i in range(11, 110)] + [i for i in range(115, 155, 5)] + [i for i in range(160, 210, 10)] + [i for i
                                                                                                                in
                                                                                                                range(
                                                                                                                    225,
                                                                                                                    275,
                                                                                                                    25)] + [
                400, 3000]
whole_parsed_count = 0
whole_saved_count = 0
whole_count = 0

# parser.flat_closing_check()
#
for mintarea, maxtarea in zip(mintareas, maxtareas):
    url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&maxtarea={maxtarea}&mintarea={mintarea}&object_type%5B0%5D=1&offer_type=flat&p={page}&region=1'.format(
        maxtarea=maxtarea,
        mintarea=mintarea,
        page=1
    )
    url = url.replace('p=1', 'p={}')
    print('parsing from', mintarea, 'to', maxtarea)
    whole_parsed_count, whole_saved_count, whole_count = parser.parse(url, whole_parsed_count, whole_saved_count,
                                                                      whole_count)
    print()
    time.sleep(10)

# res = parser.parse_flat_info('https://www.cian.ru/sale/flat/220934355/')
# print(res)
# parser.save_to_db(res)

# res = requests.get('https://www.cian.ru/kupit-kvartiru-1-komn-ili-2-komn/')
# print(res.cookies.__dict__)
# jar = requests.cookies.RequestsCookieJar()


# res = parser.parse_flat_info('http://0s.o53xo.mnuwc3rooj2q.nblz.ru/sale/flat/220934355/')
# print(res)
# parser.save_to_db(res)
# sys.stdout = orig_stdout
# f.close()


# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# import time
#
# req_proxy = RequestProxy()
#
# test_url = 'https://www.cian.ru'
# try:
#     request = req_proxy.generate_proxied_request(test_url)
#     print(request.text)
#     print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
# except:
#     print('fail')
#
# try:
#     request = req_proxy.generate_proxied_request(test_url)
#     print(request.text)
#     print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
# except:
#     print('fail')
#
# try:
#     request = req_proxy.generate_proxied_request(test_url)
#     print(request.text)
#     print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
# except:
#     print('fail')
#
# try:
#     request = req_proxy.generate_proxied_request(test_url)
#     print(request.text)
#     print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
# except:
#     print('fail')
#
# try:
#     request = req_proxy.generate_proxied_request(test_url)
#     print(request.text)
#     print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
# except:
#     print('fail')
# request = req_proxy.generate_proxied_request(test_url)
# print(request.__dict__)
# print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))
#
# request = req_proxy.generate_proxied_request(test_url)
# print(request.__dict__)
# print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))

# url = 'https://www.cian.ru'
# # s = requests.Session()
# proxies = {
#     'http': 'http://85.143.66.138:8080'
# }
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'
#     }
#
# # response = requests.get(url, headers=headers, proxies=proxies)
# response = requests.get(url, proxies=proxies, headers=headers)
# print(response.text)


# r = ProxyRequests("https://toster.ru/q/246483")
# response = r.get()
#
# print(r)


# import urllib.request
# page = urllib.request.urlopen('https://www.cian.ru/')
# print(page.read())
#
# from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup
# url = 'https://www.cian.ru/'
# req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()
# print(webpage)
#
#
# b'<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<title>Captcha - \xd0\xb1\xd0\xb0\xd0\xb7\xd0\xb0 \xd0\xbe\xd0\xb1\xd1\x8a\xd1\x8f\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\xa6\xd0\x98\xd0\x90\xd0\x9d</title>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex" />\n<style>\nhtml {\nbackground: #F4F4F4;\nheight: 100%;\n}\nbody {\nfont-family: Verdana, Tahoma, Arial, sans-serif;\nheight: 100%;\n}\nmain {\nbackground: #FFFFFF;\nborder: 1px solid #E8E8E8;\nborder-radius: 3px;\n}\nmain > img {\ndisplay: block;\n}\n@media (min-width: 704px) {\nbody {\npadding: 0 20px;\nmin-width: 704px;\nmax-width: 1376px;\nmin-height: 625px;\nmargin: 0 auto;\nbox-sizing: border-box;\ndisplay: flex;\nalign-items: center;\njustify-content: center;\n}\nmain {\nmargin-left: 8.333333333%;\nmargin-right: 8.333333333%;\nwidth: 100%;\npadding-bottom: 35px;\n}\nmain > * {\nmargin-left: 10.15%;\nmargin-right: 10.15%;\n}\nmain > img {\nmargin-top: 35px;\nmargin-bottom: 35px;\nposition: relative;\nleft: -34px;\n}\n}\n@media (max-width: 703px) {\nbody {\nmargin: 0;\npadding: 20px 15px;\nbox-sizing: border-box;\nmin-width: 320px;\n}\nmain {\nheight: 94%;\nheight: 100%;\nbox-sizing: border-box;\nmin-height: 515px;\npadding-bottom: 20px;\n}\nmain > * {\nmargin-left: 30px;\nmargin-right: 30px;\n}\nmain > img {\nmargin-top: 20px;\nmargin-bottom: 20px;\nwidth: 170px;\nposition: relative;\nleft: -15px;\n}\n}\n</style>\n<script type="text/javascript">\nvar onloadCaptcha= function(){\ngrecaptcha.render(\'captcha\', { \'sitekey\': \'6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_\', \'callback\': setCookie });\n};\nvar setCookie = function(resp){\nvar form = document.getElementById(\'form_captcha\');\nvar input = document.createElement(\'input\');\ninput.type = \'hidden\';\ninput.name = \'redirect_url\';\ninput.value = location.search.split(\'redirect_url=\').splice(1).join(\'\');\nform.appendChild(input);\nform.submit();\n};\n</script>\n<script src="https://www.google.com/recaptcha/api.js?onload=onloadCaptcha&render=explicit" async defer></script>\n<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\nnew Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n\'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n})(window,document,\'script\',\'dataLayer\',\'GTM-KC2KW5\');</script>\n<!-- End Google Tag Manager -->\n</head>\n<body>\n<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KC2KW5"\nheight="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n<main>\n<img src="data:image/gif;base64,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" alt="\xd0\x91\xd0\xb0\xd0\xb7\xd0\xb0 \xd0\xbe\xd0\xb1\xd1\x8a\xd1\x8f\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\xa6\xd0\x98\xd0\x90\xd0\x9d">\n<form method=post action="" id="form_captcha">\n<div id="captcha"></div>\n</form>\n</main>\n</body>\n</html>\n'

# from selenium import webdriver
# driver = webdriver.PhantomJS()

# from selenium import webdriver
# # import chromedriver_binary
#
# # from phantomjs_bin import executable_path
# # print(executable_path)
# # driver = webdriver.PhantomJS(executable_path="/Users/egor/PycharmProjects/phantomjs")
# driver = webdriver.Chrome(executable_path="/Users/egor/PycharmProjects/chromedriver")

# driver.get('https://www.cian.ru/')
# print(driver.page_source)
# print('ok')
# time.sleep(10)
# print('ok')
# print(driver.page_source)
# print('ok')
# p_element = driver.find_element_by_id(id_='g-recaptcha-response')
# print(p_element.text)

# from requests_html import HTMLSession
# session = HTMLSession()
#
# r = session.get('https://www.cian.ru/')
#
# print(r.text)


# session = HTMLSession()
# r = session.get('http://results.neptron.se/#/lundaloppet2018/?sortOrder=Place&raceId=99&page=0&pageSize=25')
# r.html.render()
# table = r.html.find('table', first=True)
#
# print(table.html)

src="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&hl=ru&v=75nbHAdFrusJCwoMVGTXoHoM&size=normal&cb=3pvs6x7ozq9v"
src="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&hl=ru&v=75nbHAdFrusJCwoMVGTXoHoM&size=normal&cb=h6j28iu1sqo4"
src="https://www.google.com/recaptcha/api2/anchor?ar=1;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=rxyf3i5kdhfd"
src="https://www.google.com/recaptcha/api2/anchor?ar=;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=fhz1ozckdbbr"
src="https://www.google.com/recaptcha/api2/anchor?ar=1&amp;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=dx6a1hyrh5lo"