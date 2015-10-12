from flask import Flask
from icalendar import Calendar
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    r = requests.get('https://korppi.jyu.fi/calendar/ical/QAdtuntDGVQmFXN')
    koodi = r.text
    cal = Calendar.from_ical(koodi)
    for component in cal.walk('vevent'):
        print (component.get('summary'))
        print (component.get('location'))
    return "Hello World!"

@app.route('/luku')
def luku():
    return "Hello"

if __name__ == '__main__':
    app.run()
