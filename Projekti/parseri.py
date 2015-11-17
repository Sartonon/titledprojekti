from datetime import date, timezone
import datetime
import operator
from icalendar import Calendar
import lista


def lisaaTapahtumatListaan(tapahtumat, cal, listaDict, paiva=date.today(), kaikki=False):
    tapahtumaLyh = ""
    for tapahtuma in cal.walk('vevent'):
        alku = tapahtuma.get('dtstart').dt.date()
        if (alku == paiva or kaikki) and alku >= date.today():
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
                                   'lat': '',
                                   'lon': ''})
    tapahtumat.sort(key=operator.itemgetter('paiva', 'aika'))


def tiedotArray(data):
    today = date.today()
    listaDict = lista.listaDict()
    kaikkiTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(kaikkiTapahtumat, cal, listaDict, today, True)
    return kaikkiTapahtumat


def tiedotArrayTanaan(data):
    today = date.today()
    listaDict = lista.listaDict()
    tanaanTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(tanaanTapahtumat, cal, listaDict, today)
    return tanaanTapahtumat


def tiedotArrayHuomenna(data):
    huomenna = datetime.date.today() + datetime.timedelta(days=1)
    print(huomenna)
    listaDict = lista.listaDict()
    huomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(huomennaTapahtumat, cal, listaDict, huomenna)
    return huomennaTapahtumat


def tiedotArrayYlihuomenna(data):
    ylihuomenna = datetime.date.today() + datetime.timedelta(days=2)
    print(ylihuomenna)
    listaDict = lista.listaDict()
    ylihuomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(ylihuomennaTapahtumat, cal, listaDict, ylihuomenna)
    print(ylihuomennaTapahtumat)
    return ylihuomennaTapahtumat


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    # TODO: aikavy�hykkeen kovakoodaaminen (ei voi tiet�� miss� p�in maailmaa serveri tulee sijaitsemaan)
