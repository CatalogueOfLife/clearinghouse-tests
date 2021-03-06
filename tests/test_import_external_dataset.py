from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import datetime
import config
import re
import urllib.request
import json
from lib import exists
from lib import wait
from lib.exceptions import *

opts = Options()
opts.headless = True
browser = webdriver.Firefox(options=opts)
#browser = webdriver.Chrome()
browser.get('http://' + config.HOSTNAME + ':' + config.PORT)


# make sure host is up
def test_host_up():
    assert 'Catalogue of Life +' in browser.title


# click login button
def test_click_login():
    wait.wait_until_class_name_invisible(browser, 'ant-modal-wrap')
    assert exists.test_exists_by_xpath(browser, '//button[contains(.,"Login")]')
    browser.find_element_by_xpath('//button[contains(.,"Login")]').click()


# submit login form
def test_submit_login_form():
    username_input = browser.find_element_by_id('username')
    username_input.clear()
    username_input.send_keys(config.USER)
    password_input = browser.find_element_by_id('password')
    password_input.clear()
    password_input.send_keys(config.PASSWORD)
    browser.find_element_by_class_name('login-form-submit').click()


# open datasets panel
def test_click_datasets():
    wait.wait_until_xpath_clickable(browser, '//span[contains(.,"Datasets")]')
    browser.find_element_by_xpath('//span[contains(.,"Datasets")]').click()


# click new dataset
def test_click_dataset():
    browser.find_element_by_xpath("//a[contains(.,'New Dataset')]").click()


# add dataset title
def test_register_dataset():
    wait.wait_until_element_by_id_clickable(browser, 'title')
    title_input = browser.find_element_by_id('title')
    title_input.clear()
    title_input.send_keys('Robo-tester dataset ' + str(datetime.datetime.now()))
    time.sleep(1)

    # select license
    wait.wait_until_element_by_id_clickable(browser, 'license')
    browser.find_element_by_id('license').click()
    browser.find_element_by_xpath("//li[contains(.,'unspecified')]").click()

    # select dataset type
    wait.wait_until_element_by_id_clickable(browser, 'type')
    browser.find_element_by_id('type').click()
    browser.find_element_by_xpath("//li[contains(.,'global')]").click()

    # select dataset origin
    wait.wait_until_element_by_id_clickable(browser, 'origin')
    browser.find_element_by_id('origin').click()
    browser.find_element_by_xpath("//li[contains(.,'external')]").click()

    # select dataset format
    wait.wait_until_element_by_id_clickable(browser, 'dataFormat')
    browser.find_element_by_id('dataFormat').click()
    time.sleep(0.5)
    browser.find_element_by_xpath("//li[contains(.,'coldp')]").click()

    # enter dataset url
    wait.wait_until_element_by_id_clickable(browser, 'dataAccess')
    url_input = browser.find_element_by_id('dataAccess')
    url_input.clear()
    url_input.send_keys('https://raw.githubusercontent.com/Sp2000/data-unit-tests/master/duplicates.zip')

    # select dataset import frequency
    wait.wait_until_element_by_id_clickable(browser, 'importFrequency')
    browser.find_element_by_id('importFrequency').click()
    browser.find_element_by_xpath("//li[contains(.,'once')]").click()

    # click the save button
    browser.find_element_by_css_selector(".ant-btn-primary").click()


# click the import button
def test_data_importer():
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"Import")]')
    browser.find_element_by_xpath('//button[contains(.,"Import")]').click()
    time.sleep(2)

    # determine dataset ID
    dataset_id = re.findall(r'.*\/dataset\/([0-9]+)\/meta.*', browser.current_url)[0]

    time.sleep(1)

    # check import queue to make sure it finished successfully
    with urllib.request.urlopen('https://api-dev.col.plus/importer?limit=25&offset=0&state=finished&datasetKey=' +
                                str(dataset_id)) as url:
        data = json.loads(url.read().decode())
        print(data)
        assert int(data['total']) >= 1


# delete the dataset
def test_delete_dataset():
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"Delete")]')
    browser.find_element_by_xpath('//button[contains(.,"Delete")]').click()
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"Yes")]')
    browser.find_element_by_xpath('//button[contains(.,"Yes")]').click()

    # determine dataset ID
    dataset_id = re.findall(r'.*\/dataset\/([0-9]+)\/meta.*', browser.current_url)[0]

    time.sleep(1)

    # confirm dataset was deleted
    with urllib.request.urlopen('http://api-dev.col.plus/dataset/' + str(dataset_id)) as url:
        data = json.loads(url.read().decode())
        assert 'deleted' in data


# import warning indicator should not be present
def test_uncaught_warning_displayed():
    try:
        warning = browser.find_element_by_css_selector('html body div#root section.ant-layout.ant-layout-has-sider '
                                             'section.ant-layout main.ant-layout-content div '
                                             'div.ant-row div.ant-col.ant-col-2.ant-col-offset-18 '
                                             'i.anticon.anticon-warning svg')
        if warning is not None:
            raise WarningMessageDisplayed(warning.text)
    except NoSuchElementException:
        pass


# test for any errors displayed that are not caught by frontend testing yet
def test_uncaught_error_displayed():
    try:
        error_message_element = browser.find_element_by_class_name('ant-alert-error')
        raise ErrorMessageDisplayed(error_message_element.text)
    except NoSuchElementException:
        pass


# close browser
def test_browser_close():
    browser.close()
