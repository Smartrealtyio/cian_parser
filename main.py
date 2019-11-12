import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import psycopg2
import sys


# orig_stdout = sys.stdout
# f = open('out.txt', 'w')
# sys.stdout = f

class CianParser():
    # s = requests.Session()
    cookies = {
        '__zzat140': 'MDA0dBA=Fz2+aQ==',
        '_CIAN_GK': '483bd4e5-6bea-411d-9800-ac9e83c87362',
        '_cmg_csst8yrRI': '1573547869',
        '_comagic_id8yrRI': '2441688109.3876234738.1573547868',
        '_fbp': 'fb.1.1572441633077.65162569',
        '_ga': 'GA1.2.1234808825.1572441633',
        '_gac_UA-30374201-1': '1.1573136630.Cj0KCQiAno_uBRC1ARIsAB496IWrbt90M4wtAwCfyslGBOxudlVV1qgt8SaHVTygiRqDRBK4T3edYcsaAufAEALw_wcB',
        '_gcl_au': '1.1.1806903351.1573049913',
        '_gcl_aw': 'GCL.1573136624.Cj0KCQiAno_uBRC1ARIsAB496IWrbt90M4wtAwCfyslGBOxudlVV1qgt8SaHVTygiRqDRBK4T3edYcsaAufAEALw_wcB',
        '_gid': 'GA1.2.886469788.1573454980',
        'afUserId': '21a3cc2b-19d9-44b2-a33c-66d07bf81faa',
        'audience_serp_light': 'test',
        'cfids140': 'Xl81jai19V8FNTMRNuk2Kul7ZMXnGEn7E9QiPPUD5Hsf82VdkrnHZvC69lkyaVg9GPLjN3NSwvXzUb3sRp3Ug8Zic3/rTfhvnBDsfleOq9LbU1tZ4c4f9IyfBiaJSUVI8Oc/v/38+0n32OzJR2SL74lcvzKRAJQwHiOuM6g=',
        'cto_bundle': 'p0h7tl9YMkJPJTJCNGhaUmFNaUpqakFZaE1FWFVac1B5RVRIVVhKMHZwbXlKbjlrckt2QmZzZktGNEMlMkIzTWp0TkNJV1QzRE1yM2JEM2ZhV2NEbEpzenpHdGF6bGhJOE02N3NjbUhzd2ZYQTFlcUMlMkJEZlp4SmtlMiUyRjNnUUtsSlBqck5Famty',
        'cto_lwid': '5359d483-12f9-4878-9733-3896d3e3c25c',
        'financeMark': '6a02ecc3-b87b-4329-a321-9d5ba5c1ca07',
        'finauth': 'fincian_fdd5161f-f1f8-433b-ac97-99f085b98122',
        'fingerprint': '1f8a6e2448c844da7d17ed32daeffa7d',
        'flocktory-uuid': '24e54e59-c3ef-4888-8e98-82d2a55e0aed-0',
        'hide_onboarding': '1',
        'incap_ses_378_2094920': 'Ha4BGY9VwTs+1Zzj0O0+BU9nyl0AAAAA214UC6PVlhRiQGB9kM8Alw==',
        'login_mro_popup': 'meow',
        'newobject_active': '1',
        'newobject_all': '1',
        'newobject_scount': '5',
        'pview': '2',
        'read_offers_compressed': 'EwBgnMwBxgbFBaYBGCAWKBWKInIOz7IDMsZSoW%2BmJQA',
        'seen_pins_compressed': 'IwhME4BYDpOB2cTlIDT0gNgKzeqURFZAWhGAGZQL95MAGRp+4dbYcADmnEyA',
        'serp_registration_trigger_popup': '1',
        'serp_stalker_banner': '1',
        'session_main_town_region_id': '1',
        'session_region_id': '1',
        'sopr_session': '27de0a2e72cc4d1e',
        'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
        'tildauid': '1572958412722.492619',
        'tmr_detect': '0%7C1573550238782',
        'uxfb_usertype': 'searcher',
        'uxs_mig': '1',
        'uxs_uid': '50a68880-00a0-11ea-b608-6b6bcae4d15c',
        'visid_incap_2094920': 'NkfRtAOsT4q1F6MKN0pOYB+OuV0AAAAAQUIPAAAAAAAh4pjbgUZBRZHDmDI44qaj'
    }
    # s.headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
    # }
    yand_api_token = '31a6ed51-bc46-4d1d-9ac9-e3c2e22d2628'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
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

        cur.execute("select id from buildings where address=%s;", (flat['address'],))
        is_building_exist = cur.fetchone()
        if not is_building_exist:
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
                return False

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
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.find('div', {'id': 'captcha'}):
                print('captcha... sleeping 5 minutes')
                time.sleep(5 * 60)
                self.captcha_check(url)
            else:
                # self.cookies = response.cookies
                # print(self.cookies)
                return soup
        except:
            print('connection fail... sleeping 1 minute')
            time.sleep(60)
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

        return pages_url, next_page_number

    def parse(self, url, whole_parsed_count, whole_saved_count, whole_count):
        page_number = 1
        next_page_number = 1
        count = 0
        parsed_count = 0
        saved_count = 0
        while (page_number == next_page_number):
            time.sleep(3)
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
                if whole_count%20 == 0:
                    print('sleep')
                    time.sleep(10)
                time.sleep(3)

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
            time.sleep(3)


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

parser.flat_closing_check()

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
#     time.sleep(5)

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
