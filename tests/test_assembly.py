from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import config
import urllib.request
import json
import re
from lib.drag_and_drop import drag_and_drop
from lib import exists
from lib import wait
from lib.exceptions import *

opts = Options()
opts.headless = False
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


# open Catalogue panel
def test_click_catalogue():
    wait.wait_until_xpath_clickable(browser, '//span[contains(.,"Catalogue")]')
    browser.find_element_by_xpath('//span[contains(.,"Catalogue")]').click()


# open assembly panel
def test_click_assembly():
    browser.find_element_by_xpath("//a[contains(.,'Assembly')]").click()


# delete sector for Merostomata
def test_sector_search():

    # search for Merostomata
    wait.wait_until_element_by_class_name_clickable(browser, 'ant-input')
    search_input = browser.find_elements_by_class_name('ant-input')[0]
    search_input.clear()
    search_input.send_keys('Merostomata')

    # click on the Merostomata search result
    wait.wait_until_xpath_clickable(browser, '//li[contains(text(),"Merostomata")]')
    browser.find_element_by_xpath('//li[contains(text(),"Merostomata")]').click()

    # click on the Merostomata sector attachment point
    wait.wait_until_xpath_clickable(browser, '//div[contains(text(),"Merostomata")]')
    browser.find_element_by_xpath('//div[contains(text(),"Merostomata")]').click()


def test_show_sector_in_source():
    # click the 'Show sector in source' button
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"Show sector in source")]')
    browser.find_element_by_xpath('//button[contains(.,"Show sector in source")]').click()


def test_delete_sector():
    # click the 'Delete sector' button
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"Delete sector")]')
    browser.find_element_by_xpath('//button[contains(.,"Delete sector")]').click()

    # confirm dataset was deleted
    with urllib.request.urlopen('https://api-dev.col.plus/sector/?datasetKey=1152') as url:
        data = json.loads(url.read().decode())
        assert len(data) == 0


def test_attach_sector():
    # dismiss sector popup
    browser.find_element_by_xpath("//a[contains(.,'Assembly')]").click()

    # TODO: eliminate hack to get drag_and_drop() to work when Selenium bug is fixed
    # # ActionChains(browser).drag_and_drop(src_element, dest_element).perform()  # won't work currently
    # begin hack to get around the selenium drag_and_drop bug
    drag_and_drop(browser,
            "div.ant-row:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > "
            "div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > ul:nth-child(3) > li:nth-child(1) > "
            "ul:nth-child(3) > li:nth-child(1) > span:nth-child(2) > span:nth-child(1) > div:nth-child(1) > "
            "div:nth-child(1) > span:nth-child(1)",
            ".ant-tree-node-selected > span:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)")
    # end hack to get around the selenium drag_and_drop bug

    # tests for Sp2000/colplus-frontend#271 issue
    ant_message = browser.find_element_by_class_name('ant-message')
    if ant_message.get_attribute('innerText') == 'You cant modify the CoL draft in attachment mode':
        raise ErrorMessageDisplayed('You cant modify the CoL draft in attachment mode')

    # click okay for sector attachment
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"OK")]')
    browser.find_element_by_xpath('//button[contains(.,"OK")]').click()

    # confirm dataset was attached
    with urllib.request.urlopen('https://api-dev.col.plus/sector/?datasetKey=1152') as url:
        data = json.loads(url.read().decode())
        assert len(data) == 1

    time.sleep(3)


def test_close_search():
    # close search
    assert browser.find_elements_by_class_name('ant-input')[0].get_attribute('value') == 'Merostomata'
    browser.find_element_by_css_selector('.anticon-close-circle').click()
    assert browser.find_elements_by_class_name('ant-input')[0].get_attribute('value') == ''


def test_tree_navigation():
    # reload assembly page to reset classification tree
    browser.get("http://" + config.HOSTNAME + ":" + config.PORT + "/assembly")
    time.sleep(5)

    # expand kingdom Chromista
    browser.find_element_by_css_selector('li.ant-tree-treenode-switcher-close:nth-child(4) > span:nth-child(1) > '
                                         'i:nth-child(1) > svg:nth-child(1)').click()


def test_dataset_search():
    search_term = 'Sector attach'

    # search for search_term
    wait.wait_until_element_by_class_name_clickable(browser, 'ant-input')
    search_input = browser.find_elements_by_class_name('ant-input')[1]
    search_input.clear()
    search_input.send_keys(search_term)

    # click on the search_term search result
    wait.wait_until_xpath_clickable(browser, '//li[contains(text(),"' + search_term + '")]')
    browser.find_element_by_xpath('//li[contains(text(),"' + search_term + '")]').click()


def test_within_dataset_search():
    search_term = 'Microheliella maris'

    # search for Merostomata
    wait.wait_until_element_by_class_name_clickable(browser, 'ant-input')
    search_input = browser.find_elements_by_class_name('ant-input')[2]
    search_input.clear()
    search_input.send_keys(search_term)

    # click on the search_term search result
    wait.wait_until_xpath_clickable(browser, '//div/div/div/ul/li')
    browser.find_element_by_xpath('//div/div/div/ul/li').click()
    time.sleep(5)


def test_attach_sector_from_search():
    # dismiss sector popup
    browser.find_element_by_xpath("//a[contains(.,'Assembly')]").click()

    # get dataset id from source_url
    source_url_element = browser.find_element_by_css_selector(
        'div.ant-row:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > '
        'h4:nth-child(1) > a:nth-child(1)')
    source_url = source_url_element.get_attribute('href')
    dataset_id = re.findall(r'.*\/dataset\/([0-9]+)\/meta.*', source_url)[0]

    # confirm no sector attachments for dataset
    with urllib.request.urlopen('https://api-dev.col.plus/sector/?datasetKey=' + str(dataset_id)) as url:
         data = json.loads(url.read().decode())
         assert len(data) == 0

    # find dest  source element
    src_css_selector = 'li.ant-tree-treenode-switcher-open:nth-child(4) > span:nth-child(2) > span:nth-child(1) > ' \
                       'div:nth-child(1) > div:nth-child(1)'
    dest_css_selector = 'div.ant-row:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ' \
                        'div:nth-child(5) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > ' \
                        'span:nth-child(2) > span:nth-child(1) > div:nth-child(1) > div:nth-child(1)'

    # TODO: eliminate hack to get drag_and_drop() to work when Selenium bug is fixed
    # # ActionChains(browser).drag_and_drop(src_element, dest_element).perform()  # won't work currently
    drag_and_drop(browser, dest_css_selector, src_css_selector)
    time.sleep(2)

    # click okay for sector attachment
    wait.wait_until_xpath_clickable(browser, '//button[contains(.,"OK")]')
    browser.find_element_by_xpath('//button[contains(.,"OK")]').click()
    time.sleep(2)

    # confirm dataset was attached
    with urllib.request.urlopen('https://api-dev.col.plus/sector/?datasetKey=' + str(dataset_id)) as url:
         data = json.loads(url.read().decode())
         assert len(data) == 1
    time.sleep(2)


def test_sync_sector():
    # determine number of sector syncs before pressing sync button
    before = browser.find_element_by_css_selector('div.ant-col-6:nth-child(1) > div:nth-child(1) > div:nth-child(2)')\
        .get_attribute('innerText')

    # find and click sector sync button
    sector = browser.find_element_by_css_selector('.ant-tree-child-tree > li:nth-child(5) > span:nth-child(2) > '
                                                  'span:nth-child(1) > div:nth-child(1) > div:nth-child(1) > '
                                                  'span:nth-child(3) > div:nth-child(2)')
    sector.click()
    browser.find_element_by_css_selector('button.ant-btn:nth-child(3)').click()
    time.sleep(5)

    # determine number of sector syncs after pressing sync button
    after = browser.find_element_by_css_selector('div.ant-col-6:nth-child(1) > div:nth-child(1) > div:nth-child(2)').\
        get_attribute('innerText')

    # test that sync completed successfully
    assert int(before) + 1 == int(after)


# warning indicator should not be present
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
