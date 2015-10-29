from datetime import date
from datetime import timezone

from icalendar import Calendar

import lista


def tiedotArray(data):
    today = date.today()
    listaDict = lista.listaDict()
    tapahtumat = []

    # try:
    tekstina = data.text
    cal = Calendar.from_ical(tekstina)
    for tapahtuma in cal.walk('vevent'):
        if tapahtuma.get('location') is not None:
            tapahtumaLyh = tapahtuma.get('location')[:2]
        if tapahtumaLyh in listaDict:
            print(tapahtumaLyh)
            tapahtumat.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': listaDict[tapahtumaLyh]['lat'],
                               'lon': listaDict[tapahtumaLyh]['lon']})
        else:
            print(tapahtumaLyh)
            tapahtumat.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': 0,
                               'lon': 0})
            # ecept:
            #   print("virhe")

    tiedot = [
        {
            'paikka': 'Ag C231',
            'aika': '20150928T051500Z',
            'kuvaus': 'TIEA207 TIEA207 projektikurssin aloitustapaaminen'
        }
    ]
    return tapahtumat


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
