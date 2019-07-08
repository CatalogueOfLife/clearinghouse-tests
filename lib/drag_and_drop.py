from hashlib import md5
import os


# this is a workaround for the Selenium drag_and_drop bug
def drag_and_drop(browser, src_css_selector, dest_css_selector):

    # generate temporary HTML ids from the CSS selectors
    #   element IDs need to be unique in case multiple drag and drops are used on the same page
    src_id = md5(src_css_selector.encode('utf-8')).hexdigest()
    dest_id = md5(dest_css_selector.encode('utf-8')).hexdigest()

    # execute javascript to set temporary HTML element attribute IDs
    browser.execute_script("document.querySelector('" + src_css_selector + "').setAttribute('id', '" + src_id + "')")
    browser.execute_script("document.querySelector('" + dest_css_selector + "').setAttribute('id', '" + dest_id + "')")

    # load and execute jQuery and the drag_and_drop_helper.js
    with open(os.path.abspath('../lib/drag_and_drop_helper.js'), 'r') as js_file:
        script = js_file.read()
    browser.execute_script(script + "$('#" + src_id + "').simulateDragDrop({ dropTarget: '#" + dest_id + "'});")
