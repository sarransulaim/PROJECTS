from tkinter import *

import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

root=Tk()
root.title("Rogster's Phone Number Tracker")
root.geometry("650x780")
root.resizable(False,False)

def track():
    enter_number=entry.get()
    number=phonenumbers.parse(enter_number)

    #country
    locate = geocoder.description_for_number(number,'en')
    country.config(text=locate)

    #operater
    operator = carrier.name_for_number(number,"en")
    sim.config(text=operator)

    #phone timezone
    time = timezone.time_zones_for_number(number)
    zone.config(text=time)

    #longitude and latitude
    geolocater = Nominatim(user_agent="geoapiExercises")
    location = geolocater.geocode(locate)

    lng = location.longitude
    lat = location.latitude
    longitude.config(text=lng)
    latitude.config(text=lat)

    #time showing in phone
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude,lat=location.latitude)

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M:%p")
    clock.config(text=current_time)

#logo
logo=PhotoImage(file="logo image.png")
Label(root,image=logo).place(x=270,y=60)

Heading=Label(root,text="Track Number's Like Never Before",font=("arial",18,"bold"))
Heading.place(x=120,y=160)

#Entry
Entry_back=PhotoImage(file="search png.png")
Label(root,image=Entry_back).place(x=150,y=190)

entry=StringVar()
entry_number=Entry(root,textvariable=entry,width=17,bd=0,font=("arial",20),justify="center")
entry_number.place(x=185,y=220)

#button
Search_image=PhotoImage(file="search.png")
search=Button(image=Search_image,borderwidth=0,cursor="hand2",bd=0,font=("arial,16"),command=track)
search.place(x=168,y=280)

#background
Box=PhotoImage(file="background.png")
Label(root,image=Box).place(x=-30,y=355)

country=Label(root,text="Country:",fg="skyblue",font=("arial",15,"bold"))
country.place(x=50,y=500)

sim=Label(root,text="Sim:",bg="#b9ebff",fg="black",font=("arial",15,"bold"))
sim.place(x=370,y=500)

zone=Label(root,text="TimeZone:",fg="skyblue",font=("arial",15,"bold"))
zone.place(x=50,y=600)

clock=Label(root,text="Phone Time:",bg="#a5e5ff",fg="black",font=("arial",15,"bold"))
clock.place(x=370,y=600)

longitude=Label(root,text="Longitude:",fg="skyblue",font=("arial",15,"bold"))
longitude.place(x=50,y=700)

latitude=Label(root,text="Latitude:",bg="#a5e5ff",fg="black",font=("arial",15,"bold"))
latitude.place(x=370,y=700)





root,mainloop()