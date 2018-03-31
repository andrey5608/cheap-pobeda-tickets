import time
from selenium import webdriver
import configparser
import codecs
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

config = configparser.ConfigParser()
config.readfp(codecs.open("settings.ini", "r", "utf8"))

sleepTime = 0.5 #300 ms delay time
from_IataCode = config.get("DEFAULT", "from_IataCode")
to_IataCode = config.get("DEFAULT", "to_IataCode")
checkLowerThan = config.get("DEFAULT", "checkLowerThan")
chromeDriverPath = config.get("DEFAULT", "chromeDriverPath")
mode = config.get("DEFAULT", "mode")
link = config.get("DEFAULT", "link")

if checkLowerThan.lower() == "yes":
    lowerThan = int(config.get("DEFAULT", "lowerThan"))
else:
    lowerThan = 0


def init_driver(mode):
    options = webdriver.ChromeOptions()
    if mode.lower() == 'maximized':
        print(mode.lower(), 'mode')
        options.add_argument("--start-maximized")
    elif mode.lower() == 'headless':
        print(mode.lower(), 'mode')
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    else:
        print(mode.lower(), 'mode')
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)  # Optional argument, if not specified will search path.
    return driver



def select_flight_params(driver,sleepTime,startPlace, to, elems, elementCounter, lowerThan, sendStartPlaceOnce):
        time.sleep(sleepTime)
        field = driver.find_element_by_xpath('//*[@id="airtickets-form"]/div[1]/div[1]/input')
        if sendStartPlaceOnce and elementCounter != 0:
            time.sleep(sleepTime)
        else:
            field.clear()
            field.send_keys(startPlace)
            time.sleep(sleepTime)
        field = driver.find_element_by_xpath('//*[@id="airtickets-form"]/div[2]/div[1]/input')
        field.clear()
        if to.lower() == "all":
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
             if len(elems) == 1:
                 print("No tickets available from ", startPlace, " to ", endPlace, "!")
        except StaleElementReferenceException:
            if len(elems) == 1:
                print("No tickets available from ", startPlace, " to ", endPlace, "!")



def genMass(driver, sleepTime):
    time.sleep(sleepTime)
    elems = []
    first_iata_code = ''
    try:
        countriesList = driver.find_elements_by_class_name('form-dropoutList__item')
        for country in range(len(countriesList)):
            iataCode = countriesList[country].get_attribute("data-iata")
            if iataCode:
                if iataCode == first_iata_code:
                    return elems
                if country == 0:
                    first_iata_code = iataCode
                elems.append(iataCode)

    except NoSuchElementException:
        print("NoSuchElementException")



if __name__ == "__main__":
    elems = []
    if mode.lower() == 'debug':
        debug = True
    else:
        debug = False
    driver = init_driver(mode)
    driver.get(link)
    if to_IataCode.lower() == "all":
        elems = genMass(driver, sleepTime)
        for i in range(len(elems)):
            if debug:
                print(elems[i])
            if from_IataCode != elems[i]:
                select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, elems, i, lowerThan, True)
    elif from_IataCode != to_IataCode:
        select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, '1', 0, lowerThan, False)
    driver.quit()
# while not msvcrt.kbhit():   # не нажата ли клавиша?
