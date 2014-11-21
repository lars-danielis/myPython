# -*- coding: utf-8 -*-
import requests
from Tkinter import *

BGCOLOR="#000"

window=Tk()
window.overrideredirect(True)
w=window.winfo_screenwidth()
h=window.winfo_screenheight()
window.geometry(str(w)+"x"+str(h)+"+0+0")
frame=Frame(master=window, bg=BGCOLOR)
label=Label(master=frame,bg=BGCOLOR,font=("Arial",20),fg="white")
button=Button(master=frame,text="X",bg=BGCOLOR,fg="white",command=window.destroy)
frame.pack(expand=True,fill=BOTH)
label.pack(expand=True,fill=BOTH)
button.pack(side=RIGHT)
aktuell = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/conditions/lang:DL/pws:1/q/pws:ibadenwr250.json")
aktuellData = aktuell.json()
vorhersage = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/forecast/lang:DL/pws:1/q/pws:ibadenwr250.json")
vorhersageData = vorhersage.json()
print aktuellData['current_observation']['weather'],
print str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt",
print aktuellData['current_observation']['feelslike_c'] + u"°C bei",
print aktuellData['current_observation']['relative_humidity'], 'Luftfeuchtigkeit.'
print 'Voraussichtlich',
print aktuellData['current_observation']['precip_today_metric'] + "mm Niederschlag."
print 'Luftdruck', aktuellData['current_observation']['pressure_mb'] + 'mbar Tendenz',
print aktuellData['current_observation']['pressure_trend']+"."
print 'Wind aus Richtung', aktuellData['current_observation']['wind_dir'], 'mit',
print str(aktuellData['current_observation']['wind_kph']) + "km/h."
aktuellText = aktuellData['current_observation']['weather']+" "
aktuellText += str(aktuellData['current_observation']['temp_c']) + u"°C gefühlt "
aktuellText += aktuellData['current_observation']['feelslike_c'] + u"°C bei "
aktuellText += aktuellData['current_observation']['relative_humidity']+ ' Luftfeuchtigkeit.\n'
aktuellText += 'Voraussichtlich '+aktuellData['current_observation']['precip_today_metric']
aktuellText += "mm Niederschlag.\n"
aktuellText += 'Luftdruck '+ aktuellData['current_observation']['pressure_mb'] + 'mbar Tendenz '
aktuellText += aktuellData['current_observation']['pressure_trend']+".\n"
aktuellText += 'Wind aus Richtung '+ aktuellData['current_observation']['wind_dir']+ ' mit '
aktuellText += str(aktuellData['current_observation']['wind_kph']) + "km/h."
print
vorhersageText ="\n"
for day in vorhersageData['forecast']['simpleforecast']['forecastday']:
    print day['date']['weekday']
    vorhersageText += day['date']['weekday']+' '
    print day['conditions'], 'zwischen', day['low']['celsius'] + u"°C und",
    vorhersageText += day['conditions']+ ' '+ day['low']['celsius'] + u"°C bis "
    print day['high']['celsius'] + u"°C"
    vorhersageText += day['high']['celsius'] + u"°C\n"
    print
print
for textDay in vorhersageData['forecast']['txt_forecast']['forecastday']:
    print textDay['title']
    print textDay['fcttext_metric']
    print
anzeigeText = aktuellText+vorhersageText
label.config(text=anzeigeText)
window.mainloop()

# alarme = requests.get(
#    "http://api.wunderground.com/api/edc8d609ba28e7c2/alerts/lang:DL/pws:1/q/pws:ibadenwr250.json")
astronomie = requests.get(
    "http://api.wunderground.com/api/edc8d609ba28e7c2/astronomy/lang:DL/pws:1/q/pws:ibadenwr250.json")

#alarmeData = alarme.json()
astronomieData = astronomie.json()



print astronomieData['moon_phase']['phaseofMoon'],
print '(' + astronomieData['moon_phase']['percentIlluminated'] + "%) vom Mond sichtbar."
print 'Die Sonne geht um', astronomieData['sun_phase']['sunrise']['hour'] + \
    ":" + astronomieData['sun_phase']['sunrise']['minute'], "Uhr auf",
print 'und um', astronomieData['sun_phase']['sunset']['hour'] + \
    ":" + astronomieData['sun_phase']['sunset']['minute'], "Uhr unter."
