#Ventilation Manager
# Author: Bastian Brück, ZBB Marburg#
import sys
import threading
import time
import json
from threading import Thread
import urllib.request as rq
from plyer import notification
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu
from PyQt5.QtGui import QIcon


# Weather API variables
api_key = "WIAJBr3YssQyD8C5OGlKmp3ek0OXZtgL"
country_code = "DE"
city = "Marburg"

key = ""

# Weather API Methods


def getLocation(countrycode, city):
    search_address = "http://dataservice.accuweather.com/locations/v1/cities/"+countrycode+"/search?apikey=WIAJBr3YssQyD8C5OGlKmp3ek0OXZtgL&q="+city+"&language=de&details=true"

    with rq.urlopen(search_address) as search_address:
        data = json.loads(search_address.read().decode())
    location_key = data[0]['Key']

    return location_key


def getTemperature(location_key):
    temperature_url = "http://dataservice.accuweather.com/currentconditions/v1/"+ location_key +"?apikey=WIAJBr3YssQyD8C5OGlKmp3ek0OXZtgL&language=de&details=true"
    with rq.urlopen(temperature_url) as temperature_Url:
        data = json.loads(temperature_Url.read().decode())

    for key1 in data:
        temperature = (key1['Temperature']['Metric']['Value'])

    return temperature


# Timer variables
# openTime = Timer Until Window needs to be opened
# closeTime = Timer Until Windows needs to be closed#
openTime = 0
closeTime = 0


def setTimer(temperature):

    if temperature > 20:
        openTime = 5*60
        closeTime = 15*60
    elif temperature < 10:
        openTime = 15*60
        closeTime = 5 * 60
    elif temperature < 20:
        openTime = 10 * 60
        closeTime = 10 * 60

    return openTime, closeTime


def schedule(t):

    while t:
        mins = t // 60
        secs = t % 60
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("'\r{0}".format(timer), end='')
        time.sleep(1)
        t -= 1


def Notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon='Ampeross-Qetto-2-Timer.ico',
        timeout=5,
    )


def mainloop():
    key = getLocation(country_code, city)

    while True:
        openTime, closeTime = setTimer(getTemperature(key))
        schedule(int(openTime))
        Notification("VentMan", "Open your Window")
        schedule(int(closeTime))
        Notification("VentMan", "Close your Window")


def systray():
    # setup Tray Icon to close application
    app = QApplication(sys.argv)

    trayIcon = QSystemTrayIcon(QIcon('Ampeross-Qetto-2-Timer.ico'), parent=None)
    trayIcon.setToolTip("VentManager")
    trayIcon.show()

    menu = QMenu()
    exitAction = menu.addAction('Exit')
    trayIcon.setContextMenu(menu)

    exitAction.triggered.connect(lambda: sys.exit())

    app.exec()


def main():
    t1 = threading.Thread(target=mainloop)
    t2 = threading.Thread(target=systray)

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
