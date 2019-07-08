from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import config
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


# click modify tree button
def test_click_modify_tree():
    wait.wait_until_element_by_css_selector_clickable(browser, "button.ant-btn:nth-child(1)")
    browser.find_element_by_css_selector("button.ant-btn:nth-child(1)").click()

    # test that button is selected
    assert browser.find_element_by_css_selector("button.ant-btn:nth-child(1)")\
        .get_attribute("class") == "ant-btn ant-btn-primary ant-btn-lg"


# add child to taxon to Chromista
def test_add_child():

    # click on Chromista
    chromista_css_selector = "li.ant-tree-treenode-switcher-close:nth-child(4) > span:nth-child(2) > " \
                             "span:nth-child(1) > div:nth-child(1) > span:nth-child(1) > " \
                             "span:nth-child(2) > i:nth-child(1)"
    wait.wait_until_element_by_css_selector_clickable(browser, chromista_css_selector)
    browser.find_element_by_css_selector(chromista_css_selector).click()

    # click on add child button
    add_child_xpath = "//button[contains(.,'Add child')]"
    wait.wait_until_xpath_clickable(browser, add_child_xpath)
    browser.find_element_by_xpath(add_child_xpath).click()

    # type in taxon name
    taxon_name_field_css_selector = "#name"
    browser.find_element_by_css_selector(taxon_name_field_css_selector).send_keys("Hyphochytriomycota")

    # select phylum as rank
    #wait.wait_until_element_by_id_clickable(browser, 'rank')
    browser.find_element_by_id('rank').click()
    time.sleep(2)
    browser.find_element_by_xpath("//li[.//text()='phylum']").click()

    # click the ok button
    #wait.wait_until_element_by_css_selector_clickable(browser, "button.ant-btn-primary:nth-child(2)")
    browser.find_element_by_css_selector("button.ant-btn-primary:nth-child(2)").click()

    # expand Chromista tree
    parent_csss = "li.ant-tree-treenode-switcher-close:nth-child(4) > span:nth-child(1) > i:nth-child(1) > " \
                  "svg:nth-child(1)"
    wait.wait_until_element_by_css_selector_clickable(browser, parent_csss)
    browser.find_element_by_css_selector(parent_csss).click()

    # test that child was added
    child_xpath = "//span[2]/i[. ='Hyphochytriomycota']"
    wait.wait_until_xpath_clickable(browser, child_xpath)
    assert exists.test_exists_by_xpath(browser, child_xpath)


# test delete child taxon
def test_delete_child():
    # click on Hyphochytriomycota
    child_xref = "//span[2]/i[. ='Hyphochytriomycota']"
    wait.wait_until_xpath_clickable(browser, child_xref)
    browser.find_element_by_xpath(child_xref).click()
    time.sleep(2)

    # click delete taxon button
    button_xpath = "//button[contains(.,'Delete taxon')]"
    browser.find_elements_by_xpath(button_xpath)[-1].click()
    time.sleep(2)

    # test that child was deleted
    child_xpath = "//span[2]/i[. ='Hyphochytriomycota']"
    assert not exists.test_exists_by_xpath(browser, child_xpath)


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
