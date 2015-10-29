from datetime import date
from datetime import timezone

from icalendar import Calendar

import lista


def laitaListaanKaikki(tapahtumat, cal, listaDict, today):
    for tapahtuma in cal.walk('vevent'):
     if tapahtuma.get('dtstart').dt.date() >= today:
            if tapahtuma.get('location') is not None:
                tapahtumaLyh = tapahtuma.get('location')[:2]
            if tapahtumaLyh in listaDict:
                tapahtumat.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': listaDict[tapahtumaLyh]['lat'],
                               'lon': listaDict[tapahtumaLyh]['lon']})
            else:
                tapahtumat.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': 0,
                               'lon': 0})

def laitaListaanTanaanHuomennaYlihuomenna(tapahtumat1, cal, listaDict, paiva):
    for tapahtuma in cal.walk('vevent'):
     if tapahtuma.get('dtstart').dt.date() == paiva:
            if tapahtuma.get('location') is not None:
                tapahtumaLyh = tapahtuma.get('location')[:2]
            if tapahtumaLyh in listaDict:
                tapahtumat1.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': listaDict[tapahtumaLyh]['lat'],
                               'lon': listaDict[tapahtumaLyh]['lon']})
            else:
                tapahtumat1.append({'paikka': tapahtuma.get('location'),
                               'paiva': tapahtuma.get('dtstart').dt.date(),
                               'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                               'kuvaus': tapahtuma.get('summary'),
                               'lat': 0,
                               'lon': 0})


def tiedotArray(data):
    today = date.today()
    listaDict = lista.listaDict()
    kaikkiTapahtumat = []
    #try:
    cal = Calendar.from_ical(data.text)

    laitaListaanKaikki(kaikkiTapahtumat, cal, listaDict, today)

    #ecept:
     #   print("virhe")
    return kaikkiTapahtumat

def tiedotArrayTanaan(data):
    today = date.today()
    listaDict = lista.listaDict()
    tanaanTapahtumat = []
    #try:
    cal = Calendar.from_ical(data.text)

    laitaListaanTanaanHuomennaYlihuomenna(tanaanTapahtumat, cal, listaDict, today)
    #laitaListaanTanaanHuomennaYlihuomenna(tanaanTapahtumat, listaDict, today) TODO: toimimaan???

    #ecept:
     #   print("virhe")
    return tanaanTapahtumat


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)