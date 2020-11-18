Small script to automate filling in XMU's daily health report

To improve cloning speed please use:
`git clone https://github.com/darknessest/XMU-Daily-Health-Report.git --depth 1`

It's recommended to add use the script at random time. For example, like in rpi0 branch.

#### Features:
 - Filling in for multiple accounts.
 - Sending notifications over IFTTT.


Tested on:
 - MacOS (Catalina) + chrome driver (81-84) + Selenium (3.141.0)
 - Raspberry Pi Zero and 4


#### Requirements:
```
requests selenium ~= 3.14
```
Also don't forget to download proper browser driver. Version of your browser driver should be the same(or higher) as your
currently installed browser. 

More information about ChromeDriver on [Selenium Wiki](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver)

You can download chromeDriver from [official website](https://sites.google.com/a/chromium.org/chromedriver/downloads)
(要翻墙。不能翻墙的话，去百度一下，下载下载)

~~Or use ones in this git. There were downloaded from the official website on 2020/03/28.~~

To run:
1) fill in login and password in config.py file (, and IFTTT key if you have it) 
2) provide a path to your webdriver
3) run the script
