from flask import Flask
from icalendar import Calendar
from flask import render_template, flash, redirect
import requests
import folium

app = Flask(__name__)
app.config.from_object('config')



@app.route('/')
def hello_world():
    r = requests.get('https://korppi.jyu.fi/calendar/ical/QAdtuntDGVQmFXN')
    koodi = r.text
    cal = Calendar.from_ical(koodi)
    for component in cal.walk('vevent'):
        print(component.get('summary'))
        print(component.get('location'))

    return "Hello Worldg!"

@app.route('/kartta')
def kartta():
    map_osm = folium.Map(location=[45.5236, -122.6750],  width="75%", height="95%")
    map_osm.create_map(path='templates/osm.html')
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
