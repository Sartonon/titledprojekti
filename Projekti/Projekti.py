from flask import Flask
from icalendar import Calendar
from flask import render_template, flash, redirect
import requests
import folium
from forms import LoginForm



app = Flask(__name__)
app.config.from_object('config')



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    r = requests.get('https://korppi.jyu.fi/calendar/ical/QAdtuntDGVQmFXN')
    koodi = r.text
    cal = Calendar.from_ical(koodi)
    for component in cal.walk('vevent'):
        print(component.get('summary'))
        print(component.get('location'))

    map_osm = folium.Map(location=[45.5236, -122.6750],  width="75%", height="95%")
    map_osm.create_map(path='osm.html')
    lol = map_osm.HTML
    hepa = "heihei"
    form = LoginForm()
    long = 25.731064
    lat = 62.234984
    if form.validate_on_submit():
        flash('Login requested for URL="%s"' %
              (form.url.data))
        return redirect('/')
    return render_template('indeksi.html',
                           title='Sign In',
                           form=form,
                           lat=lat,
                           long=long)

@app.route('/kartta')
def kartta():
    map_osm = folium.Map(location=[45.5236, -122.6750],  width="75%", height="95%")
    map_osm._build_map()
    srcdoc = map_osm.HTML
    print(srcdoc)

    return srcdoc

@app.route('/indeksi', methods=['GET', 'POST'])
def indeksi():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for URL="%s"' %
              (form.url.data))
        return redirect('/indeksi')
    return render_template('indeksi.html',
                           title='Sign In',
                           form=form)

if __name__ == '__main__':
    app.run(debug=True)
