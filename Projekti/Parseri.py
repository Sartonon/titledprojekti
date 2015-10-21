from icalendar import Calendar
from datetime import date
import urllib
from datetime import timezone
import datetime


def tiedotArray(data):
    today = date.today()
    tapahtumat = []
    try:
        cal = Calendar.from_ical(data.text)
        for tapahtuma in cal.walk('vevent'):
            if tapahtuma.get('dtstart').dt.date() == today:
                tapahtumat.append({'paikka': tapahtuma.get('location'),
                                   'paiva': tapahtuma.get('dtstart').dt.date(),
                                   'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                                   'kuvaus': tapahtuma.get('summary')})
    except urllib.URLError as e:
        print("Website (%s) could not be reached due to %s" % (e.url, e.reason))

    tiedot = [
        {
            'paikka': 'Ag C231',
            'aika' : '20150928T051500Z',
            'kuvaus': 'TIEA207 TIEA207 projektikurssin aloitustapaaminen'
        }
    ]
    return tapahtumat


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)