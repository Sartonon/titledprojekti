#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016  Jose Malmberg, Toni Pitkänen, Santeri Rusila, Markus Valkama
#
#
# Karttakotka is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Karttakotka is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Karttakotka.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, jsonify
from flask import render_template, flash, redirect
import folium
from forms import LoginForm
from flask import request
import requests
import lista
from parseri import tiedotArray, tiedotArrayTanaan, tiedotArrayHuomenna, tiedotArrayYlihuomenna, tiedotArrayValittu
import os
import json

app = Flask(__name__)
app.config.from_object('config')


@app.route('/calday')
def hae_valittu_paiva():
    selected_date = request.args.get('selected_date')
    valittupaiva = []
    form = LoginForm()
    try:
        data = urldata
        try:
            valittupaiva = tiedotArrayValittu(selected_date, data)
        except:
            print("virhe valitussa paivassa")
    except:
        print("virhe valitussa paivas")
    return json.dumps(valittupaiva)


@app.route('/uusi', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def perus():
    lat = 62.23252728347514
    lon = 25.73729200674369
    form = LoginForm()
    tapahtumat = []
    tapahtumatTanaan = []
    tapahtumatHuomenna = []
    tapahtumatYlihuomenna = []
    global urldata
    tiedosto = '../kayttoohjeet.txt'
    try:
        if form.url.data is not None:
            data = requests.get(form.url.data)
            urldata = data
            try:
                tapahtumatTanaan = tiedotArrayTanaan(data)
            except:
                print("virhe tanaan")
            try:
                tapahtumatHuomenna = tiedotArrayHuomenna(data)
            except:
                print("virhe huomenna")
            try:
                tapahtumatYlihuomenna = tiedotArrayYlihuomenna(data)
            except:
                print("virhe ylihuomenna")
            try:
                tapahtumat = tiedotArray(data)
            except:
                print("virhe kaikkien listaamisessa")
                flash("URL:ssa virhe, kokeile uudelleen.")
    except:
        print("virhe")
        flash("Anna toimiva url osoite.")
    try:
        with open(tiedosto, encoding='UTF-8') as t:
            kayttoohjeet = t.readlines()
    except:
        print("Virhe tiedoston lukemisessa.")
        kayttoohjeet = ["Pahoittelemme. Kayttoohjeiden lukemisessa tapahtui virhe."]
    return render_template('collapsevalikko.html',
                           title='Sign In',
                           form=form,
                           tapahtumat=tapahtumat,
                           tapahtumatTanaan=tapahtumatTanaan,
                           tapahtumatHuomenna=tapahtumatHuomenna,
                           tapahtumatYlihuomenna=tapahtumatYlihuomenna,
                           kayttoohjeet=kayttoohjeet,
                           lat=lat,
                           lon=lon)


@app.route('/kartta', methods=['GET', 'POST'])
def kartta():
    if request.args.get('marker'):
        showMarker = True
    else:
        showMarker = False

    if request.args.get('lat') and request.args.get('lon'):
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    else:
        listaDict = lista.listaDict()
        lat = (listaDict['ag']['lat'])
        lon = (listaDict['ag']['lon'])
        showMarker = False

    if showMarker:
        map_osm = folium.Map(location=[lat, lon], width="100%", height="100%", zoom_start=17, max_zoom=18)
        map_osm.simple_marker([lat, lon])
    else:
        map_osm = folium.Map(location=[lat, lon], width="100%", height="100%", zoom_start=15, max_zoom=18)

    if request.args.get('ulat') and request.args.get('ulon'):
        ulat = float(request.args.get("ulat"))
        ulon = float(request.args.get("ulon"))
        map_osm.polygon_marker(location=[ulat, ulon], popup='Sinun sijaintisi(Suuntaa antava)',
                               fill_color='red', num_sides=0, radius=10, rotation=60)
    map_osm.create_map(path='templates/osm.html')

    return render_template('osm.html')


@app.route('/virhe', methods=['GET', 'POST'])
def virhe():
    return render_template('virhe.html')


if __name__ == '__main__':
    server_port = os.environ.get("PORT")

    if server_port is None:
        server_port = 5000
        debugging = True
        host = "localhost"
    else:
        server_port = int(server_port)
        host = "0.0.0.0"
        debugging = True

    app.run(port=server_port, debug=debugging, host=host)
