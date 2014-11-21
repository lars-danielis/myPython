#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import locale
import time
import email.utils
import requests
import wget
from glob import glob
import os
from Tkinter import *
from PIL import Image, ImageTk

BGCOLOR = "white"
WEISS = "#FFF"

print "hole aktuelle Werte"
aktuell = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/lang:DL/pws:1/q/pws:ibadenwr250.json")
print "hole Vorhersagen"
vorhersage = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/forecast/lang:DL/pws:1/q/pws:ibadenwr250.json")
print "hole astronomische Werte"
astronomie = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/astronomy/lang:DL/pws:1/q/pws:ibadenwr250.json")
print "hole Alarme"
alarme = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/alerts/lang:DL/pws:1/q/pws:ibadenwr250.json")

print "verarbeite JSON"
aktuellData = aktuell.json()
vorhersageData = vorhersage.json()
astronomieData = astronomie.json()
alarmeData = alarme.json()

print "baue Fenster"
window = Tk()
window.overrideredirect(True)
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
# window.geometry(str(w) + "x" + str(h) + "+0+0")
window.geometry("480x320+0+0")

frame = Frame(master=window, bg=BGCOLOR)

label = Label(master=frame, bg=BGCOLOR, font=("Comic", 11), fg="black", justify=LEFT)

#Zeit holen, parsen und in deutscher Format wandeln
locale.setlocale(locale.LC_ALL,'')
zeitRoh = email.utils.parsedate(aktuellData['current_observation']['observation_time_rfc822'])
zeitTime = time.mktime(zeitRoh)
zeit = time.strftime("%A %d.%m.%Y %H:%M", time.gmtime(zeitTime))

print "lösche alte Icons"
for filename in glob("*.gif"):
    os.remove(filename)

print "hole aktuelles Icon"
iconUrl = aktuellData['current_observation']['icon_url']
iconUrl = iconUrl.replace("/k/", "/j/")
filename = wget.download(iconUrl)
img = Image.open(filename)
imgTk = ImageTk.PhotoImage(img)
label2 = Label(master=frame, bg=BGCOLOR, image=imgTk)

button = Button(master=frame, text="X", bg=BGCOLOR, fg="white", command=window.destroy)

frame.pack(expand=True, fill=BOTH)
label2.pack(expand=TRUE, side=LEFT)
label.pack(expand=True, fill=BOTH, side=LEFT)
button.pack(side=RIGHT, anchor=S)

print "erzeuge Texte"
aktuellText  = 'Heute:\n'
aktuellText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['conditions'] + ' '
aktuellText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C bis "
aktuellText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C und "
if aktuellData['current_observation']['precip_today_metric'] == '--':
    aktuellText += 'trocken\n'
else:
    aktuellText += aktuellData['current_observation']['precip_today_metric'] + "mm Niederschlag\n"
aktuellText += astronomieData['moon_phase']['phaseofMoon']
aktuellText += ', der Mond ist zu ' + astronomieData['moon_phase']['percentIlluminated'] + "% sichtbar\n"
aktuellText += 'Sonenaufgang ' + astronomieData['sun_phase']['sunrise']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunrise']['minute']
aktuellText += ', Sonnenuntergang ' + astronomieData['sun_phase']['sunset']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunset']['minute'] + '\n\n'
aktuellText += ' Wetterdaten von: ' + zeit +"\n "
aktuellText += aktuellData['current_observation']['weather'] + " und "
aktuellText += str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt wie "
aktuellText += aktuellData['current_observation']['feelslike_c'] + u"°C\n"
aktuellText += ' Luftfeuchtigkeit ' + aktuellData['current_observation']['relative_humidity'] + '\n'
aktuellText += ' Luftdruck ' + aktuellData['current_observation']['pressure_mb'] + 'mbar Tendenz '
aktuellText += aktuellData['current_observation']['pressure_trend'] + "\n"
if aktuellData['current_observation']['wind_kph'] > 0:
    aktuellText += ' Wind aus Richtung ' + aktuellData['current_observation']['wind_dir'] + ' mit '
    aktuellText += str(aktuellData['current_observation']['wind_kph']) + "km/h\n\n"
else:
    aktuellText += ' Windstill\n\n'
vorhersageText  = 'Morgen ' + vorhersageData['forecast']['simpleforecast']['forecastday'][1]['conditions'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C\n"
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['conditions'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C\n"
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['conditions'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C\n"

label.config(text=aktuellText + vorhersageText)

print "zeige Fenster"
window.mainloop()