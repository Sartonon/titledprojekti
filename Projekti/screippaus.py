from decimal import Decimal
from selenium import webdriver
import simplejson

def screippaa():
    listassa = {}
    browser = webdriver.Firefox()
    browser.get('https://korppi.jyu.fi/openid/manage/endpoint?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.identity=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.return_to=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.realm=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.assoc_handle=1439986517853-17587&openid.mode=checkid_setup&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fsreg%2F1.0&openid.sreg.optional=email%2Cfullname')
    browser.implicitly_wait(10)

    browser.get('https://korppi.jyu.fi/kotka/reservation/searchSpace.jsp?code=&submitSearch=Hae&officialOnly=true&mapOnly=true')
    global linkit
    linkit = browser.find_elements_by_link_text('Kartta') #browser.find_elements_by_link_text('Rakennus') or browser.find_elements_by_link_text('Kartta')  #((By.id("foo"),By.name("bar")));# browser.find_elements_by_link_text('Kartta')
    for linkki in range(1, len(linkit)):
        linkit = browser.find_elements_by_link_text('Kartta')
        linkit[linkki].click()
        browser.implicitly_wait(3)
        lat = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('=')[1].split(',')[0]
        lon = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('=')[1].split('+')[1]
        paikka = browser.find_element_by_link_text('[Google Maps]').get_attribute('href').split('(')[1].split(')')[0].replace('+', ' ')
        print('lat: ' + lat + '  lon: ' + lon + '  paikka: ' + paikka)
        listassa.__setitem__(paikka, {'lat': Decimal(lat), 'lon': Decimal(lon)})
        browser.back()
        browser.implicitly_wait(3)
    print(listassa)
    simplejson.dump(listassa, open('paikat.py', 'w'))

screippaa()
