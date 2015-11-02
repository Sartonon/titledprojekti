from datetime import date
from datetime import timezone
import datetime
from icalendar import Calendar

import lista


def laitaListaan(tapahtumat, cal, listaDict, paiva=date.today(), kaikki = False):
    tapahtumaLyh = ""
    for tapahtuma in cal.walk('vevent'):
     if tapahtuma.get('dtstart').dt.date() == paiva or kaikki:
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


def tiedotArray(data):
    today = date.today()
    listaDict = lista.listaDict()
    kaikkiTapahtumat = []
    cal = Calendar.from_ical(data.text)
    laitaListaan(kaikkiTapahtumat, cal, listaDict, today, True)
    return kaikkiTapahtumat


def tiedotArrayTanaan(data):
    today = date.today()
    listaDict = lista.listaDict()
    tanaanTapahtumat = []
    cal = Calendar.from_ical(data.text)
    laitaListaan(tanaanTapahtumat, cal, listaDict, today)
    return tanaanTapahtumat


def tiedotArrayHuomenna(data):
    huomenna = datetime.date.today() + datetime.timedelta(days=1)
    print(huomenna)
    listaDict = lista.listaDict()
    huomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    laitaListaan(huomennaTapahtumat, cal, listaDict, huomenna)
    return huomennaTapahtumat


def tiedotArrayYlihuomenna(data):
    ylihuomenna = datetime.date.today() + datetime.timedelta(days=2)
    print(ylihuomenna)
    listaDict = lista.listaDict()
    ylihuomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    laitaListaan(ylihuomennaTapahtumat, cal, listaDict, ylihuomenna)
    print(ylihuomennaTapahtumat)
    return ylihuomennaTapahtumat


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)