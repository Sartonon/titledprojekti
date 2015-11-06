import operator
from flask import Flask
from flask import render_template, flash, redirect
import folium
from forms import LoginForm
from flask import request
import requests
import lista
from parseri import tiedotArray, tiedotArrayTanaan, tiedotArrayHuomenna, tiedotArrayYlihuomenna
import os

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def perus():
    #kokeilu 
    lat = 67
    lon = 67
    form = LoginForm()
    tapahtumat = []
    tapahtumatTanaan = []
    tapahtumatHuomenna = []
    tapahtumatYlihuomenna = []
    tiedosto = '../kayttoohjeet.txt'
    try:
        if form.url.data is not None:
            data = requests.get(form.url.data)
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
    except:
        print("virhe")
        flash("URL:ssa virhe, kokeile uudelleen.")
    try:
        with open(tiedosto, encoding='UTF-8') as t:
            kayttoohjeet = t.readlines()
    except:
        print("Virhe tiedoston lukemisessa.")
        kayttoohjeet = ["Pahoittelemme. Kayttoohjeiden lukemisessa tapahtui virhe."]
    return render_template('base.html',
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
    if request.args.get('lat') and request.args.get('lon'):
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    else:
        listaDict = lista.listaDict()
        lat = (listaDict['Ag']['lat'])
        lon = (listaDict['Ag']['lon'])
    map_osm = folium.Map(location=[lat, lon], width="100%", height="100%", zoom_start=17, max_zoom=18)
    map_osm.simple_marker([lat, lon])
    map_osm.create_map(path='templates/osm.html')

    return render_template('osm.html')


if __name__ == '__main__':
    app.run(debug=True)
