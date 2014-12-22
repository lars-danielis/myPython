#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Version 2 mit Icons auch für die Vorhersagen
import locale
from time import *
import email.utils
import requests
import wget
from glob import glob
import os
from Tkinter import *
import threading
import sys
#rpi
import Adafruit_DHT

BGCOLOR = "white"
SCHRIFT = "FreeSans"
WEISS   = "#FFF"
#rpi
#SCHRIFTGROESSE = 10 #dell
SCHRIFTGROESSE = 13 #asus und r-pi


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
    def run(self):
        print "Starte " + self.name
        ZeitLoop()
        print "Beende " + self.name

process = myThread(10, 'Zeitprozess')
runZeitLoop = TRUE
TjWTag = ''
filenameIj = ''
t = localtime()
tj = localtime()
json = {}
warte = 60
nummer = 0
gelberText =  u'\nDas Wetter ist potenziell gefährlich. Die vorhergesagten Wetterphänomene sind nicht wirklich ungewöhnlich, aber eine erhöhte Aufmerksamkeit ist angebracht.'
orangerText = u'\nDas Wetter ist gefährlich. Ungewöhnliche meteorologische Phänomene wurden vorhergesagt. Schäden und Unfälle sind wahrscheinlich.'
roterText =   u'\nDas Wetter ist sehr gefährlich. Ungewöhnlich intensive meteorologische Phänomene wurden vorhergesagt. Extreme Schäden und Unfälle bedrohen Leben, Hab und Gut.'

def beenden():
    global runZeitLoop
    print 'beenden eingeleitet'
    runZeitLoop = FALSE
    #thread1.join()
    window.destroy()

def nextAlarm():
    global nummer
    nummer += 1
    alarmText()

def alarmText():
    global json, warte, nummer
    warte = 60
    print "erzeuge Alarm Texte"
    TjI.place(x = 25,  y = 50,  width = 0,  height = 0 )
    T0I.place(x = 25,  y = 160, width = 0,  height = 0 )
    T3I.place(x = 330, y = 253, width = 0,  height = 0 )
    T0.place( x = 0,   y = 130, width = 0, height = 0)
    Tj.place( x = 0,   y = 0,   width = 481, height = 226)
    buttonAlarm.place(x = 320, y = 225, width = 161, height = 97)
    buttonRadar.place(x = 400, y = 130, width = 0,   height = 0 )
    ablaufText = strftime("%A %H:%M Uhr", strptime(json['alerts'][nummer]['expires'],'%Y-%m-%d %H:%M:%S %Z'))
    Tj.delete(1.0, END)
    Tj.insert(INSERT, '\t' + 'Alarm ' + (str(nummer+1)), 'ueberschrift')
    Tj.insert(INSERT, u' gilt bis ' + ablaufText + '\n', 'normal')
    Tj.insert(END, json['alerts'][nummer]['message'].replace(u'&nbsp)', '').replace(u'\n','').replace(u')','').encode('latin'), 'normal')
    if json['alerts'][nummer]['level_meteoalarm_name'] == 'Yellow':
        Tj.config(bg='yellow')
        Tj.insert(END, gelberText, 'zusatz')
    elif json['alerts'][nummer]['level_meteoalarm_name'] == 'Orange':
        Tj.config(bg='orange')
        Tj.insert(END, orangerText, 'zusatz')
    elif json['alerts'][nummer]['level_meteoalarm_name'] == 'Red':
        Tj.config(bg='red')
        Tj.insert(END, roterText, 'zusatz')
    if (nummer + 2) > len(json['alerts']):
        buttonAlarm.config(text='zurück', command=jetzt)
    else:
        buttonAlarm.config(text='Nächster', command=nextAlarm)


def radar():
    print "zeige GIF"
    Tj.delete(1.0, END)
    TjI.place(x = 25,  y = 50,  width = 0,  height = 0 )
    T0I.place(x = 25,  y = 160, width = 0,  height = 0 )
    T1I.place(x = 10,  y = 253, width = 0,  height = 0 )
    T2I.place(x = 170, y = 253, width = 0,  height = 0 )
    T3I.place(x = 330, y = 253, width = 0,  height = 0 )
    T0.place( x = 0,   y = 130, width = 0, height = 0)
    Tj.place( x = 0,   y = 0,   width = 481, height = 226)
    TG.place( x = 0,   y = 0,   width = 480, height = 320)
    buttonAlarm.place(x = 400, y = 178, width = 0, height = 0)
    buttonRadar.config(text='Zurück', command=jetzt)


# Funktion um entweder einmalig zum Testen (mitLoop = 0) per Funktionsaufruf benutzt zu werden, oder mitLoop = 1
# für die Nutzung in einem separaten Thread, der dann pro Minute die Anzeige aktualisiert (für die Anzeige der
# Minuten seit Aktualisierung) und alle 20 Min (1200 Sekunden) die Daten neu abfragt
def ZeitLoop():
    global TjWTag, t, tj, json, json, filenameIj, warte, runZeitLoop
    tl = 0
    while runZeitLoop:

        # aktuelle Zeit holen und prüfen ob die websites neu abgefragt werden sollen - alle 20min bzw. 1200s
        t = mktime(localtime())
        if (t - tl) > 1200:
            tl = t

            # Wunderground JSON-Daten holen
            print "versuche JSON-Daten zu holen ...",
            try:
                jsonRaw = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/forecast/astronomy/alerts/lang:DL/pws:1/q/pws:ibadenwr274.json")
                #rpi
                #json = jsonRaw.json()
                json = jsonRaw.json
                print "erfolgreich"

                print "versuche GIF zu holen ...",
                try:
                    filenameG = wget.download("http://api.wunderground.com/api/edc8d609ba28e7c2/animatedradar/animatedsatellite/lang:DL/q/eislingen.gif?sat.width=480&sat.height=320&rad.width=480&rad.height=320&num=8&delay=25&interval=5&rad.smooth=1")           # GIF downloaden
                    print "erfolgreich"
                except IOError:
                    filenameG = './fehler.pgm'
                    print "keine Verbindung"
                imgG = PhotoImage(file = filenameG)
                TG.delete(1.0, END)
                TG.image_create(INSERT, image=imgG)

                # Zeitstempel der Wetterdaten holen, parsen und in deutsches Format wandeln
                zeitRoh = email.utils.parsedate_tz(json['current_observation']['observation_time_rfc822'])
                tj = mktime(gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))
                TjWTag = strftime("%A", gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))
                #TjZeit = strftime("%H:%M", gmtime(email.utils.mktime_tz(zeitRoh) + zeitRoh[9]))

                # Icons holen,
                # vorher alte löschen
                print "lösche alte Icons"
                for filename in glob("*.gif"):
                    os.remove(filename)
                # holen
                print "hole Jetzt-Icon"
                iconUrlIj = json['current_observation']['icon_url'] # IconUrl holen
                iconUrlIj = iconUrlIj.replace("/k/", "/a/")         # Art des Icons tauschen
                try:
                    filenameIj = wget.download(iconUrlIj)           # Icon dowloaden
                    imgIj = PhotoImage(file = filenameIj)
                    TjI.delete(1.0, END)
                    TjI.image_create(INSERT, image=imgIj)
                except IOError:
                    filenameIj = './fehler.pgm'
                    print "Jetzt-Icon konnte nicht geladen werden"

            except requests.exceptions.ConnectionError:
                print "keine Verbindung"

            print "versuche Icons zu holen ...",
            try:
                iconUrlI0 = json['forecast']['simpleforecast']['forecastday'][0]['icon_url'] # IconUrl holen
                iconUrlI0 = iconUrlI0.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI0 = wget.download(iconUrlI0)                        # Icon dowloaden
                    imgI0 = PhotoImage(file = filenameI0)
                    T0I.delete(1.0, END)
                    T0I.image_create(INSERT, image=imgI0)
                except IOError:
                    filenameI0 = './fehler.pgm'
                    imgI0 = PhotoImage(file = filenameI0)
                    T0I.delete(1.0, END)
                    T0I.image_create(INSERT, image=imgI0)
                    print "Heute-Icon konnte nicht geladen werden"

                iconUrlI1 = json['forecast']['simpleforecast']['forecastday'][1]['icon_url'] # IconUrl holen
                iconUrlI1 = iconUrlI1.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI1 = wget.download(iconUrlI1)                        # Icon dowloaden
                    imgI1 = PhotoImage(file = filenameI1)
                    T1I.delete(1.0, END)
                    T1I.image_create(INSERT, image=imgI1)
                except IOError:
                    filenameI1 = './fehler.pgm'
                    imgI1 = PhotoImage(file = filenameI1)
                    T1I.delete(1.0, END)
                    T1I.image_create(INSERT, image=imgI1)
                    print "Morgen-Icon konnte nicht geladen werden"

                iconUrlI2 = json['forecast']['simpleforecast']['forecastday'][2]['icon_url'] # IconUrl holen
                iconUrlI2 = iconUrlI2.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI2 = wget.download(iconUrlI2)                        # Icon downloaden
                    imgI2 = PhotoImage(file = filenameI2)
                    T2I.delete(1.0, END)
                    T2I.image_create(INSERT, image=imgI2)
                except IOError:
                    filenameI2 = './fehler.pgm'
                    imgI2 = PhotoImage(file = filenameI2)
                    T2I.delete(1.0, END)
                    T2I.image_create(INSERT, image=imgI2)
                    print "Übermorgen-Icon konnte nicht geladen werden"

                iconUrlI3 = json['forecast']['simpleforecast']['forecastday'][3]['icon_url'] # IconUrl holen
                iconUrlI3 = iconUrlI3.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI3 = wget.download(iconUrlI3)                        # Icon downloaden
                    imgI3 = PhotoImage(file = filenameI3)
                    T3I.delete(1.0, END)
                    T3I.image_create(INSERT, image=imgI3)
                except IOError:
                    filenameI3 = './fehler.pgm'
                    imgI3 = PhotoImage(file = filenameI3)
                    T3I.delete(1.0, END)
                    T3I.image_create(INSERT, image=imgI3)
                    print "Überübermorgen-Icon konnte nicht geladen werden"

            except requests.exceptions.ConnectionError:
                print "keine Verbindung"

            print "schreibe Vorhersage Texte je 20min"
            # Vorhersage heute
            T0.delete(1.0, END)
            T0.insert(INSERT, u' Vorhersage für heute\n', 'ueberschrift')
            T0.insert(END, ' \n', 'leer')
            # Maxtemperatur
            T0.insert(END, '\t' +  json['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C", 'normal')
            # Mond heute
            T0.insert(END, '\t', 'zusatz')
            mond = int(json['moon_phase']['percentIlluminated'])
            if mond < 5:
                T0.image_create(END, image = mondI0)
                T0.insert(END, ' Neumond ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif 5 <= mond < 12:
                T0.image_create(END, image = mondI0)
                T0.insert(END, ' ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif 12 <= mond < 37:
                T0.image_create(END, image = mondI1)
                T0.insert(END, ' ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif 37 <= mond < 62:
                T0.image_create(END, image = mondI2)
                T0.insert(END, ' ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif 62 <= mond < 87:
                T0.image_create(END, image = mondI3)
                T0.insert(END, ' ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif 87 <= mond < 95:
                T0.image_create(END, image = mondI4)
                T0.insert(END, ' ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 95:
                T0.image_create(END, image = mondI4)
                T0.insert(END, ' Vollmond ' + json['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            # Mintemperatur
            T0.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C",'normal')
            # Sonne
            T0.insert(END, '\t', 'zusatz')
            T0.image_create(END, image= sonneI)
            T0.insert(END, ' ' + json['sun_phase']['sunrise']['hour'] + ":"+json['sun_phase']['sunrise']['minute'], 'zusatz')
            T0.insert(END, ' - ' + json['sun_phase']['sunset']['hour'] + ":" + json['sun_phase']['sunset']['minute']+'\n', 'zusatz')
            # Niederschlag heute
            if json['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
                if json['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
                    T0.insert(END, '\t', 'zusatzregen')
                    T0.image_create(END, image = trockenI)
                else:
                    T0.insert(END, '\t', 'zusatzregen')
                    T0.image_create(END, image = regenI)
                    T0.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']),'zusatzregen')
                    T0.insert(END, 'mm','zusatzregen')
            else:
                T0.insert(END, '\t', 'zusatzregen')
                T0.image_create(END, image = schneeI)
                T0.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm']),'zusatzregen')
                T0.insert(END, 'cm','zusatzregen')
            # Wind heute
            T0.insert(END, '\t', 'zusatz')
            T0.image_create(END, image=windI)
            if json['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph'] > 0:
                T0.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph']),'zusatz')
                T0.insert(END, '-' + str(json['forecast']['simpleforecast']['forecastday'][0]['maxwind']['kph'])+ "km/h ", 'zusatz')
                T0.insert(END, json['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir'], 'zusatz')
            else:
                T0.insert(END, ' 0 km/h', 'zusatz')

            # Vorhersage morgen
            T1.delete(1.0, END)
            T1.insert(INSERT, ' Morgen\n', 'ueberschrift')
            T1.insert(END, ' \n', 'leer')
            T1.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C\n", 'normal')
            T1.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C\n", 'normal')
            if json['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
                if json['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'] == 0:
                    T1.insert(END, '\t', 'zusatzregen')
                    T1.image_create(END, image = trockenI)
                else:
                    T1.insert(END, '\t', 'zusatzregen')
                    T1.image_create(END, image = regenI)
                    T1.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm']),'zusatzregen')
                    T1.insert(END, 'mm','zusatzregen')
            else:
                T1.insert(END, '\t', 'zusatzregen')
                T1.image_create(END, image = schneeI)
                T1.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm']),'zusatzregen')
                T1.insert(END, 'cm','zusatzregen')

            # Vorhersage übermorgen
            T2.delete(1.0, END)
            T2.insert(INSERT, ' ' + json['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + '\n', 'ueberschrift')
            T2.insert(END, ' \n', 'leer')
            T2.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C\n", 'normal')
            T2.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C\n", 'normal')
            if json['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
                if json['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'] == 0:
                    T2.insert(END, '\t', 'zusatzregen')
                    T2.image_create(END, image = trockenI)
                else:
                    T2.insert(END, '\t', 'zusatzregen')
                    T2.image_create(END, image = regenI)
                    T2.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm']),'zusatzregen')
                    T2.insert(END, 'mm','zusatzregen')
            else:
                T2.insert(END, '\t', 'zusatzregen')
                T2.image_create(END, image = schneeI)
                T2.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm']),'zusatzregen')
                T2.insert(END, 'cm','zusatzregen')

            # Vorhersage überübermorgen
            T3.delete(1.0, END)
            T3.insert(INSERT, ' ' + json['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + '\n', 'ueberschrift')
            T3.insert(END, ' \n', 'leer')
            T3.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C\n", 'normal')
            T3.insert(END, '\t' + json['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C\n", 'normal')
            if json['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
                if json['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'] == 0:
                    T3.insert(END, '\t', 'zusatzregen')
                    T3.image_create(END, image = trockenI)
                else:
                    T3.insert(END, '\t', 'zusatzregen')
                    T3.image_create(END, image = regenI)
                    T3.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm']),'zusatzregen')
                    T3.insert(END, 'mm','zusatzregen')
            else:
                T3.insert(END, '\t', 'zusatzregen')
                T3.image_create(END, image = schneeI)
                T3.insert(END, ' ' + str(json['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm']),'zusatzregen')
                T3.insert(END, 'cm','zusatzregen')

        # jetziges Wetter anzeigen
        jetzt()

        warte = 60
        while warte and runZeitLoop:
            sleep(1)
            warte -= 1
    print 'beende Zeitloop'

def jetzt():
    global TjWTag, t, tj, json, filenameIj, nummer
    print "erzeuge Texte für aktuelle Werte je Minute"
    # Wetter jetzt
    nummer = 0
    Tj.config(bg=BGCOLOR)
    TjI.place(x = 25,  y = 50,  width = 51,  height = 51 )
    T0I.place(x = 25,  y = 160, width = 51,  height = 51 )
    T1I.place(x = 10,  y = 253, width = 51,  height = 51 )
    T2I.place(x = 170, y = 253, width = 51,  height = 51 )
    T3I.place(x = 330, y = 253, width = 51,  height = 51 )
    T0.place( x = 0,   y = 130, width = 481, height = 100)
    Tj.place( x = 0,   y = 0,   width = 481, height = 135)
    TG.place( x = 0,   y = 0,   width = 0, height = 0)
    buttonAlarm.place(x = 400, y = 178, width = 80, height = 48)
    buttonRadar.place(x = 400, y = 130, width = 80, height = 49)
    buttonRadar.config(text='Radar', command=radar)
    #rpi
    feuchteInnen, temperaturInnen = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,26)
    #feuchteInnen = 0.0; temperaturInnen = 0.0
    if feuchteInnen is None and temperaturInnen is None:
        feuchteInnen = 0.0; temperaturInnen = 0.0
    Tj.delete(1.0, END)
    Tj.insert(INSERT, '\t' + TjWTag, 'ueberschrift')
    Tj.insert(END, '  letzte Aktualisierung vor ' + str(int((t-tj)/60)) +' Minuten\n', 'zusatz')

    Tj.insert(END, ' \n', 'leer')

    if json['current_observation']['temp_c'] > 20:
        Tj.insert(END, '\t' + str(json['current_observation']['temp_c']) + u"°C ", 'tempHeiss')
    elif json['current_observation']['temp_c'] < 0:
        Tj.insert(END, '\t' + str(json['current_observation']['temp_c']) + u"°C ", 'tempKalt')
    else:
        Tj.insert(END, '\t' + str(json['current_observation']['temp_c']) + u"°C ", 'tempNormal')
    Tj.insert(END,   u'fühlt sich an wie ' + json['current_observation']['feelslike_c'] + u"°C", 'zusatz')
    Tj.insert(END, '\t', 'tempNormal')
    Tj.image_create(END, image=hausI)
    Tj.insert(END, '\t{0:0.1f}'.format(temperaturInnen)+ u'°C\n', 'tempNormal')

    Tj.insert(END, ' \n', 'leer')

    # Luftfeuchtigkeit jetzt
    Tj.insert(END, '\t', 'normal')
    Tj.image_create(END, image=tropfenI)
    Tj.insert(END, ' ' + json['current_observation']['relative_humidity'], 'normal')
    Tj.insert(END, '\t', 'normal')
    if 60 >= feuchteInnen >= 40:
        Tj.image_create(END, image=frohI)
    else:
        Tj.image_create(END, image=traurigI)
    Tj.insert(END, '\t{0:0.1f}'.format(feuchteInnen)+ u"%\n", 'tempKalt')

    # Luftdruck jetzt und Tendenz
    Tj.insert(END, '\t', 'normal')
    Tj.image_create(END, image=druckI)
    Tj.insert(END, ' ' + json['current_observation']['pressure_mb'] + 'mbar ', 'normal')
    if json['current_observation']['pressure_trend'] == '+':
        Tj.image_create(END, image=hochI)
        Tj.insert(END, '\n', 'normal')
    elif json['current_observation']['pressure_trend'] == '-':
        Tj.image_create(END, image=runterI)
        Tj.insert(END, '\n', 'normal')
    else:
        Tj.insert(END, '\n', 'normal')

    # Wind jetzt und Niederschlag bis jetzt
    #Tj.insert(END, '\t', 'zusatz')
    #Tj.image_create(END, image=windI)
    #if json['current_observation']['wind_kph'] > 0:
    #    Tj.insert(END, ' ' + str(json['current_observation']['wind_kph']) + "km/h aus ", 'zusatz')
    #    Tj.insert(END, json['current_observation']['wind_dir'], 'zusatz')
    #else:
    #    Tj.insert(END, ' 0 km/h', 'zusatz')
    #Tj.insert(END, ', ', 'zusatz')
    #if json['current_observation']['precip_today_metric'] == '0':
    #    Tj.image_create(END, image = trockenI)
    #else:
    #    Tj.image_create(END, image = regenI)
    #    Tj.insert(END, ' ' + json['current_observation']['precip_today_metric'],'zusat')
    #    Tj.insert(END, 'mm','zusatz')

    # Alarme prüfen und wenn vorhanden den Knopf mit der Anzahl der Alarme anzeigen, sonst Knopf löschen
    if len(json['alerts']):
        buttonText = str(len(json['alerts']))
        if len(json['alerts']) == 1:
             buttonText += ' Alarm'
        else:
            buttonText += ' Alarme'
        buttonAlarm.config(text=buttonText, bg="grey", command=alarmText)
    else:
        #buttonAlarm.config(text='Alarm', bg="yellow", fg="black", command=alarmText)
        buttonAlarm.config(text='', bg='white', command = jetzt)

locale.setlocale(locale.LC_ALL,'')

# Fenster anlegen
print "baue Fenster"
window = Tk()
window.overrideredirect(True)
window.geometry("480x320+0+0")

# konstante Icons laden
mondI0   = PhotoImage(file = './mond04.pgm' )
mondI1   = PhotoImage(file = './mond14.pgm' )
mondI2   = PhotoImage(file = './mond24.pgm' )
mondI3   = PhotoImage(file = './mond34.pgm' )
mondI4   = PhotoImage(file = './mond44.pgm' )
sonneI   = PhotoImage(file = './sonne.pgm'  )
tropfenI = PhotoImage(file = './tropfen.pgm')
trockenI = PhotoImage(file = './trocken.pgm')
druckI   = PhotoImage(file = './druck.pgm'  )
windI    = PhotoImage(file = './wind.pgm'   )
schneeI  = PhotoImage(file = './schnee.pgm' )
regenI   = PhotoImage(file = './regen.pgm'  )
hochI    = PhotoImage(file = './hoch.pgm'   )
runterI  = PhotoImage(file = './runter.pgm' )
hausI    = PhotoImage(file = './haus.pgm'   )
frohI    = PhotoImage(file = './froh.pgm'   )
traurigI = PhotoImage(file = './traurig.pgm')

#Formate definieren
Tj = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
Tj.tag_configure('ueberschrift', font=(SCHRIFT, SCHRIFTGROESSE + 4, 'bold'), tabs = ('1c', CENTER))
Tj.tag_configure('tempHeiss',    font=(SCHRIFT, SCHRIFTGROESSE + 4, 'bold'), tabs = ('3c', NUMERIC, '9,3c', '10,6c', NUMERIC), foreground ='darkred')
Tj.tag_configure('tempKalt',     font=(SCHRIFT, SCHRIFTGROESSE + 4, 'bold'), tabs = ('3c', NUMERIC, '9,3c', '10,6c', NUMERIC), foreground ='darkblue')
Tj.tag_configure('tempNormal',   font=(SCHRIFT, SCHRIFTGROESSE + 4, 'bold'), tabs = ('3c', NUMERIC, '9,3c', '10,6c', NUMERIC), foreground ='darkgreen')
Tj.tag_configure('normal',       font=(SCHRIFT, SCHRIFTGROESSE    ),         tabs = ('3c',          '9,3c', '10,6c', NUMERIC), wrap = WORD)
Tj.tag_configure('zusatz',       font=(SCHRIFT, SCHRIFTGROESSE - 2),         tabs = ('3c',          '9,3c', '10,6c', NUMERIC), wrap = WORD)
Tj.tag_configure('leer',         font=(SCHRIFT, SCHRIFTGROESSE -10))

T0 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T0.tag_configure('ueberschrift', font=(SCHRIFT, SCHRIFTGROESSE, 'bold'), tabs = ('2,5c',          '5,5c'))
T0.tag_configure('normal',       font=(SCHRIFT, SCHRIFTGROESSE    ),     tabs = ('2,7c', NUMERIC, '5,5c'))
T0.tag_configure('zusatz',       font=(SCHRIFT, SCHRIFTGROESSE - 2),     tabs = ('2,7c',          '5,5c'))
T0.tag_configure('zusatzregen',  font=(SCHRIFT, SCHRIFTGROESSE - 2),     tabs = ('2,6c',          '5,5c'))
T0.tag_configure('leer',         font=(SCHRIFT, SCHRIFTGROESSE - 8))

T1 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T1.tag_configure('ueberschrift', font=(SCHRIFT, SCHRIFTGROESSE, 'bold'))
T1.tag_configure('normal',       font=(SCHRIFT, SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T1.tag_configure('zusatzregen',  font=(SCHRIFT, SCHRIFTGROESSE - 2), tabs =  '2,2c')
T1.tag_configure('leer',         font=(SCHRIFT, SCHRIFTGROESSE - 9))

T2 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T2.tag_configure('ueberschrift', font=(SCHRIFT, SCHRIFTGROESSE, 'bold'))
T2.tag_configure('normal',       font=(SCHRIFT, SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T2.tag_configure('zusatzregen',  font=(SCHRIFT, SCHRIFTGROESSE - 2), tabs =  '2,2c')
T2.tag_configure('leer',         font=(SCHRIFT, SCHRIFTGROESSE - 9))

T3 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T3.tag_configure('ueberschrift', font=(SCHRIFT, SCHRIFTGROESSE, 'bold'))
T3.tag_configure('normal',       font=(SCHRIFT, SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T3.tag_configure('zusatzregen',  font=(SCHRIFT, SCHRIFTGROESSE - 2), tabs =  '2,2c')
T3.tag_configure('leer',         font=(SCHRIFT, SCHRIFTGROESSE - 9))

# Formate für die Vorhersagebilder
TjI = Text(master=window, relief = 'flat', borderwidth = 0)
T0I = Text(master=window, relief = 'flat', borderwidth = 0)
T1I = Text(master=window, relief = 'flat', borderwidth = 0)
T2I = Text(master=window, relief = 'flat', borderwidth = 0)
T3I = Text(master=window, relief = 'flat', borderwidth = 0)
TG  = Text(master=window, relief = 'flat', borderwidth = 0)

fehler = PhotoImage(file = './fehler.pgm')
TjI.image_create(INSERT, image=fehler)
T0I.image_create(INSERT, image=fehler)
T1I.image_create(INSERT, image=fehler)
T2I.image_create(INSERT, image=fehler)
T3I.image_create(INSERT, image=fehler)

# Text-Labels mit Text in Fenster einbauen und anordnen
Tj.place( x = 0,   y = 0,   width = 481, height = 135)
T0.place( x = 0,   y = 130, width = 481, height = 100)
T1.place( x = 0,   y = 225, width = 161, height = 96 )
T2.place( x = 160, y = 225, width = 161, height = 96 )
T3.place( x = 320, y = 225, width = 161, height = 96 )
TjI.place(x = 25,  y = 50,  width = 51,  height = 51 )
T0I.place(x = 25,  y = 160, width = 51,  height = 51 )
T1I.place(x = 10,  y = 253, width = 51,  height = 51 )
T2I.place(x = 170, y = 253, width = 51,  height = 51 )
T3I.place(x = 330, y = 253, width = 51,  height = 51 )
TG.place( x = 0,   y = 0,   width = 0,   height = 0  )

# Knöpfe
print u'Knoepfe einbauen'
buttonAlarm = Button(master=window, text='',      bg="white", fg="white",     relief='flat', command=jetzt  )
buttonRadar = Button(master=window, text='Radar', bg="white", fg="black",     relief='flat', command=radar  )
buttonExit  = Button(master=window, text="X",     bg=BGCOLOR, fg="lightgrey", relief='flat', command=beenden)
buttonRadar.place(x = 400, y = 130, width = 80, height = 49)
buttonAlarm.place(x = 400, y = 178, width = 80, height = 48)
buttonExit.place( x = 460, y = 0,   width = 20, height = 20)

# starte Zeitloop in einem weiteren thread

print 'Starte Zeit- und Fensterprozess'
process.start()
window.mainloop()
print 'Beende Anzeige'
