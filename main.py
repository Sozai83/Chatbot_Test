from flask import *
from init.init_db import init_db
from init.weather_database import LocationDB, db
from bot.conversation import full_converstaion


app = Flask(__name__)

init_db()
# Get locations list from the LocationDB
locations = [x.location for x in db.session.query(LocationDB).all()]


print('Hello. My name is Weacher. How can I help?')

while True:
    try:
        full_converstaion(locations)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break


if __name__ == '__main__':
    app.run()