from icalendar import Calendar
from datetime import date
import time
import datetime


def tiedotArray(data):
    today = date.today()
    tapahtumat = []
    try:
        cal = Calendar.from_ical(data.text)
        for tapahtuma in cal.walk('vevent'):
            if tapahtuma.get('dtstart').dt.date() >= today:
                tapahtumat.append({'paikka': tapahtuma.get('location'),
                                   'paiva': tapahtuma.get('dtstart').dt.date(),
                                   'aika': tapahtuma.get('dtstart').dt.time(),
                                   'kuvaus': tapahtuma.get('summary')})
    except:
        print('virhe parsimisessa')

    tiedot = [
        {
            'paikka': 'Ag C231',
            'aika' : '20150928T051500Z',
            'kuvaus': 'TIEA207 TIEA207 projektikurssin aloitustapaaminen'
        }
    ]
    return tapahtumat
