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
SCHRIFTGROESSE = 13

stopZeitLoop = FALSE
TjWTag = ''
filenameIj = ''
t = localtime()
tj = localtime()
aktD = {}
alD = {}
gelberText = u'Das Wetter ist potenziell gefährlich. Die vorhergesagten Wetterphänomene sind nicht wirklich ungewöhnlich, aber eine erhöhte Aufmerksamkeit ist angebracht. Gehen Sie keine vermeidbaren Risiken ein.'
orangerText = u'Das Wetter ist gefährlich. Ungewöhnliche meteorologische Phänomene wurden vorhergesagt. Schäden und Unfälle sind wahrscheinlich. Seien Sie sehr aufmerksam und vorsichtig.'
roterText = u'Das Wetter ist sehr gefährlich. Ungewöhnlich intensive meteorologische Phänomene wurden vorhergesagt. Extreme Schäden und Unfälle, oft über größere Flächen, bedrohen Leben sowie Hab und Gut.'

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
    def run(self):
        print "Starte " + self.name
        ZeitLoop(1)
        print "Beende " + self.name


def beenden():
    global stopZeitLoop
    stopZeitLoop = TRUE
    thread1.join()
    window.destroy()

def alarmText():
    global alD
    print "erzeuge Alarm Texte"
    buttonAlarm.config(text='zurück', bg='white', fg='black', command=jetzt)
    Tj.delete(1.0, END)
    #if len(alD['alerts'])
    TjI.place(x = 25,  y = 50,  width = 0,  height = 0 )
    Tj.insert(INSERT, '\t' + 'Alarm 1\n', 'ueberschrift')

    Tj.insert(END, u(alD['alerts'][0]['message'])+'\n','normal')
    if alD['alerts'][0]['level_meteoalarm_name'] == 'Yellow':
        Tj.config(bg='yellow')
        Tj.insert(END, gelberText, 'zusatz')
    elif alD['alerts'][0]['level_meteoalarm_name'] == 'Orange':
        Tj.config(bg='orange')
        Tj.insert(END, orangerText, 'zusatz')
    elif alD['alerts'][0]['level_meteoalarm_name'] == 'Red':
        Tj.insert(END, roterText, 'zusatz')
        Tj.config(bg='red')

def jetzt():
    global TjWTag, t, tj, aktD, aldD, filenameIj
    print "erzeuge Texte für aktuelle Werte je Minute"
    # Wetter jetzt
    Tj.delete(1.0, END)
    Tj.config(bg=BGCOLOR)
    TjI.place(x = 25,  y = 50,  width = 51,  height = 51 )
    Tj.insert(INSERT, '\t' + TjWTag, 'ueberschrift')
    Tj.insert(END, '  letzte Aktualisierung vor ' + str(int((t-tj)/60)) +' Minuten\n', 'zusatz')
    #Tj.insert(END, ' \n', 'leer')
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

    # Wind jetzt und Niederschlag bis jetzt
    Tj.insert(END, '\t', 'zusatz')
    Tj.image_create(END, image=windI)
    if aktD['current_observation']['wind_kph'] > 0:
        Tj.insert(END, ' ' + str(aktD['current_observation']['wind_kph']) + "km/h aus ", 'zusatz')
        Tj.insert(END, aktD['current_observation']['wind_dir'], 'zusatz')
    else:
        Tj.insert(END, ' 0 km/h', 'zusatz')
    Tj.insert(END, ', ', 'zusatz')
    if aktD['current_observation']['precip_today_metric'] == '0':
        Tj.image_create(END, image = trockenI)
    else:
        Tj.image_create(END, image = regenI)
        Tj.insert(END, ' ' + aktD['current_observation']['precip_today_metric'],'zusat')
        Tj.insert(END, 'mm','zusatz')

    # Alarme prüfen und wenn vorhanden den Knopf mit der Anzahl der Alarme anzeigen, sonst Knopf löschen
    if len(alD['alerts']):
        buttonText = str(len(alD['alerts']))
        if len(alD['alerts']) == 1:
             buttonText += ' Alarm'
        else:
            buttonText += ' Alarme'
        buttonAlarm.config(text=buttonText, bg="yellow", fg="black", command=alarmText)
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
Tj.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,5c'))
Tj.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-12))
Tj.tag_configure('tempHeiss', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkred', tabs = ('2,5c', NUMERIC))
Tj.tag_configure('tempKalt', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkblue', tabs = ('2,5c', NUMERIC))
Tj.tag_configure('tempNormal', font=("Arial", SCHRIFTGROESSE + 4, 'bold'), foreground ='darkgreen', tabs = ('2,5c', NUMERIC))
Tj.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,5c'), wrap = WORD)

T0 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T0.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'), tabs = ('2,5c', '5,5c'))
T0.tag_configure('normal', font=("Arial", SCHRIFTGROESSE), tabs = ('2,7c', NUMERIC, '5,5c'))
T0.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-10))
T0.tag_configure('zusatz', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,7c', '5,5c'))
T0.tag_configure('zusatzregen', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,6c', '5,5c'))

T1 = Text(master=window, relief = 'flat', borderwidth = 0, bg = BGCOLOR)
T1.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T1.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T1.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-9))
T1.tag_configure('zusatzregen', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,2c'))

T2 = Text(master=window, relief = 'flat', bd = 0, bg = BGCOLOR)
T2.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T2.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T2.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-9))
T2.tag_configure('zusatzregen', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,2c'))

T3 = Text(master=window, relief = 'flat', bd = 0, bg = BGCOLOR)
T3.tag_configure('ueberschrift', font=("Arial", SCHRIFTGROESSE, 'bold'))
T3.tag_configure('normal', font=("Arial", SCHRIFTGROESSE - 1), tabs = ('2,3c', NUMERIC))
T3.tag_configure('leer', font=("Arial", SCHRIFTGROESSE-9))
T3.tag_configure('zusatzregen', font=("Arial", SCHRIFTGROESSE - 2), tabs = ('2,2c'))

# Formate für die Vorhersagebilder
TjI = Text(master=window, relief = 'flat', borderwidth = 0)
T0I = Text(master=window, relief = 'flat', borderwidth = 0)
T1I = Text(master=window, relief = 'flat', borderwidth = 0)
T2I = Text(master=window, relief = 'flat', borderwidth = 0)
T3I = Text(master=window, relief = 'flat', borderwidth = 0)

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

# Knöpfe
buttonAlarm = Button(master=window, text='', bg="white", fg="black", relief='flat', command=jetzt)
buttonExit = Button(master=window, text="X", bg=BGCOLOR, fg="lightgrey", relief='flat', command=beenden)
buttonAlarm.place(x = 395, y = 0, width = 65, height = 30)
buttonExit.place( x = 460, y = 0, width = 20, height = 20)

# Funktion um entweder einmalig zum Testen (mitLoop = 0) per Funktionsaufruf benutzt zu werden, oder mitLoop = 1
# für die Nutzung in einem separaten Thread, der dann pro Minute die Anzeige aktualisiert (für die Anzeige der
# Minuten seit Aktualisierung) und alle 20 Min (1200 Sekunden) die Daten neu abfragt
def ZeitLoop(mitLoop):
    global TjWTag, t, tj, aktD, alD, filenameIj
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
            #T0.insert(END, ' \n', 'leer')

            # Maxtemperatur
            T0.insert(END, '\t' +  vorD['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'] + u"°C", 'normal')
            # Mond heute
            T0.insert(END, '\t', 'zusatz')
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
            # Mintemperatur
            T0.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'] + u"°C",'normal')
            # Sonne
            T0.insert(END, '\t', 'zusatz')
            T0.image_create(END, image= sonneI)
            T0.insert(END, ' ' + astD['sun_phase']['sunrise']['hour'] + ":"+astD['sun_phase']['sunrise']['minute'], 'zusatz')
            T0.insert(END, ' - ' + astD['sun_phase']['sunset']['hour'] + ":" + astD['sun_phase']['sunset']['minute']+'\n', 'zusatz')
            # Niederschlag heute
            if vorD['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'] == 0:
                    T0.insert(END, '\t', 'zusatzregen')
                    T0.image_create(END, image = trockenI)
                else:
                    T0.insert(END, '\t', 'zusatzregen')
                    T0.image_create(END, image = regenI)
                    T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']),'zusatzregen')
                    T0.insert(END, 'mm','zusatzregen')
            else:
                T0.insert(END, '\t', 'zusatzregen')
                T0.image_create(END, image = schneeI)
                T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm']),'zusatzregen')
                T0.insert(END, 'cm','zusatzregen')
            # Wind heute
            T0.insert(END, '\t', 'zusatz')
            T0.image_create(END, image=windI)
            if vorD['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph'] > 0:
                T0.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph']),'zusatz')
                T0.insert(END, '-' + str(vorD['forecast']['simpleforecast']['forecastday'][0]['maxwind']['kph'])+ "km/h ", 'zusatz')
                T0.insert(END, vorD['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir'], 'zusatz')
            else:
                T0.insert(END, ' 0 km/h', 'zusatz')

            # Vorhersage morgen
            T1.delete(1.0, END)
            T1.insert(INSERT, ' Morgen\n', 'ueberschrift')
            #T1.insert(END, ' \n', 'leer')
            T1.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][1]['high']['celsius'] + u"°C\n", 'normal')
            T1.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][1]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm'] == 0:
                    T1.insert(END, '\t', 'zusatzregen')
                    T1.image_create(END, image = trockenI)
                else:
                    T1.insert(END, '\t', 'zusatzregen')
                    T1.image_create(END, image = regenI)
                    T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['qpf_allday']['mm']),'zusatzregen')
                    T1.insert(END, 'mm','zusatzregen')
            else:
                T1.insert(END, '\t', 'zusatzregen')
                T1.image_create(END, image = schneeI)
                T1.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['cm']),'zusatzregen')
                T1.insert(END, 'cm','zusatzregen')

            # Vorhersage übermorgen
            T2.delete(1.0, END)
            T2.insert(INSERT, ' ' + vorD['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'] + '\n', 'ueberschrift')
            #T2.insert(END, ' \n', 'leer')
            T2.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][2]['high']['celsius'] + u"°C\n", 'normal')
            T2.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][2]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm'] == 0:
                    T2.insert(END, '\t', 'zusatzregen')
                    T2.image_create(END, image = trockenI)
                else:
                    T2.insert(END, '\t', 'zusatzregen')
                    T2.image_create(END, image = regenI)
                    T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['qpf_allday']['mm']),'zusatzregen')
                    T2.insert(END, 'mm','zusatzregen')
            else:
                T2.insert(END, '\t', 'zusatzregen')
                T2.image_create(END, image = schneeI)
                T2.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][2]['snow_allday']['cm']),'zusatzregen')
                T2.insert(END, 'cm','zusatzregen')

            # Vorhersage überübermorgen
            T3.delete(1.0, END)
            T3.insert(INSERT, ' ' + vorD['forecast']['simpleforecast']['forecastday'][3]['date']['weekday'] + '\n', 'ueberschrift')
            #T3.insert(END, ' \n', 'leer')
            T3.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][3]['high']['celsius'] + u"°C\n", 'normal')
            T3.insert(END, '\t' + vorD['forecast']['simpleforecast']['forecastday'][3]['low']['celsius'] + u"°C\n", 'normal')
            if vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm'] == 0.0:
                if vorD['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm'] == 0:
                    T3.insert(END, '\t', 'zusatzregen')
                    T3.image_create(END, image = trockenI)
                else:
                    T3.insert(END, '\t', 'zusatzregen')
                    T3.image_create(END, image = regenI)
                    T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['qpf_allday']['mm']),'zusatzregen')
                    T3.insert(END, 'mm','zusatzregen')
            else:
                T3.insert(END, '\t', 'zusatzregen')
                T3.image_create(END, image = schneeI)
                T3.insert(END, ' ' + str(vorD['forecast']['simpleforecast']['forecastday'][3]['snow_allday']['cm']),'zusatzregen')
                T3.insert(END, 'cm','zusatzregen')

        # jetziges Wetter anzeigen
        jetzt()

        global stopZeitLoop
        if mitLoop:
            c = 60
            while c:
                sleep(1)
                c -= 1
                if stopZeitLoop:
                    break
            if stopZeitLoop:
                break
        else:
            break

# starte Zeitloop in einem weiteren thread
thread1 = myThread(1, "Zeitloop ")
thread1.start()
#ZeitLoop(0)
# Fensterloop
print "Beenden Knopf einbauen und Fenster anzeigen\n"

window.mainloop()
print 'Beende Anzeige'
