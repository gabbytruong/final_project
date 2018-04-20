#Gabby Truong - Final Project - SI206

import json
from bs4 import BeautifulSoup
import unittest
import requests
import secrets
from yelpapi import YelpAPI
import sqlite3 as sqlite
#import plotly.plotly as py
#import plotly.graph_objs as go


yelp_api = YelpAPI(secrets.API_KEY)


#CACHE FOR NETSTATE
NETSTATE_CACHE = 'netstate_cache.json'

try:
    cache_file_3 = open(NETSTATE_CACHE, 'r')
    cache_contents_3 = cache_file_3.read()
    CACHE_DICT_3 = json.loads(cache_contents_3)
    cache_file_3.close()
except:
    CACHE_DICT_3 = {}

def get_cached_netstate(baseurl):
    unique_ident = baseurl
    if unique_ident in CACHE_DICT_3.keys():
        return CACHE_DICT_3[unique_ident]
    else:
        resp = requests.get(baseurl)
        CACHE_DICT_3[unique_ident] = resp.text
        f = open(NETSTATE_CACHE, 'w')
        dumped_json = json.dumps(CACHE_DICT_3)
        f.write(dumped_json)
        f.close()
        return CACHE_DICT_3[unique_ident]


#initial prompt
user_inp = input('Enter a state abbreviation (or "help" for a list of states): ')

#adds help option if needed
if user_inp == 'help':
     print('Please enter one of the following state abbreviations:')
     print('ak for Alaska')
     print('al for Alabama')
     print('ar for Arkansas')
     print('az for Arizona')
     print('ca for California')
     print('co for Colorado')
     print('ct for Connecticut')
     print('de for Delaware')
     print('fl for Florida')
     print('ga for Georgia')
     print('hi for Hawaii')
     print('ia for Iowa')
     print('id for Idaho')
     print('il for Illinois')
     print('in for Indiana')
     print('ks for Kansas')
     print('ky for Kentucky')
     print('la for Louisiana')
     print('ma for Massachusetts')
     print('md for Maryland')
     print('me for Maine')
     print('mi for Michigan')
     print('mn for Minnesota')
     print('mo for Missouri')
     print('ms for Mississippi')
     print('mt for Montana')
     print('nc for North Carolina')
     print('nd for North Dakota')
     print('ne for Nebraska')
     print('nh for New Hampshire')
     print('nj for New Jersey')
     print('nm for New Mexico')
     print('nv for Nevada')
     print('ny for New York')
     print('oh for Ohio')
     print('ok for Oklahoma')
     print('or for Oregon')
     print('pa for Pennsylvania')
     print('ri for Rhode Island')
     print('sc for South Carolina')
     print('sd for South Dakota')
     print('tn for Tennessee')
     print('tx for Texas')
     print('ut for Utah')
     print('va for Virginia')
     print('vt for Vermont')
     print('wa for Washington')
     print('wi for Wisconsin')
     print('wv for West Virginia')
     print('wy for Wyoming')
     user_inp = input('Enter a state abbreviation: ')

#create class
class NetState:
    def __init__(self, state_abbr='No state', city='No city',
    population ='No population', baseurl=None):

        self.state_abbr = state_abbr
        self.baseurl = baseurl

        if baseurl is None:
            self.city = city
            self.population = population

        else:
            self.ns_info(baseurl)

    def __str__(self):
        return '{}, {}: {}'.format(city, state_abbr, population)

    def ns_info(self, baseurl):
        baseurl = 'http://www.netstate.com/states/alma/{}_alma.htm'.format(self.state_abbr)
        html = get_cached_netstate(baseurl)
        soup = BeautifulSoup(html, 'html.parser')

        symbol_table =soup.find(id='symboltable')
        my_table = symbol_table.find('table')
        inner_table = my_table.find('table')
        tr = inner_table.find_all('tr')[0]
        td = tr.find_all('td')
        try:
            self.city = td[1].string
        except:
            self.city = 'No city'
        try:
            self.population = td[2].string
        except:
            self.population = 'No city'

print(' ')

#GET NETSTATE DATA
def get_netstate_data(user_inp):
    baseurl = 'http://www.netstate.com/states/alma/{}_alma.htm'.format(user_inp)
    html = get_cached_netstate(baseurl)
    soup = BeautifulSoup(html, 'html.parser')
    container =soup.find(id='container')
    my_table = container.find('table')
    inner_table = my_table.find('table')
    tr = inner_table.find_all('tr')[0]
    td = tr.find_all('td')
    city = td[1].string
    population = td[2].string

    loc = NetState(city = city, population = population, state_abbr = user_inp)

    print(city + ', ' + user_inp.upper() + ': population of ' + population)
    return (city, user_inp)

get_netstate_data(user_inp) #prints result string


#YELP CACHE - FOOD
def get_restaurants(user_inp):
    city = get_netstate_data(user_inp)
    search_results = yelp_api.search_query(term = 'Restaurant',
    location = str(city) + ', ' + str(user_inp.upper()))
    with open('yelp_cache.json', 'w') as CACHE_DICT:
        json.dump(search_results, CACHE_DICT)

    with open('yelp_cache.json') as json_data: # read the cached file and save it as a json object i can work with
        cached_file = json.load(json_data)

    for x in range(0, 5):
        rating = cached_file["businesses"][x]["rating"]
        try:
            price = cached_file["businesses"][x]["price"]
        except:
            price = "No price range available."
        review_num = cached_file["businesses"][x]["review_count"]
        name = cached_file["businesses"][x]["alias"]
        loc = cached_file["businesses"][x]["location"]["display_address"]
        print('------------------- Restaurant -------------------')
        print(name.replace('-', ' ').upper() + ' ' + str(loc))
        print('Rating: ' + str(rating))
        print('Number of reviews: ' + str(review_num))
        print('Price range: ' + str(price))
        print('')


#YELP CACHE - HOTELS
def get_hotels(user_inp):
    city = get_netstate_data(user_inp)
    search_results_2 = yelp_api.search_query(term = 'Hotels',
    location = str(city) + ', ' + str(user_inp.upper()))

    with open('yelp_cache_2.json', 'w') as CACHE_DICT_2:
        json.dump(search_results_2, CACHE_DICT_2)

    with open('yelp_cache_2.json') as json_data_2:
        cached_file_2 = json.load(json_data_2)

    for x in range(0, 5):
        rating = cached_file_2["businesses"][x]["rating"]
        try:
            price = cached_file["businesses"][x]["price"]
        except:
            price = "No price range available."
        review_num = cached_file_2["businesses"][x]["review_count"]
        name = cached_file_2["businesses"][x]["alias"]
        loc = cached_file_2["businesses"][x]["location"]["display_address"]
        print('--------------------- Hotel ----------------------')
        print(name.replace('-', ' ').upper() + ' ' + str(loc)) #if i have time, replace the [ ]
        print('Rating: ' + str(rating))
        print('Number of reviews: ' + str(review_num))
        print('Price range: ' + str(price))
        print('')

#second prompt
user_inp_2 = input('To view restaurant and hotel reccomendations, enter "yes". To exit, enter "exit": ')
if user_inp_2 == 'yes':
    get_restaurants(user_inp)
    get_hotels(user_inp)
else:
    exit()

#

def pop_db():
    state_dict = {
            'ak': 'Alaska',
            'al': 'Alabama',
            'ar': 'Arkansas',
            'az': 'Arizona',
            'ca': 'California',
            'co': 'Colorado',
            'ct': 'Connecticut',
            'de': 'Delaware',
            'fl': 'Florida',
            'ga': 'Georgia',
            'hi': 'Hawaii',
            'ia': 'Iowa',
            'id': 'Idaho',
            'il': 'Illinois',
            'in': 'Indiana',
            'ks': 'Kansas',
            'ky': 'Kentucky',
            'la': 'Louisiana',
            'ma': 'Massachusetts',
            'md': 'Maryland',
            'me': 'Maine',
            'mi': 'Michigan',
            'mn': 'Minnesota',
            'mo': 'Missouri',
            'ms': 'Mississippi',
            'mt': 'Montana',
            'nc': 'North Carolina',
            'nd': 'North Dakota',
            'ne': 'Nebraska',
            'nh': 'New Hampshire',
            'nj': 'New Jersey',
            'nm': 'New Mexico',
            'nv': 'Nevada',
            'ny': 'New York',
            'oh': 'Ohio',
            'ok': 'Oklahoma',
            'or': 'Oregon',
            'pa': 'Pennsylvania',
            'ri': 'Rhode Island',
            'sc': 'South Carolina',
            'sd': 'South Dakota',
            'tn': 'Tennessee',
            'tx': 'Texas',
            'ut': 'Utah',
            'va': 'Virginia',
            'vt': 'Vermont',
            'wa': 'Washington',
            'wi': 'Wisconsin',
            'wv': 'West Virginia',
            'wy': 'Wyoming'
    }

    city_data_lst = []
    for state in state_dict.keys():
        state_info = get_netstate_data(user_inp =state)
        city_data_lst.append(state_info)
    return city_data_lst
    print(city_data_lst)
pop_db()

#create database with two tables:
#table 'Cities' - city (w/ID), state, population (50 of them)
#table 'YelpResults' - city (w/ID), restaurant[0], hotel[0], price, rating, review #

DBNAME = 'cities.db'

def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Cities';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'YelpResults';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Cities' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'City' TEXT NOT NULL,
            'State' TEXT NOT NULL,
            'Population' INTEGER

        );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'YelpResults' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'City' TEXT NOT NULL,
            'State' TEXT NOT NULL,
            'Search Category' TEXT NOT NULL,
            'Rating' INTEGER NOT NULL,
            'Price' INTEGER NOT NULL,
            'Reviews' INTEGER NOT NULL
        );
    '''

    cur.execute(statement)
    conn.commit()
    conn.close()


# def populate_cities():
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()
#
#     f = open(NETSTATE_CACHE, 'r')
#     contents = f.read()
#     city_data = json.loads(contents)
#     cities_dict = {}
#     counter = 1
#     for c in city_data:
#         if
#
#
#     conn.commit()


 #explain to GSI only need it once


#plotly

#virtualenv


#call function at the bottom

if __name__ == "__main__":
		unittest.main(verbosity=2)

# if __name__ == '__main__':
#     unittest.main()
#
# if __name__=="__main__":
#     interactive_prompt()
