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
window.geometry("480x320+0+0")

frame = Frame(master=window, bg=BGCOLOR)

label = Label(master=frame, bg=BGCOLOR, font=("Arial", 14), fg="black", justify=LEFT)
labelJetzt = Label(master=frame, bg=BGCOLOR, font=("Arial", 14), fg="black", justify=LEFT)

#Zeit holen, parsen und in deutscher Format wandeln
locale.setlocale(locale.LC_ALL,'')
zeitRoh = email.utils.parsedate_tz(aktuellData['current_observation']['observation_time_rfc822'])
zeit = time.strftime("%A %H:%M", time.gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))

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
label2.place(x = 9, y = 35, width = 50, height = 50)
labelJetzt.place(x = 60, y = 0, width = 420, height = 130)
label.place(x = 0, y = 135, width = 480, height = 185)
button.place(x = 460, y = 300, width = 20, height = 20)

print "erzeuge Texte"

jetztText = 'Wetterdaten von ' + zeit +' Uhr.\n'
jetztText += aktuellData['current_observation']['weather'] + " bei "
jetztText += str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt wie "
jetztText += aktuellData['current_observation']['feelslike_c'] + u"°C.\n"
jetztText += u'Die Luftfeuchtigkeit beträgt ' + aktuellData['current_observation']['relative_humidity'] + '.\n'
jetztText += 'Der Luftdruck ist mit ' + aktuellData['current_observation']['pressure_mb'] + 'mbar '
if aktuellData['current_observation']['pressure_trend'] == '+':
    jetztText += 'steigend.\n'
elif aktuellData['current_observation']['pressure_trend'] == '-':
    jetztText += 'fallend.\n'
else:
    jetztText += 'gleichbeibend.\n'
if aktuellData['current_observation']['wind_kph'] > 0:
    jetztText += 'Wind aus Richtung ' + aktuellData['current_observation']['wind_dir'] + ' mit '
    jetztText += str(aktuellData['current_observation']['wind_kph']) + "km/h\n\n"
else:
    jetztText += 'Es ist windstill.'

heuteText  = 'Heute soll es bei '
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C bis "
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C "
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['conditions'].lower() + ' sein und\n'
if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
        heuteText += 'es soll trocken bleiben.\n'
    else:
        heuteText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'])
        heuteText += 'mm Regen geben.\n'
else:
    heuteText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'])
    heuteText += 'cm Schnee geben.\n'
if astronomieData['moon_phase']['percentIlluminated'] == u'0':
    heuteText += 'Der Mond ist als Neumond nicht sichtbar.\n'
elif astronomieData['moon_phase']['percentIlluminated'] == u'100':
    heuteText += 'Es ist Vollmond.\n'
else:
    heuteText += astronomieData['moon_phase']['phaseofMoon']
    heuteText += ' vom Mond der '
    heuteText += 'zu ' + astronomieData['moon_phase']['percentIlluminated'] + '% '
    heuteText += 'sichtbar ist.\n'
heuteText += 'Die Sonne geht ' + astronomieData['sun_phase']['sunrise']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunrise']['minute']
heuteText += ' Uhr auf und ' + astronomieData['sun_phase']['sunset']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunset']['minute'] + ' Uhr unter.\n\n'

vorhersageText  = 'Morgen ' + vorhersageData['forecast']['simpleforecast']['forecastday'][1]['conditions'].lower() + ', bei '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C und "
if vorhersageData['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'] == 0:
        vorhersageText += 'trocken.\n'
    else:
        vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'])
        vorhersageText += 'mm Regen.\n'
else:
    vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'])
    vorhersageText += 'cm Schnee.\n'
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['conditions'].lower() + ', bei '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C und "
if vorhersageData['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'] == 0:
        vorhersageText += 'trocken.\n'
    else:
        vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'])
        vorhersageText += 'mm Regen.\n'
else:
    vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'])
    vorhersageText += 'cm Schnee.\n'
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + ' '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['conditions'].lower() + ', bei '
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C bis "
vorhersageText += vorhersageData['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C und "
if vorhersageData['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'] == 0:
        vorhersageText += 'trocken.\n'
    else:
        vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'])
        vorhersageText += 'mm Regen.\n'
else:
    vorhersageText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'])
    vorhersageText += 'cm Schnee.\n'

label.config(text=heuteText + vorhersageText)
labelJetzt.config(text=jetztText)
print "zeige Fenster"
window.mainloop()
