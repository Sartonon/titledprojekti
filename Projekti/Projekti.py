from flask import Flask
from icalendar import Calendar
from flask import render_template, flash, redirect
import folium
from forms import LoginForm
from flask import request
import requests



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


@app.route('/kartta', methods=['GET', 'POST'])
def kartta():
    lat = 62.234984
    lon = 25.731064
    if request.args.get('lat'):
        lat = float(request.args.get("lat"))
    if request.args.get('lon'):
        lon = float(request.args.get("lon"))
    map_osm = folium.Map(location=[lat, lon],  width="75%", height="95%")
    print(map_osm)
    map = map_osm.create_map(path='templates/osm.html')
    srcdoc = map_osm.HTML
    return render_template('osm.html')

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
