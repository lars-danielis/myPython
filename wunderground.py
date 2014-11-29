#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Version 2 mit Icons auch für die Vorhersagen
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
SCHRIFTGROESSE = 14

locale.setlocale(locale.LC_ALL,'')

# Wunderground JSON-Daten holen
print "hole aktuelle Werte"
akt = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole Vorhersagen"
vor = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/forecast/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole astronomische Werte"
ast = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/astronomy/lang:DL/pws:1/q/pws:ibadenwr274.json")
print "hole Alarme"
al = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/alerts/lang:DL/pws:1/q/pws:ibadenwr274.json")

# JSON-Strukturen parsen und anlegen
print "verarbeite JSON"
aktD = akt.json()
vorD = vor.json()
astD = ast.json()
alD = al.json()

# Zeitstempel der Wetterdaten holen, parsen und in deutsches Format wandeln
zeitRoh = email.utils.parsedate_tz(aktD['current_observation']['observation_time_rfc822'])
TjWTag = time.strftime("%A", time.gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))
TjZeit = time.strftime("%H:%M", time.gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))

# Icons holen, vorher alte löschen
print "lösche alte Icons"
for filename in glob("*.gif"):
    os.remove(filename)
print "hole Icons"
iconUrlIj = aktD['current_observation']['icon_url'] # IconUrl holen
iconUrlIj = iconUrlIj.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameIj = wget.download(iconUrlIj)                        # Icon dowloaden

iconUrlI0 = vorD['forecast']['simpleforecast']['forecastday'][0]['icon_url'] # IconUrl holen
iconUrlI0 = iconUrlI0.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI0 = wget.download(iconUrlI0)                        # Icon dowloaden

iconUrlI1 = vorD['forecast']['simpleforecast']['forecastday'][1]['icon_url'] # IconUrl holen
iconUrlI1 = iconUrlI1.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI1 = wget.download(iconUrlI1)                        # Icon dowloaden

iconUrlI2 = vorD['forecast']['simpleforecast']['forecastday'][2]['icon_url'] # IconUrl holen
iconUrlI2 = iconUrlI2.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI2 = wget.download(iconUrlI2)                        # Icon dowloaden

iconUrlI3 = vorD['forecast']['simpleforecast']['forecastday'][3]['icon_url'] # IconUrl holen
iconUrlI3 = iconUrlI3.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI3 = wget.download(iconUrlI3)                        # Icon dowloaden

# Fenster bauen
print "baue Fenster"
window = Tk()
window.overrideredirect(True)
window.geometry("480x320+0+0")

imgIj = PhotoImage(file = filenameIj)                               # Icon-Datei öffnen
mondI = PhotoImage(file = './mond.pgm')
sonneI = PhotoImage(file = './sonne.pgm')
tropfenI = PhotoImage(file = './tropfen.pgm')
druckI = PhotoImage(file = './druck.pgm')
windI = PhotoImage(file = './wind.pgm')
schneeI = PhotoImage(file = './schnee.pgm')
regenI = PhotoImage(file = './regen.pgm')
imgI0 = PhotoImage(file = filenameI0)                               # Icon-Datei öffnen
imgI1 = PhotoImage(file = filenameI1)                               # Icon-Datei öffnen
imgI2 = PhotoImage(file = filenameI2)                               # Icon-Datei öffnen
imgI3 = PhotoImage(file = filenameI3)                               # Icon-Datei öffnen

Tj = Text(window, relief = 'flat', bd = 0, bg = BGCOLOR)
TjI = Text(window, relief = 'flat', bd = 0)
TjI.image_create(END, image=imgIj)
Tj.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), tabs = ('1c', CENTER))
Tj.tag_configure('zusatzUeb', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('1c', CENTER, '20c', LEFT))
Tj.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,5c'))
Tj.tag_configure('tempHeiss', font=("Arial", SCHRIFTGROESSE + 7, 'bold'), foreground ='darkred', tabs = ('2,5c'))
Tj.tag_configure('tempKalt', font=("Arial", SCHRIFTGROESSE + 7, 'bold'), foreground ='darkblue', tabs = ('2,5c'))
Tj.tag_configure('tempNormal', font=("Arial", SCHRIFTGROESSE + 7, 'bold'), foreground ='darkgreen', tabs = ('2,5c'))
Tj.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,5c'))
Tj.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('2,5c'))

T0 = Text(window, relief = 'flat', bd = 0, bg = BGCOLOR)
T0I = Text(window, relief = 'flat', bd = 0)
T0I.image_create(END, image=imgI0)
T0.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'), tabs = ('2,5c', '6c'))
T0.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,5c', '6c'))
T0.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,5c', '6c'))
T0.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('2,5c', '6c'))

T1 = Text(window, relief = 'flat', bd = 0, bg = BGCOLOR)
T1I = Text(window, relief = 'flat', bd = 0)
T1I.image_create(END, image=imgI1)
T1.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T1.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T1.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2))
T1.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')

T2 = Text(window, relief = 'flat', bd = 0, bg = BGCOLOR)
T2I = Text(window, relief = 'flat', bd = 0)
T2I.image_create(END, image=imgI2)
T2.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T2.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T2.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2))
T2.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')

T3 = Text(window, relief = 'flat', bd = 0, bg = BGCOLOR)
T3I = Text(window, relief = 'flat', bd = 0)
T3I.image_create(END, image=imgI3)
T3.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T3.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T3.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2))
T3.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')

# Beenden Knopf
button = Button(master=window, text="X", bg=BGCOLOR, fg="white", command=window.destroy)

# Labels in Fenster einbauen und anordnen
Tj.place(x = 0, y = 0, width = 480, height = 135)
T0.place(x = 0, y = 130, width = 480, height = 100)
T1.place(x = 0, y = 230, width = 160, height = 90)
T2.place(x = 160, y = 230, width = 160, height = 90)
T3.place(x = 320, y = 230, width = 160, height = 90)
TjI.place(x = 25, y = 50, width = 50, height = 50)
T0I.place(x = 25, y = 160, width = 50, height = 50)
T1I.place(x = 0, y = 245, width = 50, height = 50)
T2I.place(x = 160, y = 245, width = 50, height = 50)
T3I.place(x = 320, y = 245, width = 50, height = 50)
button.place(x = 460, y = 300, width = 20, height = 20)

print "erzeuge Texte"
# Wetter jetzt
Tj.insert(INSERT, '\t' + TjWTag, 'ueberschrift')
Tj.insert(INSERT, '  letzte Aktualisierung ' + TjZeit +' Uhr\n', 'zusatz')
if aktD['current_observation']['temp_c'] > 20:
    Tj.insert(END, '\t' + str(aktD['current_observation']['temp_c']) + u"°C ", 'tempHeiss')
elif aktD['current_observation']['temp_c'] < 0:
    Tj.insert(END, '\t' + str(aktD['current_observation']['temp_c']) + u"°C ", 'tempKalt')
else:
    Tj.insert(END, '\t' + str(aktD['current_observation']['temp_c']) + u"°C ", 'tempNormal')
Tj.insert(END,   u'fühlt sich an wie ' + aktD['current_observation']['feelslike_c'] + u"°C\n", 'zusatz')

# Luftfeuchtigkeit jetzt
Tj.insert(END, '\t', 'normal')
Tj.image_create(END, image=tropfenI)
Tj.insert(END, ' ' + aktD['current_observation']['relative_humidity'] + '\n', 'normal')

# Luftdruck jetzt und Tendenz
Tj.insert(END, '\t', 'normal')
Tj.image_create(END, image=druckI)
Tj.insert(END, ' ' + aktD['current_observation']['pressure_mb'] + 'mbar ', 'zusatz')
if aktD['current_observation']['pressure_trend'] == '+':
    Tj.insert(END,'steigend\n', 'zusatz')
elif aktD['current_observation']['pressure_trend'] == '-':
    Tj.insert(END, 'fallend\n', 'zusatz')
else:
    Tj.insert(END, 'gleichbleibend\n', 'zusatz')

# Wind jetzt
Tj.insert(END, '\t', 'zusatz')
Tj.image_create(END, image=windI)
if aktD['current_observation']['wind_kph'] > 0:
    Tj.insert(END, ' ' + str(aktD['current_observation']['wind_kph']) + "km/h aus Richtung ", 'zusatz')
    Tj.insert(END, aktD['current_observation']['wind_dir'], 'zusatz')
else:
    Tj.insert(END, ' 0 km/h', 'zusatz')

# Vorhersage heute
T0.insert(INSERT, u' Vorhersage für heute\n', 'ueberschrift')
T0.insert(END, ' ','normal')
# Mond heute
T0.insert(END, '\t\t', 'zusatz')
T0.image_create(END, image = mondI)
if astD['moon_phase']['percentIlluminated'] == u'0':
    T0.insert(END, ' Neumond\n', 'zusatz')
elif astD['moon_phase']['percentIlluminated'] == u'100':
    T0.insert(END, ' Vollmond\n','zusatz')
else:
    T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
# Temperaturen
T0.insert(END, '\t' +  vorD['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C - ", 'normal')
T0.insert(END, ' ' + vorD['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C",'normal')
# Sonne
T0.insert(END, '\t', 'zusatz')
T0.image_create(END, image= sonneI)
T0.insert(END, ' ' + astD['sun_phase']['sunrise']['hour'] + ":"+astD['sun_phase']['sunrise']['minute'], 'zusatz')
T0.insert(END, ' - ' + astD['sun_phase']['sunset']['hour'] + ":" + astD['sun_phase']['sunset']['minute']+'\n', 'zusatz')
# Niederschlag heute
if vorD['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
    T0.insert(END, '\t\t', 'zusatz')
    T0.image_create(END, image = regenI)
    T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']),'zusatz')
    T0.insert(END, 'mm','zusatz')
else:
    T0.insert(END, '\t\t', 'zusatz')
    T0.image_create(END, image = schneeI)
    T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm']),'zusatz')
    T0.insert(END, 'cm Schnee','zusatz')

# Vorhersage morgen
T1.insert(INSERT, 'Morgen\n', 'ueberschrift')
T1.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C\n", 'normal')
T1.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C\n", 'normal')
if vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
    T1.image_create(END, image = regenI)
    T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm']),'zusatz')
    T1.insert(END, 'mm','zusatz')
else:
    T1.image_create(END, image = schneeI)
    T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm']),'zusatz')
    T1.insert(END, 'cm Schnee','zusatz')

# Vorhersage übermorgen
T2.insert(INSERT, vorD['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + '\n', 'ueberschrift')
T2.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C\n", 'normal')
T2.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C\n", 'normal')
if vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
    T2.image_create(END, image = regenI)
    T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm']),'zusatz')
    T2.insert(END, 'mm','zusatz')
else:
    T2.image_create(END, image = schneeI)
    T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm']),'zusatz')
    T2.insert(END, 'cm Schnee','zusatz')

# Vorhersage überübermorgen
T3.insert(INSERT, vorD['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + '\n', 'ueberschrift')
T3.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C\n", 'normal')
T3.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C\n", 'normal')
if vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
    T3.image_create(END, image = regenI)
    T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm']),'zusatz')
    T3.insert(END, 'mm','zusatz')
else:
    T3.image_create(END, image = schneeI)
    T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm']),'zusatz')
    T3.insert(END, 'cm Schnee','zusatz')

# Fensterloop
print "zeige Fenster"
window.mainloop()
