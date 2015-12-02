from datetime import date, timezone
import datetime
import operator

from dateutil import tz
from icalendar import Calendar
import lista
import tilahierarkia
import re

def lisaaTapahtumatListaan(tapahtumat, cal, listaDict, paiva=date.today(), kaikki=False):
    tapahtumapaikka = ""
    for tapahtuma in cal.walk('vevent'):
        alku = tapahtuma.get('dtstart').dt.date()
        if (alku == paiva or kaikki) and alku >= date.today():
            if tapahtuma.get('location') is not None:
                paikka = tapahtuma.get('location')
            if paikka in listaDict:
                huone = parsiSpace(paikka)
                kerros = parsiFloor(paikka)
                rakennus = parsiBuilding(huone)
                alue = parsiArea(rakennus)
                tapahtumat.append({'paikka': paikka,
                                   'paiva': tapahtuma.get('dtstart').dt.date(),
                                   'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                                   'kuvaus': tapahtuma.get('summary'),
                                   'lat': listaDict[paikka]['lat'],
                                   'lon': listaDict[paikka]['lon'],
                                   'areaId' : alue,
                                   'buildingId' : rakennus,
                                   'floorId' : kerros,
                                   'spaceId' : huone})
            else:
                tapahtumat.append({'paikka': tapahtuma.get('location'),
                                   'paiva': tapahtuma.get('dtstart').dt.date(),
                                   'aika': utc_to_local(tapahtuma.get('dtstart').dt).time(),
                                   'kuvaus': tapahtuma.get('summary'),
                                   'lat': '',
                                   'lon': ''})
    tapahtumat.sort(key=operator.itemgetter('paiva', 'aika'))

def parsiArea(rakennus):
    if rakennus is not None:
        alueet = tilahierarkia.alueet()
        return alueet[rakennus]
    return None

def parsiBuilding(paikka):
    if paikka is not None:
        patka = paikka.split(' ')
        lyhenne = patka[0]
        rakennukset = tilahierarkia.rakennukset()
        if lyhenne in rakennukset:
            return rakennukset[lyhenne]
    return None

def parsiFloor(paikka):
    if paikka is not None:
        tila = paikka.split()
        numerot = re.findall(r'\d+[\.]?\d*', paikka)
        try:
            if tila[0] == "Ag":
                return agorakerros(paikka)
            else:
                eka = numerot[0]
                kerros = eka[0]
                kerros = int(kerros)
        except:
            return None
        return kerros
    return None

def parsiSpace(paikka):
    print(paikka)
    erikoistilat = tilahierarkia.erikoistilat()
    if paikka is not None and paikka in erikoistilat:
        return erikoistilat[paikka]
    else:
        return paikka


def agorakerros(paikka):
    tila = paikka.split()
    agora = tilahierarkia.agora()
    try:
        if tila[1] in agora:
            return agora[tila[1]]
        else:
            return parsiFloor(' '.join(tila[1:]))
    except:
        return parsiFloor(' '.join(tila[1:]))

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
    listaDict = lista.listaDict()
    huomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(huomennaTapahtumat, cal, listaDict, huomenna)
    return huomennaTapahtumat


def tiedotArrayYlihuomenna(data):
    ylihuomenna = datetime.date.today() + datetime.timedelta(days=2)
    listaDict = lista.listaDict()
    ylihuomennaTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(ylihuomennaTapahtumat, cal, listaDict, ylihuomenna)
    return ylihuomennaTapahtumat


def utc_to_local(utc_dt):
    to_zone = tz.gettz('Europe/Helsinki')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(to_zone)
