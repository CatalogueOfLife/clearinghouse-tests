from selenium.common.exceptions import NoSuchElementException


def test_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def test_exists_by_css_selector(browser, css):
    try:
        browser.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


def test_exists_by_element_id(browser, element_id):
    try:
        browser.find_by_element_id(element_id)
    except NoSuchElementException:
        return False
    return True


