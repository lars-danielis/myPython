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

# Wunderground JSON-Daten holen
print "hole aktuelle Werte"
aktuell = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole Vorhersagen"
vorhersage = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/forecast/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole astronomische Werte"
astronomie = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/astronomy/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole Alarme"
alarme = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/alerts/lang:DL/pws:1/q/pws:ibadenwr274.json")

# JSON-Strukturen parsen und anlegen
print "verarbeite JSON"
aktuellData = aktuell.json()
vorhersageData = vorhersage.json()
astronomieData = astronomie.json()
alarmeData = alarme.json()

# Fenster bauen
print "baue Fenster"
window = Tk()
window.overrideredirect(True)
window.geometry("480x320+0+0")
frame = Frame(master=window, bg=BGCOLOR)
label = Label(master=frame, bg=BGCOLOR, font=("Arial", 14), fg="black", justify=LEFT)
labelJetzt = Label(master=frame, bg=BGCOLOR, font=("Arial", 14), fg="black", justify=LEFT)

# Zeitstempel der Wetterdaten holen, parsen und in deutsches Format wandeln
locale.setlocale(locale.LC_ALL,'')
zeitRoh = email.utils.parsedate_tz(aktuellData['current_observation']['observation_time_rfc822'])
zeit = time.strftime("%A %H:%M", time.gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))

# Icon für aktuelles Wetter holen, vorher alte(s) löschen
print "lösche alte Icons"
for filename in glob("*.gif"):
    os.remove(filename)
print "hole aktuelles Icon"
iconUrl = aktuellData['current_observation']['icon_url'] # IconUrl holen
iconUrl = iconUrl.replace("/k/", "/j/")                  # Art des Icons tauschen
filename = wget.download(iconUrl)                        # Icon dowloaden
img = Image.open(filename)                               # Icon-Datei öffnen
imgTk = ImageTk.PhotoImage(img)                          # Icon-Datei in Grafikobjekt laden
label2 = Label(master=frame, bg=BGCOLOR, image=imgTk)    # Grafikobjekt in Label einbauen

# Beenden Knopf
button = Button(master=frame, text="X", bg=BGCOLOR, fg="white", command=window.destroy)

# Labels in Fenster einbauen und anordnen
frame.pack(expand=True, fill=BOTH)
label2.place(x = 9, y = 35, width = 50, height = 50)
labelJetzt.place(x = 60, y = 0, width = 420, height = 130)
label.place(x = 0, y = 135, width = 480, height = 185)
button.place(x = 460, y = 300, width = 20, height = 20)

print "erzeuge Texte"
# Wetter jetzt
jetztText = 'Wetterdaten von ' + zeit +' Uhr.\n'
jetztText += aktuellData['current_observation']['weather'] + " bei "
jetztText += str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt wie "
jetztText += aktuellData['current_observation']['feelslike_c'] + u"°C.\n"
# Luftfeuchtigkeit jetzt
jetztText += u'Die Luftfeuchtigkeit beträgt ' + aktuellData['current_observation']['relative_humidity'] + '.\n'
# Luftdruck jetzt und Tendenz
jetztText += 'Der Luftdruck ist mit ' + aktuellData['current_observation']['pressure_mb'] + 'mbar '
if aktuellData['current_observation']['pressure_trend'] == '+':
    jetztText += 'steigend.\n'
elif aktuellData['current_observation']['pressure_trend'] == '-':
    jetztText += 'fallend.\n'
else:
    jetztText += 'gleichbeibend.\n'
# Wind jetzt
if aktuellData['current_observation']['wind_kph'] > 0:
    jetztText += 'Wind aus Richtung ' + aktuellData['current_observation']['wind_dir'] + ' mit '
    jetztText += str(aktuellData['current_observation']['wind_kph']) + "km/h."
else:
    jetztText += 'Es ist windstill.'

# Vorhersage heute
heuteText  = 'Heute soll es bei '
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C bis "
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C "
heuteText += vorhersageData['forecast']['simpleforecast']['forecastday'][0]['conditions'].lower() + ' sein und\n'
# Niederschlag heute
if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
        heuteText += 'es soll trocken bleiben.\n'
    else:
        heuteText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'])
        heuteText += 'mm Regen geben.\n'
else:
    heuteText += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'])
    heuteText += 'cm Schnee geben.\n'
# Mond heute
if astronomieData['moon_phase']['percentIlluminated'] == u'0':
    heuteText += 'Der Mond ist als Neumond nicht sichtbar.\n'
elif astronomieData['moon_phase']['percentIlluminated'] == u'100':
    heuteText += 'Es ist Vollmond.\n'
else:
    heuteText += astronomieData['moon_phase']['phaseofMoon'] + ', der Mond ist zu '
    heuteText += astronomieData['moon_phase']['percentIlluminated'] + '% '
    heuteText += 'sichtbar ist.\n'
heuteText += 'Die Sonne geht ' + astronomieData['sun_phase']['sunrise']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunrise']['minute']
heuteText += ' Uhr auf und ' + astronomieData['sun_phase']['sunset']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunset']['minute'] + ' Uhr unter.\n\n'

# Vorhersage morgen
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
# Vorhersage übermorgen
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
# Vorhersage überübermorgen
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

# Textlabels für das Fenster zusammensetzen
label.config(text=heuteText + vorhersageText)
labelJetzt.config(text=jetztText)

# Fensterloop
print "zeige Fenster"
window.mainloop()
