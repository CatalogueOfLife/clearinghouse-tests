from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

TIMEOUT = 10  # seconds


def wait_until_element(browser, element_id):
    try:
        return WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, element_id)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_xpath(browser, xpath):
    try:
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_xpath_clickable(browser, xpath):
    try:
        wait_until_class_name_invisible(browser, 'ant-modal-wrap')
        wait_until_class_name_invisible(browser, 'ant-notification-notice')
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, xpath)))
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        WebDriverWait(browser, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_element_by_id_clickable(browser, element_id):
    try:
        wait_until_class_name_invisible(browser, 'ant-modal-wrap')
        wait_until_class_name_invisible(browser, 'ant-notification-notice')
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, element_id)))
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.ID, element_id)))
        WebDriverWait(browser, TIMEOUT).until(EC.element_to_be_clickable((By.ID, element_id)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_element_by_class_name_clickable(browser, class_name):
    try:
        wait_until_class_name_invisible(browser, 'ant-modal-wrap')
        wait_until_class_name_invisible(browser, 'ant-notification-notice')
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
        WebDriverWait(browser, TIMEOUT).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_element_by_css_selector_clickable(browser, css_selector):
    try:
        wait_until_class_name_invisible(browser, 'ant-modal-wrap')
        wait_until_class_name_invisible(browser, 'ant-notification-notice')
        WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        WebDriverWait(browser, TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        print("Error: TimeoutException")


def wait_until_class_name_invisible(browser, class_name, timeout=TIMEOUT):
    try:
        WebDriverWait(browser, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, class_name)))
    except TimeoutException:
        print("Error: TimeoutException")


def page_has_loaded(browser):
    page_state = browser.execute_script('return document.readyState;')
    return page_state == 'complete'


def wait_until_page_loads(browser, timeout=TIMEOUT):
    t = 0
    while t < timeout:
        time.sleep(1)
        if page_has_loaded(browser):
            break
        t += 1

