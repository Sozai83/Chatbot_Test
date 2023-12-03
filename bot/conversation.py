from bot.bot import bot
from flask import *
import re
from classes.Geocode import Geocode
from classes.Weather import Weather
from init.weather_database import LocationDB
from datetime import *
from __main__ import db

def search_geocode(location):
    try:
        temp_location = Geocode(location)
        location, latitude, longitude = temp_location.check_geocode()

        return (location, latitude, longitude)

    except:
        raise Exception()

        
asked_weather = False
location = ''
quit_words = ['quit', 'q', 'close']
# Get locations list from the LocationDB
locations = [x.location for x in db.session.query(LocationDB).all()]




# Initiate conversation
def full_conversation(input, 
                        conversation="", 
                        question="", 
                        location="", 
                        latitude="", 
                        longitude="", 
                        weather_type="", 
                        date=""):


    if not conversation:
        # Get input from the user
        bot_input = input

        #################
        # Analyze input #
        ##################

        bot_input_words = re.sub('[.,;!?]','', bot_input.lower()).split()

        # Check if the location in the locations dictionary is in the bot_input
        temp_location = [x for x in bot_input_words if x in locations]

        # Check if the bot_input has weather related words (weather or forecast or temprature)
        weather_query_keywords = ['weather', 'forecast', 'temprature']
        asked_weather = any(x for x in bot_input_words if x in weather_query_keywords)
    

        #####################################
        # process input and produce output #
        ####################################

        # If location list is not empty
        if len(temp_location) > 0:

            # Check if the location is valid
            try:
                location, latitude, longitude = search_geocode(temp_location[0])
            except:
                raise Exception(f'Geocode could not be retrieved for {temp_location[0]}. Please try again.')

            # Check if they want to know the weather in the location
            response = f'''
                You mentioned about {location.capitalize()}. Did you want to know about the weather in that location?
                Select number to tell us what you want to know in {location.capitalize()}.
                1: Current Weather
                2: Weather on a specific date
                3: 7 days forecast
                4: Something elsey
                '''

            response_json = {
                "response": response,
                "conversation": True,
                "question": "weather_type",
                "location" : location,
                "latitude" : latitude,
                "longitude": longitude,
                "weather_type": "",
                "date": "",
                "response_type": "string"
            }

            return response_json
            # weather_conversation(temp_location=location[0])


        # If there is no location mentioned but no location was included 
        elif asked_weather:
            # Ask location
            response = f'''
                In which location you want to know the weather of? Please let us konw the location.
                '''

            response_json = {
                "response": response,
                "conversation": True,
                "question": "location",
                "location" : "",
                "latitude" : "",
                "longitude": "",
                "weather_type": "",
                "date": "",
                "response_type": "string"
            }

            return response_json

            # weather_conversation()


        # If the input does not have weather or location related word
        elif bot_input.lower() not in quit_words:
            bot_output = bot.get_response(bot_input)
            response = str(bot_output)

            response_json = {
                "response": response,
                "conversation": "",
                "question": "",
                "location" : "",
                "latitude" : "",
                "longitude": "",
                "weather_type": "",
                "date": "",
                "response_type": "string"
            }


            return response_json


    elif conversation:
        if question == "location":
            # Check if the location is valid
            temp_location = input

            try:
                location, latitude, longitude = search_geocode(temp_location)
            except:
                raise Exception(f'Geocode could not be retrieved for {temp_location}. Please try again.')
            
            if location and latitude and longitude:
                # Check if they want to know the weather in the location
                response = f'''
                    You mentioned about {location.capitalize()}. Did you want to know about the weather in that location?
                    Select number to tell us what you want to know in {location.capitalize()}.
                    1: Current Weather
                    2: Weather on a specific date
                    3: 7 days forecast
                    4: Something else
                    '''

                response_json = {
                    "response": response,
                    "conversation": True,
                    "question": "weather_type",
                    "location" : location,
                    "latitude" : latitude,
                    "longitude": longitude,
                    "weather_type": "",
                    "date": "",
                    "response_type": "string"
                }

                return response_json
            # weather_conversation(temp_location=location[0])
            # temp_weather = Weather(location, latitude, longitude)
        
        elif (question == "weather_type" or question == "date") and location and latitude and longitude:
            temp_weather_type = "2" if question == "date" else input
            temp_date = input if question == "date" else date
            temp_weather = Weather(location, latitude, longitude)

            if temp_weather_type == '1' or temp_weather_type == '3':
                response = temp_weather.search_weather(temp_weather_type)
                reseponse_type = 'weather' if temp_weather_type == '1' else 'forecast'

            elif temp_weather_type == '2':
                if temp_date and temp_date >= temp_weather.datetime_current_date and temp_date <= temp_weather.datetime_7days_after:
                    response = temp_weather.search_weather(temp_weather_type, temp_date)
                    reseponse_type = 'weather specific date'

                else:
                    if temp_date:
                        response = (f'Please type date between {temp_weather.datetime_current_date} and {temp_weather.datetime_7days_after}.')
                    else:
                        response = '''
                            Weatcher: Which date do you want to know the weather for?
                            Please type the date in YYYY-MM-DD format.
                        '''
                    response_json = {
                        "response": response,
                        "conversation": True,
                        "question": "date",
                        "location" : location,
                        "latitude" : latitude,
                        "longitude": longitude,
                        "weather_type": "2",
                        "date": "",
                        "response_type": "string"
                    }

                    return response_json
            
            else:
                response = 'Please start again. How can I help?'
                reseponse_type = 'string'

            response_json = {
                        "response": response,
                        "conversation": "",
                        "question": "",
                        "location" : "",
                        "latitude" : "",
                        "longitude": "",
                        "weather_type": "",
                        "date": "",
                        "response_type": reseponse_type
                    }

            return response_json


    else:
        raise Exception('Quitting Conversation')

