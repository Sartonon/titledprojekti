# Copyright 2016  Jose Malmberg, Toni Pitkänen, Santeri Rusila, Markus Valkama
#
#
# This file is part of Karttakotka.
#
# Karttakotka is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Karttakotka is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Karttakotka.  If not, see <http://www.gnu.org/licenses/>.

from decimal import Decimal
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import simplejson

def screippaa():
    listassa = {}
    browser = webdriver.Firefox()
    browser.get('https://korppi.jyu.fi/openid/manage/endpoint?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.identity=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.return_to=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.realm=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.assoc_handle=1439986517853-17587&openid.mode=checkid_setup&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fsreg%2F1.0&openid.sreg.optional=email%2Cfullname')
    browser.implicitly_wait(10)

    browser.get('https://korppi.jyu.fi/kotka/reservation/searchSpace.jsp')
    browser.implicitly_wait(100)

    global linkit
    linkit = browser.find_elements_by_link_text('Kartta') #browser.find_elements_by_link_text('Rakennus') or browser.find_elements_by_link_text('Kartta')  #((By.id("foo"),By.name("bar")));# browser.find_elements_by_link_text('Kartta')
    for linkki in range(1, len(linkit)):
        linkit = browser.find_elements_by_link_text('Kartta')
        linkit[linkki].click()
        browser.implicitly_wait(3)
        try:
            lat = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('=')[1].split(',')[0]
            lon = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('=')[1].split('+')[1]
            paikka = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('(')[1].split(')')[0].replace('+', ' ')
            print('lat: ' + lat + '  lon: ' + lon + '  paikka: ' + paikka)
            listassa.__setitem__(paikka, {'lat': Decimal(lat), 'lon': Decimal(lon)})
        except:
            pass
        browser.back()
        browser.implicitly_wait(3)
    print(listassa)
    simplejson.dump(listassa, open('paikat.py', 'w'))

screippaa()
