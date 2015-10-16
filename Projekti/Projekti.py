from flask import Flask
from icalendar import Calendar
from flask import render_template, flash, redirect
import folium
from forms import LoginForm
from flask import request
import requests
import lista
import parseri

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def perus():
    listaDict = lista.listaDict()
    lat = (listaDict['Ag']['lat'])
    lon = (listaDict['Ag']['lon'])
    form = LoginForm()
    tapahtumat = []
    try:
        if form.url.data is not None:
            data = requests.get(form.url.data)
            tapahtumat = parseri.tiedotArray(data)
            koodi = data.text
            cal = Calendar.from_ical(koodi)
            for component in cal.walk('vevent'):
                print(component.get('summary'))
                print(component.get('location'))
    except:
        print ("virhe")

    ''' #Mita tama tekee?
    if form.validate_on_submit():
        flash('Login requested for URL="%s"' %
              form.url.data)
        return redirect('/')'''

    return render_template('indeksi.html',
                           title='Sign In',
                           form=form,
                           tapahtumat=tapahtumat,
                           lat=lat,
                           lon=lon)


@app.route('/kartta', methods=['GET', 'POST'])
def kartta():
    if request.args.get('lat') and request.args.get('lon'):
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lat"))
    else:
        listaDict = lista.listaDict()
        lat = (listaDict['Ag']['lat'])
        lon = (listaDict['Ag']['lon'])
    map_osm = folium.Map(location=[lat, lon],  width="100%", height="100%", zoom_start=17, max_zoom=18)
    map_osm.simple_marker([lat, lon])
    map_osm.create_map(path='templates/osm.html')

    return render_template('osm.html')


@app.route('/indeksi', methods=['GET', 'POST'])
def indeksi():
    form = LoginForm()
    lat = 62.234984
    lon = 25.731064
    if form.validate_on_submit():
        flash('Login requested for URL="%s"' %
              form.url.data)
        return redirect('/indeksi')
    return render_template('indeksi.html',
                           title='Sign In',
                           form=form,
                           lat=lat,
                           lon=lon)

if __name__ == '__main__':
    app.run(debug=True)
