from config import login, password
from fill_in import fill_in

'''
    FILL IN
'''
for i in range(len(login)):
    if login[i] != '' and password[i] != '':
        fill_in(login[i], password[i])
    else:
        print("Don't forget to fill in login and password in config.py")

exit()
