import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import base64
import configparser
import codecs
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
config.readfp(codecs.open("settings.ini", "r", "utf8"))
#config.read('settings.ini').decode('utf8')
# #-------------

sleepTime = 0.3 #300 ms delay time
from_IataCode = config.get("DEFAULT", "from_IataCode")
to_IataCode = config.get("DEFAULT", "to_IataCode")
checkLowerThan = config.get("DEFAULT", "checkLowerThan")
chromeDriverPath = config.get("DEFAULT", "chromeDriverPath")
#-------------
if checkLowerThan == "YES":
    lowerThan = int(config.get("DEFAULT", "lowerThan"))
else:
    lowerThan = 0
#-------------
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)  # Optional argument, if not specified will search path.
    return driver
#-------------
def select_flight_params(driver,sleepTime,startPlace, to, elems, elementCounter, lowerThan):
        time.sleep(sleepTime)
        field = driver.find_element_by_xpath('//*[@id="airtickets-form"]/div[1]/div[1]/input')
        field.clear()
        field.send_keys(startPlace)
        time.sleep(sleepTime)
        field = driver.find_element_by_xpath('//*[@id="airtickets-form"]/div[2]/div[1]/input')
        field.clear()
        if to == "ALL":
            field.send_keys(elems[elementCounter])
            endPlace = str(elems[elementCounter])
        else:
            field.send_keys(to)
            endPlace = str(to)
        time.sleep(sleepTime)
        button = driver.find_element_by_xpath('//*[@id="airtickets-form"]/div[11]/button')
        button.click()
        time.sleep(sleepTime)
        try:
            price = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li/div[2]/div[3]/div[2]').text
            route = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li[1]/div[2]/div[3]/div[1]').text
            dates = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li[1]/div[2]/div[4]').text
            if lowerThan > 0:
                if int(price[:-3].replace(" ", "")) < lowerThan:
                    print("Tickets from ", startPlace, " to ", endPlace, ":")
                    print(route, "\n", dates, "\n", price[:-3].replace(" ", ""), " РУБ")
            elif lowerThan == 0:
                if int(price[:-3].replace(" ", "")) > 0:
                    print("Tickets from ", startPlace, " to ", endPlace, ":")
                    print(route, "\n", dates, "\n", price[:-3].replace(" ", ""), " РУБ")
            else:
                print("Tickets from ", startPlace, " to ", endPlace, ":")
                print(route, "\n", dates, "\n", price[:-3].replace(" ", ""), " РУБ")
        except NoSuchElementException:
            print("No tickets available from ", startPlace, " to ", endPlace, "!")


def genMass(driver,sleepTime):
    
    a = []
    #1 столбец
        #A
    for h in range(2,4):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(1,1,h)
        a.append(text)
        h += 1
        #Б
    for h in range(2,4):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(1,2,h)
        a.append(text)
        h += 1
            #В
    for h in range(2,5):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(1,3,h)
        a.append(text)
        h += 1
        #G
    for h in range(2,3):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(1,4,h)
        a.append(text)
        h += 1
            #E
    for h in range(2,4):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(1,5,h)
        a.append(text)
        h += 1
#2 столбец
        
    for h in range(2,8):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(2,1,h)
        a.append(text)
        h += 1
    for h in range(2,3):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(2,2,h)
        a.append(text)
        h += 1
    for h in range(2,8):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(2,3,h)
        a.append(text)
        h += 1
    for h in range(2,5):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(2,4,h)
        a.append(text)
        h += 1
        
        #3 столбец
    for h in range(2,4):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,1,h)
        a.append(text)
        h += 1
    for h in range(2,3):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,2,h)
        a.append(text)
        h += 1
    for h in range(2,8):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,3,h)
        a.append(text)
        h += 1
    for h in range(2,5):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,4,h)
        a.append(text)
        h += 1
    for h in range(2,3):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,5,h)
        a.append(text)
        h += 1        
    for h in range(2,3):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,6,h)
        a.append(text)
        h += 1
    for h in range(2,4):
        text = ('//*[@id="airtickets-form"]/div[1]/div[2]/div/div[{0}]/div[{1}]/div[{2}]').format(3,7,h)
        a.append(text)
        h += 1
    driver.get('https://www.pobeda.aero/information/book/search_cheap_tickets')
    time.sleep(sleepTime)
    elems = []
    try:
        for i in range(len(a)):
            elem = driver.find_element_by_xpath(a[i]).get_attribute("data-iata")
            elems.append(elem)
            #print("iata code(1 from): ", elem)
            #print(elem)
    except NoSuchElementException:
        print("NoSuchElementException")
    return elems


#-------------------------------

if __name__ == "__main__":
    elems = []
    driver = init_driver()
    elems = genMass(driver,sleepTime)
    if to_IataCode == "ALL":
        for i in range(len(elems)):
            if from_IataCode != elems[i]:
                select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, elems, i, lowerThan)
    elif from_IataCode != to_IataCode:
        select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, elems, 0, lowerThan)
    driver.quit()


# while not msvcrt.kbhit():   # не нажата ли клавиша?
#     pass

