import os
from datetime import datetime
from time import sleep

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import ifttt_key


def waitForElement(driver, by_what=By.XPATH, element_info='', delay=90, do_quit=True):
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_what, element_info)))
        return elem
    except TimeoutException:
        print("Loading took too much time!")
        print("quiting while waiting for element:", element_info)
        if do_quit:
            send_report_and_close("quiting while waiting for element: " + element_info, driver)
            # driver.quit()
        return None


def sendNotification(app_name, message, additional_message, event_name='program_log'):
    data = {
        "value1": app_name,
        "value2": message,
        "value3": additional_message
    }
    url = "https://maker.ifttt.com/trigger/" + event_name + "/with/key/" + ifttt_key

    r = requests.post(url, data=data)

    return r


def send_report_and_close(report, driver, special=''):
    if ifttt_key != '':
        for i in range(10):
            r = sendNotification(ifttt_key, "Health report", report, special)
            if r.status_code == 200:
                break
            else:
                print("Hasn't sent retrying... " + str(i) + " of 10")
    if driver is not None:
        driver.close()
    # exit()


def fill_in(login, password):
    report = ''
    url = 'https://xmuxg.xmu.edu.cn/app/214'

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")

    '''
        LOAD WEBSITE
    '''
    try:
        path_to_driver = os.path.join(os.path.curdir, 'chromedriver')
        driver = webdriver.Chrome(path_to_driver, options=options)
    except WebDriverException:
        report = 'WebDriver Not Found.'
        send_report_and_close(report, None, special='FATAL')

    driver.get(url)

    if '<html dir="ltr" lang="en"><head>' in driver.page_source:
        report = 'URL is incorrect.'
        send_report_and_close(report, driver, special='FATAL')

    loaded_url = driver.current_url

    '''
        LOG IN
    '''
    if 'login' in loaded_url:
        # log in here then
        print('0) trying to log in')
        login_button = waitForElement(driver, element_info="//button[contains(.,'统一身份认证')]")
        login_button.click()

        login_field = driver.find_element_by_xpath("//input[@id='username']")
        login_field.click()
        print('clicking login')
        # login_field.clear()
        login_field.send_keys(login)

        password_field = driver.find_element_by_xpath("//input[@id='password']")
        password_field.click()
        print('clicking password')
        # password_field.clear()
        password_field.send_keys(password)

        # press login/登录
        loging_button = driver.find_element_by_xpath("//button[contains(.,'登录/Login')]")
        loging_button.click()

        if loaded_url != driver.current_url:
            print("logged in successfully")
            report += "Login OK."
        else:
            print("Hasn't logged in")
            report = "Hasn't logged in. Check log:pass"
            send_report_and_close(report, driver)

    # print("logged in")

    '''
        SELECT PROPER SECTION
    '''
    print("closing nav bar")
    nav_bar = waitForElement(driver, element_info="//div[@class='menu-toggle pull-left']//i[@class='maticon']")
    nav_bar.click()

    print("selecting daily health section")

    # dhr_section = waitForElement(driver, element_info="//div[contains(text(),'防疫管理')]")
    dhr_section = waitForElement(driver, element_info="//div[contains(text(),'Daily Health Report')]")
    dhr_section.click()

    '''
        NEW TAB HERE
    '''
    sleep(10)  # waiting for tab to open/appear
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    driver.switch_to.window(driver.window_handles[-1])
    tab_button = waitForElement(driver, element_info="//div[contains(@class, 'tab')][2]")

    '''
        CHECK DATE
    '''
    curdate = datetime.today().strftime('%Y-%m-%d')
    if len(driver.find_elements_by_xpath("//span[text()[contains(.,'" + curdate + "')]]")) > 0:
        print("date is correct:", curdate)
        report += "Date OK."
    else:
        print("there's something wrong with date " + curdate + ", but we'll continue anyway")
        report += "Date BAD."

    '''
        CHECK TIME
    '''
    hours = int(datetime.today().strftime('%H'))
    minutes = int(datetime.today().strftime('%M'))

    if (hours == 19 and minutes >= 30) or hours < 7:
        print("too late for the daily health report")
        report += "Time BAD."
        send_report_and_close(report, driver)
    else:
        print("time is alright:", hours, ':', minutes)
        report += "Time OK."

    '''
        REPORTING PART
        MENU BUTTON
    '''
    print("1) choosing 我的菜单")
    tab_button.click()

    '''
        CONFIRMATION FIELD
    '''
    # waiting for tab to load up properly
    not_used = waitForElement(driver, element_info="//span[contains(text(),'No need to fill out or c')]")

    # ready to continue
    # hoping that the last element is the confirmation one
    confirmation_field = driver.find_elements_by_xpath("//div[contains(@class, 'v-select btn-block info-value')]")[-1]

    '''
        CLICK YES
    '''
    if len(driver.find_elements_by_xpath("//span[text()[contains(.,'是 Yes')]]")) > 0:
        print("confirmation is already yes, consider checking website yourself")
        report += 'Yes already.'
        # clicking outside
        # driver.find_element_by_xpath("//body").click()
    else:
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # hoping that the last element is the confirmation one
        confirmation_field.click()
        print("2) chose confirmation field")
        yes_button = driver.find_element_by_xpath(
            "//span[text()[contains(.,'是 Yes')]]/ancestor::label[@class='btn-block']")

        yes_button.click()
    print("3) clicked yes-button")

    '''
        SAVE BUTTON
    '''
    # May cause some problems if there will be something below the button
    save_button = driver.find_elements_by_xpath("//span[text()[contains(.,'保存')]]")[-1]

    '''
        SAVING
    '''
    saved_suc = None
    retry = -1
    driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
    while saved_suc is None and retry < 10:
        retry += 1
        if retry > 0:
            print("Hasn't saved retrying:", retry, "of 10")
        # save_button.click()
        driver.execute_script("arguments[0].click();", save_button)
        print("4) clicked save")

        '''
            POPUP ALERT
        '''
        driver.switch_to.alert.accept()
        print("5) clicked OK on an alert window")

        '''
            保存成功
        '''
        saved_suc = waitForElement(driver, element_info="//pre[contains(@class, 'message')]", do_quit=False)

    report += 'Saved OK. Login: ' + login
    if retry > 0:
        report += str(retry) + ' retry'

    print("6) has been saved")

    '''
        DONE
    '''
    print("It should be done by now with", login)
    send_report_and_close(report, driver)
