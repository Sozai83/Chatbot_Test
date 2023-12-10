import requests, os, json
import pandas as pd
import numpy as np
from init.weather_database import add_location, LocationDB
from __main__ import db


# API Key for geocode_url
geocode_api_key = os.environ.get('GoogleMapAPIKey')

# Google map API - Retrieve longitude and latitude based on location
geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='


class Geocode:
    def __init__(self, location):
        self.location = location        

    def check_geocode(self):
        # If the location is in the existing location disctiornary, return latitude and longitude
        try:
            temp_location = db.session.query(LocationDB).filter(LocationDB.location==self.location.lower()).first()
            self.latitude = temp_location.latitude
            self.longitude = temp_location.longitude
            self.location = temp_location.location

            return self.location, self.latitude, self.longitude
        
        # Otherwise, retrieve latitude and longitude using google geocode API
        except:
            resp = requests.get(f'{geocode_url}{self.location.replace(" ", "+")}&key={geocode_api_key}')
            status = resp.json()['status']

            if resp.status_code == 200 and status != 'ZERO_RESULTS':
                result = resp.json()['results'][0]
                self.latitude = result['geometry']['location']['lat']
                self.longitude = result['geometry']['location']['lng']
                self.location = result['address_components'][0]['short_name']
                self.country = result['address_components'][-1]['short_name']

                # Add location data in database
                add_location(self.location.lower(), self.latitude, self.longitude, self.country)

                return self.location, self.latitude, self.longitude

            else:
                raise Exception(f'Filed to retrieve geocode. Please try again. Error:{resp.status_code}')
        