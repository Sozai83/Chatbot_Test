from weather_database import db, LocationDB, add_weather, add_location, create_db
from locations import locations
from get_weather_location import Weather


def init_db():

    # Create database
    create_db()

    for location in locations:
        try:
            if not (db.session.query(LocationDB).filter(LocationDB.location==location.lower()).first()):
                # Add location in the locations dictionary to DB
                add_location(
                    location = location,
                    latitude = locations[location]['lat'],
                    longitude = locations[location]['lng']
                )

            # Add weather in location to DB
            temp_weather = Weather(location, locations[location]['lat'], locations[location]['lng'])
            temp_weather.check_weather_forecast()

        except:
            continue

    




