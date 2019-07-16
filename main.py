import time
from selenium import webdriver
import configparser
import codecs
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
config.read_file(codecs.open("settings.ini", "r", "utf8"))

sleep_time = 0.3  # webdriver delay time
from_IataCode = config.get("DEFAULT", "from_IataCode")
to_IataCode = config.get("DEFAULT", "to_IataCode")
checkLowerThan = config.get("DEFAULT", "checkLowerThan")
chromeDriverPath = config.get("DEFAULT", "chromeDriverPath")
link = config.get("DEFAULT", "link")

from_field_xpath = "//label[normalize-space()='Город вылета']/following-sibling::div[@class='form-customSelect']/input"
to_field_xpath = "//label[normalize-space()='Город прилёта']/following-sibling::div[@class='form-customSelect']/input"
find_button_xpath = "//form[@id='airtickets-form']/descendant::button[normalize-space()='Найти билеты']"
price_block_xpath = "//div[@id='airtickets-wrapper']/descendant::div[@class='airtickets-cost'][1]"
route_block_xpath = "//div[@id='airtickets-wrapper']/descendant::div[@class='airtickets-cities'][1]"
dates_block_xpath = "//div[@id='airtickets-wrapper']/descendant::div[@class='airtickets-date'][1]"
airport_codes_xpath = "//div[@class='header-form__item _white' and contains(normalize-space(),'Город вылета')]" \
                      "/descendant::div[@class='form-dropoutList__item' and @data-iata]"


if checkLowerThan == "YES":
    lowerThan = int(config.get("DEFAULT", "lowerThan"))
else:
    lowerThan = 0


def init_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    return webdriver.Chrome(chromeDriverPath, chrome_options=options)


def select_flight_params(driver, sleep_time, start_place, to, elems, element_counter, lower_than):
    time.sleep(sleep_time)
    from_field = driver.find_element_by_xpath(from_field_xpath)
    from_field.clear()
    from_field.send_keys(start_place)
    time.sleep(sleep_time)
    to_field = driver.find_element_by_xpath(to_field_xpath)
    to_field.clear()
    if to == "ALL":
        to_field.send_keys(elems[element_counter])
        end_place = str(elems[element_counter])
    else:
        to_field.send_keys(to)
        end_place = str(to)
    time.sleep(sleep_time)
    find_button = driver.find_element_by_xpath(find_button_xpath)
    find_button.click()
    time.sleep(sleep_time)
    try:
        price_text = driver.find_element_by_xpath(price_block_xpath).text # TODO: get all prices from the page
        route_text = driver.find_element_by_xpath(route_block_xpath).text
        dates_text = driver.find_element_by_xpath(dates_block_xpath).text
        price = price_text.replace("руб", "").replace(" ", "") if len(price_text) >= 3 else "None"
        price = try_parse_int(price)

        if lower_than > 0 and lower_than > price:
            print("Tickets from ", start_place, " to ", end_place, ":")
            print(route_text, "\n", dates_text, "\n", price, " РУБ")
        elif lower_than == 0 and price > 0:
            print("Tickets from ", start_place, " to ", end_place, ":")
            print(route_text, "\n", dates_text, "\n", price, " РУБ")
    except NoSuchElementException:
        print("No tickets available from ", start_place, " to ", end_place, "!")


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
        elems = driver.find_elements_by_xpath(airport_codes_xpath)
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
                select_flight_params(driver, sleep_time, from_IataCode, to_IataCode, elems, i, lowerThan)
    elif from_IataCode != to_IataCode:
        select_flight_params(driver, sleep_time, from_IataCode, to_IataCode, None, 0, lowerThan)
    driver.quit()