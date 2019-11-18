import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# import time
import psycopg2
# import sys
import time
# from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
from selenium import webdriver


# orig_stdout = sys.stdout
# f = open('out.txt', 'a')
# sys.stdout = f
# driver = webdriver.Chrome(executable_path="/Users/egor/PycharmProjects/chromedriver")

class CianParser():
    # s = requests.Session()
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language': 'en-en,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Connection': 'keep-close',
    # }
    driver = webdriver.Chrome(executable_path="/Users/egor/PycharmProjects/chromedriver")

    # proxies = ['95.79.36.55:44861', '213.110.230.247:8080', '109.170.96.26:8080', '193.9.245.199:8080',
    #            '77.236.251.234:8080', '92.53.124.209:3128', '85.143.66.138:8080', '85.143.254.20:8080',
    #            '91.230.11.164:8080', '82.147.120.32:35542', '94.141.60.69:8080', '37.230.147.206:8080',
    #            '212.33.28.51:8080',
    #            '195.62.70.22:8080', '188.128.63.210:8080', '217.145.150.19:42191', '212.220.1.38:8080',
    #            '89.22.132.57:8080',
    #            '95.138.228.28:8080', '77.246.237.230:80', '62.33.207.196:3128', '37.235.65.76:8080',
    #            '185.87.50.49:3128',
    #            '95.167.150.166:49464', '85.173.165.36:46330']
    # proxy_number = 0
    # cookies = {
    #     'VID': '14Z1s204aa1t00000D0Q54Xt::48707187:0-0-2829259-0:',
    #     'IDE': 'AHWqTUnhVBkv_NdiHLOPgnDkFFVeLjDpqjQTaPAQOaJyhgC8pLIyJkp0OD-_i8Tt',
    #     '__zzat140': 'MDA0dBA=Fz2+aQ==',
    #     '_CIAN_GK': '9ef1db87-bc4c-44b0-9ae2-cdda7342da7f',
    #     '_cmg_csst8yrRI': '1573137226',
    #     '_comagic_id8yrRI': '2441941911.3853297180.1573137225',
    #     '_fbp': 'fb.1.1572451342223.830816584',
    #     '_ga': 'GA1.2.171392150.1572451341',
    #     '_gcl_au': '1.1.184971591.1572451340',
    #     '_gid': 'GA1.2.972360331.1573729574',
    #     'afUserId': '19427fdc-c2b7-4f09-b377-dc520addf4c6',
    #     'af_id': '19427fdc-c2b7-4f09-b377-dc520addf4c6',
    #     'audience_serp_light': 'control',
    #     'cfids140': 'BwZsfMM4EtJEwniUuachwZWOz0xslwSGs+ZqOgSKiTM4ch58GaRmBP4IXKWg4qy+2x2ccuyyQOvo9o1i+P5wq5uMzaH7Te0nUusMU9ohdYmrzZ67xrjVUiQbYekRwyj3GnnE6LPvjW1KXMYeI/7V1+oFWXkPsxgvOgNAiQ==',
    #
    #     'cryptouid': '15020567973508632186',
    #     'cryptouid_actual': '1',
    #     'cryptouid_sign': '45275593b8390a3146f332d6cb526ef3',
    #     'cto_bundle': 'SPSrP19IaTU1dVI5QlNmTzFmRFdPNWtGdG1xeWJDZFhMUWlONGFrRno5bWsyVmNLQmtjVW8lMkZHOWxtOWp1SmxiQjFIYWZvaCUyRmZ0S01wRHl3WFZjQXB0WGwyRG5VUyUyQjREdENSanlTRFBSdXNzS2d2R2EwMVl0NXRWc3pnQXAycFJZTXVrTUZsYSUyRkFnbE5VT212MUxMcUFOTDRIUSUzRCUzRA',
    #     'cto_lwid': '70433073-00de-4f48-90ba-68d9fa6bfd60',
    #
    #     'datr': 'aOOVXcZVbleA3zPZN2Rm5sWW',
    #     'financeMark': 'd7580668-9ace-4f25-8546-12250bca474a',
    #
    #     'fingerprint': 'e4299ef1fc8c4e1d4f42e46491769ee0',
    #     'flocktory-uuid': 'b586a86b-a8a8-490f-94c2-774a7345cff6-9',
    #     'forever_region_id': '2',
    #     'forever_region_name': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
    #     'fr': '0cV5H70AsVukSfgbh..BdXU8X..F3E.1.0.BdzTUm.',
    #     'incap_ses_378_2094920': 'DjqrX74r/l+yShnm0O0+BRc1zV0AAAAAsjNYCcaxcIt6G3Eei4baOg==',
    #     'login_mro_popup': 'meow',
    #     'luid1': 'i:cgfkaei:i:cgfkaei:a',
    #     'luid1_ts': 'faawpgq:fciymmt',
    #     'p': 'rEgBAGm3GAAA',
    #
    #     # 'newobject_active': '1',
    #     # 'newobject_all': '1',
    #     # 'newobject_scount': '5',
    #     # 'pview': '2',
    #     'read_offers_compressed': 'EwRhwDghOBWBmIA',
    #     'remixdt': '0',
    #     'remixlang': '0',
    #     'remixrefkey': 'c624762e9152ba31bd',
    #     'remixscreen_depth': '24',
    #     'remixsid': 'b5aa407018c0c5575333cec63d6a61e0ccce15bf57909a94ea54d60cd86d2',
    #     'remixstid': '1147850838_502ed2e5a2c78a145c',
    #     'remixusid': 'YzZmMzYwNTc3MmFiYmRjNDM0MTc4OTI1',
    #     'sb': 'aOOVXS06ckZ8Cr6QlWoTT_oC',
    #
    #     # 'seen_pins_compressed': 'IwhME4BYDpOB2cTlIDT0gNgKzeqURFZAWhGAGZQL95MAGRp+4dbYcADmnEyA',
    #     # 'serp_registration_trigger_popup': '1',
    #     # 'serp_stalker_banner': '1',
    #     'session_main_town_region_id': '2',
    #     'session_region_id': '4588',
    #     # 'sopr_session': '27de0a2e72cc4d1e',
    #     'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    #     'tmr_detect': '0%7C1573729661057',
    #     'uid': '6bd19703-cd04-4eff-9eef-4cef26fe6c94',
    #
    #     'tildauid': '1572958412722.492619',
    #     # 'tmr_detect': '0%7C1573550238782',
    #     'uxfb_usertype': 'searcher',
    #
    #     'uxs_mig': '1',
    #     'uxs_uid': 'a80c0c20-fb2e-11e9-9ddd-07c33823a03f',
    #     'visid_incap_2094920': 'DFnzZK1SSKWpI9HYdfpSogm0uV0AAAAAQUIPAAAAAACz+QMawkB3xpw9QErHiisG'
    # }
    # s.headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    # }
    # proxies = {
    #     "http": "http://user:pass@10.10.10.10:8000"
    # }
    yand_api_token = '31a6ed51-bc46-4d1d-9ac9-e3c2e22d2628'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'
    # }
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
            coords_response = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={self.yand_api_token}&format=json&geocode={flat["address"]}',timeout=5).text
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
            self.driver.get(url)
            # response = requests.get(url, headers=self.headers, proxies={'http': 'http://' + self.proxies[self.proxy_number]}, timeout=10)
            # print('http://' + self.proxies[self.proxy_number])
            # soup = BeautifulSoup(response.text, 'lxml')
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
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



if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="/Users/egor/PycharmProjects/chromedriver")
    driver.get('https://www.cian.ru')
    print(driver.page_source)
    # parser = CianParser()
    #
    # mintareas = [i for i in range(11, 110)] + [i for i in range(110, 150, 5)] + [i for i in range(150, 200, 10)] + [i for i
    #                                                                                                                 in
    #                                                                                                                 range(
    #                                                                                                                     200,
    #                                                                                                                     250,
    #                                                                                                                     25)] + [
    #                 250, 400]
    # maxtareas = [i for i in range(11, 110)] + [i for i in range(115, 155, 5)] + [i for i in range(160, 210, 10)] + [i for i
    #                                                                                                                 in
    #                                                                                                                 range(
    #                                                                                                                     225,
    #                                                                                                                     275,
    #                                                                                                                     25)] + [
    #                 400, 3000]
    # whole_parsed_count = 0
    # whole_saved_count = 0
    # whole_count = 0
    #
    # # parser.flat_closing_check()
    # #
    # for mintarea, maxtarea in zip(mintareas, maxtareas):
    #     url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&maxtarea={maxtarea}&mintarea={mintarea}&object_type%5B0%5D=1&offer_type=flat&p={page}&region=1'.format(
    #         maxtarea=maxtarea,
    #         mintarea=mintarea,
    #         page=1
    #     )
    #     url = url.replace('p=1', 'p={}')
    #     print('parsing from', mintarea, 'to', maxtarea)
    #     whole_parsed_count, whole_saved_count, whole_count = parser.parse(url, whole_parsed_count, whole_saved_count,
    #                                                                       whole_count)
    #     print()
    #     time.sleep(10)

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

# src="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&hl=ru&v=75nbHAdFrusJCwoMVGTXoHoM&size=normal&cb=3pvs6x7ozq9v"
# src="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&hl=ru&v=75nbHAdFrusJCwoMVGTXoHoM&size=normal&cb=h6j28iu1sqo4"
# src="https://www.google.com/recaptcha/api2/anchor?ar=1;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=rxyf3i5kdhfd"
# src="https://www.google.com/recaptcha/api2/anchor?ar=;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=fhz1ozckdbbr"
# src="https://www.google.com/recaptcha/api2/anchor?ar=1&amp;k=6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_&amp;co=aHR0cHM6Ly93d3cuY2lhbi5ydTo0NDM.&amp;hl=ru&amp;v=75nbHAdFrusJCwoMVGTXoHoM&amp;size=normal&amp;cb=dx6a1hyrh5lo"
