from random import randint
from time import sleep

from config import login, password, sleep_time
from fill_in import fill_in

'''
    FILL IN
'''
for i in range(len(login)):
    # random timeout before filling in, check config file for settings
    timeout = randint(sleep_time[0] * 60, sleep_time[1] * 60)
    print('timeout is =', timeout)
    sleep(timeout)

    if login[i] != '' and password[i] != '':
        restart = 0
        while not fill_in(login[i], password[i]):
            restart += 1
            if restart > 10:
                break
    else:
        print("Don't forget to fill in login and password in config.py")

exit()
