import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waitForElement(driver, by_what=By.XPATH, element_info='', delay=5, do_quit=True):
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_what, element_info)))
        print("Page is ready!")
        return elem
    except TimeoutException:
        print("Loading took too much time!")
        print("quiting while waiting for element:", element_info)
        if do_quit:
            driver.quit()
        return None


def sendNotification(app_name, message, additional_message='', event_name='log_from_app'):
    my_key = ''
    data = {
        "value1": app_name,
        "value2": message,
        "value3": additional_message
    }
    url = "https://maker.ifttt.com/trigger/" + event_name + "/with/key/" + my_key

    r = requests.post(url, data=data)

    return r


def send_report_and_close(report, driver):
    for i in range(10):
        r = sendNotification("Health report", report)
        if r.status_code == 200:
            break
        else:
            print("Hasn't sent retrying... " + str(i) + " of 10")

    driver.close()
    exit()


login = ''  # student number
password = ''  # you should know it

report = ''
url = 'https://xmuxg.xmu.edu.cn/app/214'
path_to_driver = os.path.join(os.path.curdir, 'chromedriver')

driver = webdriver.Chrome(path_to_driver)
driver.get(url)

loaded_url = driver.current_url

# In case you are not logged in
if 'login' in loaded_url:
    # log in here then
    print('0) trying to log in')
    login_button = waitForElement(driver, element_info="//button[contains(.,'统一身份认证')]")
    # loging_button = driver.find_element_by_xpath("//button[contains(.,'统一身份认证')]")
    login_button.click()

    login_field = driver.find_element_by_name("username")
    login_field.click()
    print('clicking login')
    # login_field.clear()
    login_field.send_keys(login)

    password_field = driver.find_element_by_name("password")
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

print("logged in")

'''
    CHECK DATE
'''
menu_button = waitForElement(driver, element_info="//div[contains(@class, 'tab')][2]")

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

if hours >= 16 and minutes >= 30:
    print("too late for the daily health report")
    report += "Time BAD."
    send_report_and_close(report, driver)
    # TODO: send_report_and_close()
else:
    print("time's alright:", hours, ':', minutes)
    report += "Time OK."

'''
    REPORTING PART
    MENU BUTTON
'''

menu_button.click()
print("1) chose 我的菜单")

'''
    CONFIRMATION FIELD
'''
# waiting for tab to load up properly
not_used = waitForElement(driver, element_info="//span[text()[contains(.,'37.3')]]")

# ready to continue
# hoping that the last element is the confirmation one
confirmation_field = driver.find_elements_by_xpath("//div[contains(@class, 'form-control dropdown-toggle')]")[-1]

'''
    CLICK YES
'''
if len(driver.find_elements_by_xpath("//span[text()[contains(.,'是 Yes')]]")) > 0:
    print("confirmation is already yes, consider checking website yourself")
    report += 'Yes already.'
    # clicking outside
    # driver.find_element_by_xpath("//body").click()
else:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # hoping that the last element is the confirmation one
    confirmation_field.click()
    print("2) chose confirmation field")
    yes_button = driver.find_element_by_xpath("//span[text()[contains(.,'是 Yes')]]/ancestor::label[@class='btn-block']")

    yes_button.click()
print("3) clicked yes-button")

'''
    SAVE BUTTON
'''
# May cause some problems if there will be something below the button
save_button = driver.find_elements_by_xpath("//span[text()[contains(.,'保存')]]")[-1]

'''
    保存成功
'''

saved_suc = None
retry = -1
while saved_suc is None and retry < 10:
    retry += 1
    if retry > 0:
        print("Hasn't saved retrying:", retry, "of 10")
    save_button.click()
    print("4) clicked save")

    '''
        POPUP ALERT
    '''
    driver.switch_to.alert.accept()
    print("5) clicked OK on an alert window")

    '''
        保存成功
    '''
    saved_suc = waitForElement(driver, delay=7, element_info="//pre[contains(@class, 'message')]", do_quit=False)

report += 'Saved OK.'
if retry > 0:
    report += str(retry) + ' retry'

print("6) has been saved")

'''
    DONE
'''
print("It should be done by now")
send_report_and_close(report, driver)

