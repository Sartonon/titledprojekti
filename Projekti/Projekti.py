from flask import Flask
from icalendar import Calendar
from flask import render_template, flash, redirect
import folium
from forms import LoginForm
from flask import request
import requests
import lista
from Parseri import tiedotArray

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def perus():
    listaDict = lista.listaDict()
    lat = (listaDict['Ag']['C232']['lat'])
    lon = (listaDict['Ag']['C232']['lon'])
    form = LoginForm()
    tapahtumat = []
    try:
        if form.url.data is not None:
            data = requests.get(form.url.data)
            tapahtumat = tiedotArray(data)

    except:
        print("virhe")
        flash("URL:ssa virhe, kokeile uudelleen.")
    return render_template('base.html',
                           title='Sign In',
                           form=form,
                           tapahtumat=tapahtumat,
                           lat=lat,
                           lon=lon)

#Turha?
@app.route('/kartta', methods=['GET', 'POST'])
def kartta():
    if request.args.get('lat') and request.args.get('lon'):
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    else:
        listaDict = lista.listaDict()
        lat = (listaDict['Ag']['lat'])
        lon = (listaDict['Ag']['lon'])
    map_osm = folium.Map(location=[lat, lon],  width="100%", height="100%", zoom_start=17, max_zoom=18)
    map_osm.simple_marker([lat, lon])
    map_osm.create_map(path='templates/osm.html')

    return render_template('osm.html')

if __name__ == '__main__':
    app.run(debug=True)
