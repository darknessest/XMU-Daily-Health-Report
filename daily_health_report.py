import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waitForElement(driver, by_what=By.XPATH, element_info='', delay=5):
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_what, element_info)))
        print("Page is ready!")
        return elem
    except TimeoutException:
        print("Loading took too much time!")
        print("quiting while waiting for element:", element_info)
        driver.quit()


login = ''  # student number
password = ''  # you should know it

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

print('logged in')

'''
    CHECK DATE
'''

curdate = datetime.today().strftime('%Y-%m-%d')
if len(driver.find_elements_by_xpath("//span[text()[contains(.,'" + curdate + "')]]")) > 0:
    print("date is correct:", curdate)
else:
    print("there's something wrong with date " + curdate + ", but we'll continue anyway")

'''
    CHECK TIME
'''
hours = int(datetime.today().strftime('%H'))
minutes = int(datetime.today().strftime('%M'))

if hours >= 16 and minutes >= 30:
    print("too late for the daily health report")
    driver.close()
    print("exiting")
    exit()
else:
    print("time's alright:", hours, ':', minutes)

'''
    REPORTING PART
    MENU BUTTON
'''
menu_button = waitForElement(driver, element_info="//div[contains(@class, 'tab')][2]")
# menu_button = driver.find_element_by_xpath("//div[contains(@class, 'tab')][2]")
# menu_button = driver.find_element_by_xpath("//div[text()='我的菜单')]")
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
if len(driver.find_elements_by_xpath("//span[text()[contains(.,'是 Yes')]]/ancestor::label[@class='btn-block']")) > 0:
    print("confirmation is already yes, consider checking website yourself")
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
save_button = driver.find_elements_by_xpath("//span[text()[contains(.,'保存')]]")
# May cause some problems if there will be something below the button
save_button[-1].click()
print("4) clicked save")

'''
    POPUP ALERT
'''
driver.switch_to.alert.accept()
print("5) clicked OK on an alert window")

'''
    DONE
'''
print('sleeping for 5 sec, so you can see the result')
time.sleep(5)  # kinda waiting for a response

driver.close()
print("It should be done by now")
