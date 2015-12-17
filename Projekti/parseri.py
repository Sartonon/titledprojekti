#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timezone
import datetime
import operator
from dateutil import tz
from icalendar import Calendar
import lista
import tilahierarkia
import re
from bottle import unicode

#hahaha
def lisaaTapahtumatListaan(tapahtumat, cal, listaDict, paiva=date.today(), kaikki=False):
    nykyhetki = utc_to_local(datetime.datetime.today())
    for tapahtuma in cal.walk('vevent'):
        alku = tapahtuma.get('dtstart')
        alkupaiva = alku.dt.date()
        loppuaika = tapahtuma.get('dtend').dt
        if (alkupaiva == paiva or kaikki) and loppuaika >= nykyhetki:
            if tapahtuma.get('location') is not None:
                paikat1 = tapahtuma.get('location').split(', ')
                paikat2 = tapahtuma.get('location').lower().split(', ')
            else:
                paikat1 = ""
                paikat2 = ""
            paikat = []
            for p in range(0, paikat2.__len__()):
                if paikat2[p] in listaDict:
                    huone = parsiSpace(paikat1[p])
                    kerros = parsiFloor(huone)
                    rakennus = parsiBuilding(huone)
                    alue = parsiArea(rakennus)
                    paikat.append({'paikka': paikat1[p],
                                   'lat': listaDict[paikat2[p]]['lat'],
                                   'lon': listaDict[paikat2[p]]['lon'],
                                   'areaId': alue,
                                   'buildingId': rakennus,
                                   'floorId': kerros,
                                   'spaceId': huone})
                else:
                    paikat.append({'paikka': paikat1[p],
                                   'lat': '',
                                   'lon': ''})

            tapahtumat.append({'paikat': paikat,
                               'paivalajittelu' : unicode(alkupaiva),
                               'paiva': unicode(alkupaiva.strftime('%d.%m.%Y')),
                               'aika': unicode(utc_to_local(alku.dt).strftime('%H:%M')),
                               'kuvaus': tapahtuma.get('summary')})
    tapahtumat.sort(key=operator.itemgetter('paivalajittelu', 'aika'))


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


def tiedotArrayValittu(paiva, data):
    yy = paiva.split('-')[0]
    mm = paiva.split('-')[1]
    dd = paiva.split('-')[2]
    d1 = datetime.date(int(yy), int(mm), int(dd))
    listaDict = lista.listaDict()
    valitutTapahtumat = []
    cal = Calendar.from_ical(data.text)
    lisaaTapahtumatListaan(valitutTapahtumat, cal, listaDict, d1)
    return valitutTapahtumat


def utc_to_local(utc_dt):
    to_zone = tz.gettz('Europe/Helsinki')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(to_zone)
