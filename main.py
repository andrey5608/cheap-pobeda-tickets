import time
from selenium import webdriver
import configparser
import codecs
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
config.read_file(codecs.open("settings.ini", "r", "utf8"))

sleepTime = 0.3  # webdriver delay time
from_IataCode = config.get("DEFAULT", "from_IataCode")
to_IataCode = config.get("DEFAULT", "to_IataCode")
checkLowerThan = config.get("DEFAULT", "checkLowerThan")
chromeDriverPath = config.get("DEFAULT", "chromeDriverPath")
link = config.get("DEFAULT", "link")
iata_codes_xpath = config.get("DEFAULT", "iata_codes_xpath")

if checkLowerThan == "YES":
    lowerThan = int(config.get("DEFAULT", "lowerThan"))
else:
    lowerThan = 0


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(chromeDriverPath, chrome_options=options)


def select_flight_params(driver, sleepTime, startPlace, to, elems, elementCounter, lowerThan):
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
        price_text = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li/div[2]/div[3]/div[2]').text
        route = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li[1]/div[2]/div[3]/div[1]').text
        dates = driver.find_element_by_xpath('//*[@id="airtickets-wrapper"]/ul/li[1]/div[2]/div[4]').text
        price = price_text[:-3].replace(" ", "") if len(price_text) >= 3 else "None"
        price = try_parse_int(price)

        if lowerThan > 0 and lowerThan > price:
            print("Tickets from ", startPlace, " to ", endPlace, ":")
            print(route, "\n", dates, "\n", price, " РУБ")
        elif lowerThan == 0 and price > 0:
            print("Tickets from ", startPlace, " to ", endPlace, ":")
            print(route, "\n", dates, "\n", price, " РУБ")
    except NoSuchElementException:
        print("No tickets available from ", startPlace, " to ", endPlace, "!")


def try_parse_int(number):
    parsed_int = ignore_exception(ValueError)(int)
    return parsed_int(number)


def ignore_exception(exception=Exception, default_val=None):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return default_val

        return wrapper

    return decorator


def get_massive(driver):
    iata_codes = []
    try:
        elems = driver.find_elements_by_xpath("//div[@class='header-form__item _white' "
                                              "and contains(normalize-space(),'Город вылета')]/descendant::div"
                                              "[@class='form-dropoutList__item' and @data-iata]")
        for i in range(len(elems)):
            iata_code = elems[i].get_attribute("data-iata")
            iata_codes.append(iata_code)
            print("iata code(1 from ", i, "): ", iata_code)
        return iata_codes
    except NoSuchElementException:
        print("NoSuchElementException")


if __name__ == "__main__":
    driver = init_driver()
    driver.get(link)
    if to_IataCode == "ALL":
        elems = get_massive(driver)
        for i in range(len(elems)):
            if from_IataCode != elems[i]:
                select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, elems, i, lowerThan)
    elif from_IataCode != to_IataCode:
        select_flight_params(driver, sleepTime, from_IataCode, to_IataCode, None, 0, lowerThan)
    driver.quit()
