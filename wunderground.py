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
SCHRIFTGROESSE = 11

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

# Zeitstempel der Wetterdaten holen, parsen und in deutsches Format wandeln
locale.setlocale(locale.LC_ALL,'')
zeitRoh = email.utils.parsedate_tz(aktuellData['current_observation']['observation_time_rfc822'])
zeitTj = time.strftime("%A %H:%M", time.gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))

# Icons holen, vorher alte löschen
print "lösche alte Icons"
for filename in glob("*.gif"):
    os.remove(filename)
print "hole Icons"
iconUrlIj = aktuellData['current_observation']['icon_url'] # IconUrl holen
iconUrlIj = iconUrlIj.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameIj = wget.download(iconUrlIj)                        # Icon dowloaden

iconUrlI0 = vorhersageData['forecast']['simpleforecast']['forecastday'][0]['icon_url'] # IconUrl holen
iconUrlI0 = iconUrlI0.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI0 = wget.download(iconUrlI0)                        # Icon dowloaden
imgI0 = Image.open(filenameI0)                               # Icon-Datei öffnen

iconUrlI1 = vorhersageData['forecast']['simpleforecast']['forecastday'][1]['icon_url'] # IconUrl holen
iconUrlI1 = iconUrlI1.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI1 = wget.download(iconUrlI1)                        # Icon dowloaden
imgI1 = Image.open(filenameI1)                               # Icon-Datei öffnen

iconUrlI2 = vorhersageData['forecast']['simpleforecast']['forecastday'][2]['icon_url'] # IconUrl holen
iconUrlI2 = iconUrlI2.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI2 = wget.download(iconUrlI2)                        # Icon dowloaden
imgI2 = Image.open(filenameI2)                               # Icon-Datei öffnen

iconUrlI3 = vorhersageData['forecast']['simpleforecast']['forecastday'][3]['icon_url'] # IconUrl holen
iconUrlI3 = iconUrlI3.replace("/k/", "/j/")                  # Art des Icons tauschen
filenameI3 = wget.download(iconUrlI3)                        # Icon dowloaden
imgI3 = Image.open(filenameI3)                               # Icon-Datei öffnen

# Fenster bauen
print "baue Fenster"
window = Tk()
window.overrideredirect(True)
window.geometry("480x320+0+0")
imgIj = PhotoImage(filenameIj)                               # Icon-Datei öffnen

#imgTkIj = ImageTk.PhotoImage(imgIj)                          # Icon-Datei in Grafikobjekt laden
imgTkI0 = ImageTk.PhotoImage(imgI0)                          # Icon-Datei in Grafikobjekt laden
imgTkI1 = ImageTk.PhotoImage(imgI1)                          # Icon-Datei in Grafikobjekt laden
imgTkI2 = ImageTk.PhotoImage(imgI2)                          # Icon-Datei in Grafikobjekt laden
imgTkI3 = ImageTk.PhotoImage(imgI3)                          # Icon-Datei in Grafikobjekt laden

frame = Frame(master=window, bg=BGCOLOR)
labelTj = Label(master=frame, bg=BGCOLOR, font=("Arial", SCHRIFTGROESSE), fg="black", justify=LEFT, anchor = W)
labelT0 = Label(master=frame, bg=BGCOLOR, font=("Arial", SCHRIFTGROESSE), fg="black", justify=LEFT, anchor = W)
labelT1 = Label(master=frame, bg=BGCOLOR, font=("Arial", SCHRIFTGROESSE), fg="black", justify=LEFT, anchor = W)
labelT2 = Label(master=frame, bg=BGCOLOR, font=("Arial", SCHRIFTGROESSE), fg="black", justify=LEFT, anchor = W)
labelT3 = Label(master=frame, bg=BGCOLOR, font=("Arial", SCHRIFTGROESSE), fg="black", justify=LEFT, anchor = W)
#labelIj = Label(master=frame, bg=BGCOLOR, image=imgTkIj)    # Grafikobjekt in Label einbauen
labelI0 = Label(master=frame, bg=BGCOLOR, image=imgTkI0)    # Grafikobjekt in Label einbauen
labelI1 = Label(master=frame, bg=BGCOLOR, image=imgTkI1)    # Grafikobjekt in Label einbauen
labelI2 = Label(master=frame, bg=BGCOLOR, image=imgTkI2)    # Grafikobjekt in Label einbauen
labelI3 = Label(master=frame, bg=BGCOLOR, image=imgTkI3)    # Grafikobjekt in Label einbauen

Tj = Text(window)
Tj.tag_configure('Ueberschrift', font=("Arial", SCHRIFTGROESSE + 1, 'bold'))
Tj.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
Tj.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 1))
Tj.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')
T0 = Text(window)
T0.tag_configure('Ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T0.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T0.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 1))
T0.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')
T1 = Text(window)
T1.tag_configure('Ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T1.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T1.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 1))
T1.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')
T2 = Text(window)
T2.tag_configure('Ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T2.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T2.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 1))
T2.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')
T3 = Text(window)
T3.tag_configure('Ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T3.tag_configure('normal', font=("Arial", SCHRIFTGROESSE))
T3.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 1))
T3.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue')

# Beenden Knopf
button = Button(master=frame, text="X", bg=BGCOLOR, fg="white", command=window.destroy)

# Labels in Fenster einbauen und anordnen
frame.pack(expand=True, fill=BOTH)
Tj.place(x = 0, y = 0, width = 475, height = 135)
labelT0.place(x = 9, y = 135, width = 475, height = 80)
labelT1.place(x = 9, y = 230, width = 150, height = 80)
labelT2.place(x = 169, y = 230, width = 150, height = 80)
labelT3.place(x = 329, y = 230, width = 150, height = 80)
#labelIj.place(x = 9, y = 32, width = 50, height = 50)
labelI0.place(x = 9, y = 150, width = 50, height = 50)
labelI1.place(x = 9, y = 248, width = 50, height = 50)
labelI2.place(x = 169, y = 248, width = 50, height = 50)
labelI3.place(x = 329, y = 248, width = 50, height = 50)
button.place(x = 460, y = 300, width = 20, height = 20)

print "erzeuge Texte"
# Wetter jetzt
Tj.insert(INSERT, 'Wetter am ' + zeitTj +' Uhr\n', 'Ueberschrift')
Tj.image_create(END, image=imgIj)
Tj.insert(END,str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt wie ", 'normal')
Tj.insert(END, aktuellData['current_observation']['feelslike_c'] + u"°C\n", 'normal')
# Luftfeuchtigkeit jetzt
Tj.insert(END, 'Feuchtigkeit ', 'normal')
Tj.insert(END, aktuellData['current_observation']['relative_humidity'] + '\n', 'blau')
# Luftdruck jetzt und Tendenz
Tj.insert(END, 'Luftdruck ' + aktuellData['current_observation']['pressure_mb'] + 'mbar ', 'normal')
if aktuellData['current_observation']['pressure_trend'] == '+':
    Tj.insert(END,'steigend\n', 'normal')
elif aktuellData['current_observation']['pressure_trend'] == '-':
    Tj.insert(END, 'fallend\n', 'normal')
else:
    Tj.insert(END, 'gleichbleibend\n', 'normal')
# Wind jetzt
if aktuellData['current_observation']['wind_kph'] > 0:
    Tj.insert(END, 'Wind aus Richtung ' + aktuellData['current_observation']['wind_dir'] + ' mit ', 'zusatz')
    Tj.insert(END, str(aktuellData['current_observation']['wind_kph']) + "km/h", 'zusatz')
else:
    Tj.insert(END, 'Es ist windstill', 'zusatz')

# Vorhersage heute
T0  = 'Heute\n'
T0 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C\t"
# Mond heute
if astronomieData['moon_phase']['percentIlluminated'] == u'0':
    T0 += 'Mond als Neumond nicht sichtbar\n'
elif astronomieData['moon_phase']['percentIlluminated'] == u'100':
    T0 += 'Vollmond\n'
else:
    T0 += astronomieData['moon_phase']['phaseofMoon'] + ', Mond zu '
    T0 += astronomieData['moon_phase']['percentIlluminated'] + '% '
    T0 += 'sichtbar\n'
T0 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C\t"
T0 += 'Sonne geht ' + astronomieData['sun_phase']['sunrise']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunrise']['minute']
T0 += ' auf und ' + astronomieData['sun_phase']['sunset']['hour'] + \
                  ":" + astronomieData['sun_phase']['sunset']['minute'] + ' unter\n'
# Niederschlag heute
if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
        #heuteText += 'und es soll trocken bleiben.\n'
        T0 += 'trocken'
    else:
        T0 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'])
        T0 += 'mm Regen'
else:
    T0 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'])
    T0 += 'cm Schnee'

# Vorhersage morgen
T1  = 'Morgen\n'
T1 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C\n"
T1 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C\n"
if vorhersageData['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'] == 0:
        T1 += 'trocken'
    else:
        T1 += 'und ' + str(vorhersageData['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'])
        T1 += 'mm Regen.'
else:
    T1 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'])
    T1 += 'cm Schnee.'

# Vorhersage übermorgen
T2 = vorhersageData['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + '\n'
T2 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C\n"
T2 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C\n"
if vorhersageData['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'] == 0:
        T2 += 'trocken'
    else:
        T2 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'])
        T2 += 'mm Regen.'
else:
    T2 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'])
    T2 += 'cm Schnee.'

# Vorhersage überübermorgen
T3 = vorhersageData['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + '\n'
T3 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C\n"
T3 += '\t' + vorhersageData['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C\n"
if vorhersageData['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
    if vorhersageData['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'] == 0:
        T3 += 'trocken'
    else:
        T3 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'])
        T3 += 'mm Regen.'
else:
    T3 += str(vorhersageData['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'])
    T3 += 'cm Schnee.'

# Textlabels für das Fenster zusammensetzen
labelTj.config(text=Tj)
labelT0.config(text=T0)
labelT1.config(text=T1)
labelT2.config(text=T2)
labelT3.config(text=T3)

# Fensterloop
print "zeige Fenster"
window.mainloop()
