#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from icalendar import Calendar, Event
from urllib.request import urlopen
import locale

# set fr locale for date conversion
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

page = urlopen('http://mamasound.fr').read()
soup = BeautifulSoup(page, parse_only=SoupStrainer(id="calendar-list"))

cal = Calendar()
cal['summary'] = 'Mamasound calendar'
cpt = 0


def add_event(x):
    event = Event()
    event.add('uid', x["uid"])
    event.add('summary', x["name"])
    event.add('dtstart', datetime.strptime(x["date"], "%d %B %Y %HH%M"))
    event.add('location', x["place"])
    event.add('description', x["price"])
    cal.add_component(event)

for soup in soup.find_all("li"):
    day = soup.strong.a.string
    for soup in soup.find_all("div", class_="list-event"):
        cpt += 1
        hour = soup.b.string
        date = day + " " + hour
        place = soup.a.string
        genre = soup.select("div")[2].select("br")[-1].nextSibling
        name = soup.select(".mc-details")[0].string
        if bool(soup.select("p")) is True:
            price = soup.select("p")[0].string
        else:
            price = ""
        eventdic = {"name": name, "genre": genre.strip(), "date": date, "place": place, "price": price, "uid": cpt}
        add_event(eventdic)

with open('test.ics', mode='wb') as ical:
    ical.write(cal.to_ical())
