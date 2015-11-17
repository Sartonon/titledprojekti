from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def screippaa():
    browser = webdriver.Firefox()
    browser.get("https://korppi.jyu.fi/openid/manage/endpoint?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.identity=https%3A%2F%2Fkorppi.jyu.fi%2Fopenid%2F&openid.return_to=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.realm=https%3A%2F%2Fkorppi.jyu.fi%2Fkotka%2Fservlet%2Fauthentication%2FconsumeOpenIdResult&openid.assoc_handle=1439986517853-17587&openid.mode=checkid_setup&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fsreg%2F1.0&openid.sreg.optional=email%2Cfullname")
    username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password = browser.find_element_by_id("password")
    username.send_keys("topepitk")
    password.send_keys("Jeejee123")
    browser.find_element_by_id("loginbutton").click()
    browser.get("https://korppi.jyu.fi/kotka/reservation/searchSpace.jsp?code=&submitSearch=Hae&officialOnly=true&mapOnly=true")

    td_list = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("spaceResultTable")) #TODO: klikkaa karttaa
    for td in td_list:
        if(td.text == "Kartta"):
            td.click()
screippaa()
