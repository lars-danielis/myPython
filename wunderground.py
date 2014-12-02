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

BGCOLOR = "white"
WEISS = "#FFF"
SCHRIFTGROESSE = 10

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
    def run(self):
        print "Starte " + self.name
        ZeitLoop(1)
        print "Beende " + self.name

locale.setlocale(locale.LC_ALL,'')

# Fenster anlegen
print "baue Fenster"
window = Tk()
window.overrideredirect(True)
window.geometry("480x320+0+0")

# konstante Icons laden
mondI0 = PhotoImage(file = './mond04.pgm')
mondI1 = PhotoImage(file = './mond14.pgm')
mondI2 = PhotoImage(file = './mond24.pgm')
mondI3 = PhotoImage(file = './mond34.pgm')
mondI4 = PhotoImage(file = './mond44.pgm')
sonneI = PhotoImage(file = './sonne.pgm')
tropfenI = PhotoImage(file = './tropfen.pgm')
trockenI = PhotoImage(file = './trocken.pgm')
druckI = PhotoImage(file = './druck.pgm')
windI = PhotoImage(file = './wind.pgm')
schneeI = PhotoImage(file = './schnee.pgm')
regenI = PhotoImage(file = './regen.pgm')

#Formate definieren
Tj = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
Tj.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), tabs = ('1c', CENTER))
Tj.tag_configure('zusatzUeb', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('1c', CENTER, '20c', LEFT))
Tj.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,5c'))
Tj.tag_configure('tempHeiss', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkred', tabs = ('2,5c'))
Tj.tag_configure('tempKalt', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkblue', tabs = ('2,5c'))
Tj.tag_configure('tempNormal', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkgreen', tabs = ('2,5c'))
Tj.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,5c'))
Tj.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('2,5c'))

T0 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T0.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'), tabs = ('2,5c', '6c'))
T0.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,5c', '6c'))
T0.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,5c', '6c'))
T0.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('2,5c', '6c'))

T1 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T1.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T1.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('1,8c'))
T1.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-8))
T1.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('1,8c'))
T1.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('1,8c'))

T2 = Text(master=window, relief = 'flat', bd = 0, bg = BGCOLOR)
T2.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'), tabs = ('1,8c'))
T2.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('1,8c'))
T2.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-8))
T2.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('1,8c'))
T2.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('1,8c'))

T3 = Text(master=window, relief = 'flat', bd = 0, bg = BGCOLOR)
T3.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'), tabs = ('1,8c'))
T3.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('1,8c'))
T3.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-8))
T3.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('1,8c'))
T3.tag_configure('blau', font=("Arial", SCHRIFTGROESSE), foreground='blue', tabs = ('1,8c'))

# Formate für die Vorhersagebilder
TjI = Text(master=window, relief = 'flat', borderwidth = 0)
T0I = Text(master=window, relief = 'flat', borderwidth = 0)
T1I = Text(master=window, relief = 'flat', borderwidth = 0)
T2I = Text(master=window, relief = 'flat', borderwidth = 0)
T3I = Text(master=window, relief = 'flat', borderwidth = 0)

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

# Funktion um entweder einmalig zum Testen (mitLoop = 0) per Funktionsaufruf benutzt zu werden, oder mitLoop = 1
# für die Nutzung in einem separaten Thread, der dann pro Minute die Anzeige aktualisiert (für die Anzeige der
# Minuten seit Aktualisierung) und alle 20 Min (1200 Sekunden) die Daten neu abfragt
def ZeitLoop(mitLoop):
    tl = 0
    while True:

        # aktuelle Zeit holen und prüfen ob die websites neu abgefragt werden sollen - alle 20min bzw. 1200s
        t = mktime(localtime())
        if (t - tl) > 1200:
            tl = t

            # Wunderground JSON-Daten holen
            print "versuche aktuelle Werte und Icon zu holen ...",
            try:
                akt = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/lang:DL/pws:1/q/pws:ibadenwr274.json")
                aktD = akt.json()
                print "erfolgreich"

                # Zeitstempel der Wetterdaten holen, parsen und in deutsches Format wandeln
                zeitRoh = email.utils.parsedate_tz(aktD['current_observation']['observation_time_rfc822'])
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
                iconUrlIj = aktD['current_observation']['icon_url'] # IconUrl holen
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

            print "versuche Vorhersagen und Icons zu holen ...",
            try:
                vor = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/forecast/lang:DL/pws:1/q/pws:ibadenwr274.json")
                vorD = vor.json()
                print "erfolgreich"

                print "hole Vorhersage-Icons"
                iconUrlI0 = vorD['forecast']['simpleforecast']['forecastday'][0]['icon_url'] # IconUrl holen
                iconUrlI0 = iconUrlI0.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI0 = wget.download(iconUrlI0)                        # Icon dowloaden
                    imgI0 = PhotoImage(file = filenameI0)
                    T0I.delete(1.0, END)
                    T0I.image_create(INSERT, image=imgI0)
                except IOError:
                    filenameI0 = './fehler.pgm'
                    print "Heute-Icon konnte nicht geladen werden"

                iconUrlI1 = vorD['forecast']['simpleforecast']['forecastday'][1]['icon_url'] # IconUrl holen
                iconUrlI1 = iconUrlI1.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI1 = wget.download(iconUrlI1)                        # Icon dowloaden
                    imgI1 = PhotoImage(file = filenameI1)
                    T1I.delete(1.0, END)
                    T1I.image_create(INSERT, image=imgI1)
                except IOError:
                    filenameI1 = './fehler.pgm'
                    print "Morgen-Icon konnte nicht geladen werden"

                iconUrlI2 = vorD['forecast']['simpleforecast']['forecastday'][2]['icon_url'] # IconUrl holen
                iconUrlI2 = iconUrlI2.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI2 = wget.download(iconUrlI2)                        # Icon downloaden
                    imgI2 = PhotoImage(file = filenameI2)
                    T2I.delete(1.0, END)
                    T2I.image_create(INSERT, image=imgI2)
                except IOError:
                    filenameI2 = './fehler.pgm'
                    print "Übermorgen-Icon konnte nicht geladen werden"

                iconUrlI3 = vorD['forecast']['simpleforecast']['forecastday'][3]['icon_url'] # IconUrl holen
                iconUrlI3 = iconUrlI3.replace("/k/", "/a/")                  # Art des Icons tauschen
                try:
                    filenameI3 = wget.download(iconUrlI3)                        # Icon downloaden
                    imgI3 = PhotoImage(file = filenameI3)
                    T3I.delete(1.0, END)
                    T3I.image_create(INSERT, image=imgI3)
                except IOError:
                    filenameI3 = './fehler.pgm'
                    print "Überübermorgen-Icon konnte nicht geladen werden"


            except requests.exceptions.ConnectionError:
                print "keine Verbindung"

            print "versuche astronomische Werte zu holen ...",
            try:
                ast = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/astronomy/lang:DL/pws:1/q/pws:ibadenwr274.json")
                astD = ast.json()
                print "erfolgreich,"
            except requests.exceptions.ConnectionError:
                print "keine Verbindung"

            print "versuche Alarme zu holen ...",
            try:
                al = requests.get("http://api.wunderground.com/api/edc8d609ba28e7c2/alerts/lang:DL/pws:1/q/pws:ibadenwr274.json")
                alD = al.json()
                print "erfolgreich,"
            except requests.exceptions.ConnectionError:
                print "keine Verbindung"

            print "schreibe Vorhersage Texte je 20min"
            # Vorhersage heute
            T0.delete(1.0, END)
            T0.insert(INSERT, u' Vorhersage für heute\n', 'ueberschrift')
            T0.insert(END, ' ','normal')
            # Mond heute
            T0.insert(END, '\t\t', 'zusatz')
            mond = int(astD['moon_phase']['percentIlluminated'])
            if mond < 5:
                T0.image_create(END, image = mondI0)
                T0.insert(END, ' Neumond ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 5 and mond < 12:
                T0.image_create(END, image = mondI0)
                T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 12 and mond < 37:
                T0.image_create(END, image = mondI1)
                T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 37 and mond < 62:
                T0.image_create(END, image = mondI2)
                T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 62 and mond < 87:
                T0.image_create(END, image = mondI3)
                T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond >= 87 and mond < 95:
                T0.image_create(END, image = mondI4)
                T0.insert(END, ' ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
            elif mond > 95:
                T0.image_create(END, image = mondI4)
                T0.insert(END, ' Vollmond ' + astD['moon_phase']['percentIlluminated'] + '%\n', 'zusatz')
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
                if vorD['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
                    T0.insert(END, '\t\t', 'zusatz')
                    T0.image_create(END, image = trockenI)
                else:
                    T0.insert(END, '\t\t', 'zusatz')
                    T0.image_create(END, image = regenI)
                    T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']),'zusatz')
                    T0.insert(END, 'mm','zusatz')
            else:
                T0.insert(END, '\t\t', 'zusatz')
                T0.image_create(END, image = schneeI)
                T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm']),'zusatz')
                T0.insert(END, 'cm','zusatz')

            # Vorhersage morgen
            T1.delete(1.0, END)
            T1.insert(INSERT, ' Morgen\n', 'ueberschrift')
            T1.insert(END, ' \n', 'leer')
            T1.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C", 'normal')
            T1.insert(END, ' - ' + vorD['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'] == 0:
                    T1.insert(END, '\t', 'zusatz')
                    T1.image_create(END, image = trockenI)
                else:
                    T1.insert(END, '\t', 'zusatz')
                    T1.image_create(END, image = regenI)
                    T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm']),'zusatz')
                    T1.insert(END, 'mm','zusatz')
            else:
                T1.image_create(END, image = schneeI)
                T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm']),'zusatz')
                T1.insert(END, 'cm','zusatz')

            # Vorhersage übermorgen
            T2.delete(1.0, END)
            T2.insert(INSERT, ' ' + vorD['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + '\n', 'ueberschrift')
            T2.insert(END, ' \n', 'leer')
            T2.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C", 'normal')
            T2.insert(END, ' - ' + vorD['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'] == 0:
                    T2.insert(END, '\t', 'zusatz')
                    T2.image_create(END, image = trockenI)
                else:
                    T2.insert(END, '\t', 'zusatz')
                    T2.image_create(END, image = regenI)
                    T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm']),'zusatz')
                    T2.insert(END, 'mm','zusatz')
            else:
                T2.image_create(END, image = schneeI)
                T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm']),'zusatz')
                T2.insert(END, 'cm','zusatz')

            # Vorhersage überübermorgen
            T2.delete(1.0, END)
            T3.insert(INSERT, ' ' + vorD['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + '\n', 'ueberschrift')
            T3.insert(END, ' \n', 'leer')
            T3.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C", 'normal')
            T3.insert(END, ' - ' + vorD['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'] == 0:
                    T3.insert(END, '\t', 'zusatz')
                    T3.image_create(END, image = trockenI)
                else:
                    T3.insert(END, '\t', 'zusatz')
                    T3.image_create(END, image = regenI)
                    T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm']),'zusatz')
                    T3.insert(END, 'mm','zusatz')
            else:
                T3.image_create(END, image = schneeI)
                T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm']),'zusatz')
                T3.insert(END, 'cm','zusatz')

        print "erzeuge Texte für aktuelle Werte je Minute"
        # Wetter jetzt
        Tj.delete(1.0, END)
        Tj.insert(INSERT, '\t' + TjWTag, 'ueberschrift')
        Tj.insert(END, '  letzte Aktualisierung vor ' + str(int((t-tj)/60)) +' Minuten\n', 'zusatz')
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
            Tj.insert(END, ' ' + str(aktD['current_observation']['wind_kph']) + "km/h aus ", 'zusatz')
            Tj.insert(END, aktD['current_observation']['wind_dir'], 'zusatz')
        else:
            Tj.insert(END, ' 0 km/h', 'zusatz')

        if mitLoop:
            sleep(60)
        else:
            break


# starte Zeitloop in einem weiteren thread
thread1 = myThread(1, "Zeitloop ")
thread1.start()
#ZeitLoop(0)
# Fensterloop
print "Beenden Knopf einbauen und Fenster anzeigen\n"

# Beenden Knopf
button = Button(master=window, text="X", bg=BGCOLOR, fg="white", command=window.destroy)
button.place(x = 460, y = 300, width = 20, height = 20)

window.mainloop()
