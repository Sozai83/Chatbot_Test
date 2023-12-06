from bot.bot import bot
from flask import *
import re
from classes.Geocode import Geocode
from classes.Weather import Weather
from init.weather_database import LocationDB
from datetime import *
from __main__ import db


asked_weather = False
location = ''
quit_words = ['quit', 'q', 'close']
# Get locations list from the LocationDB
locations = [x.location for x in db.session.query(LocationDB).all()]

def search_geocode(location):
    try:
        temp_location = Geocode(location)
        location, latitude, longitude = temp_location.check_geocode()

        return (location, latitude, longitude)

    except:
        raise Exception()



def response_generator(response, conversation="",question="",location="",latitude="",longitude="",weather_type="",date="",response_type="", current_date="", date_7days=""):
    temp_response = ''

    if response == 'ask_weather':
        temp_response = f'''
            You mentioned about {location.capitalize()}. Did you want to know about the weather in that location?<br>
            Select number to tell us what you want to know in {location.capitalize()}.<br>
            1: Current Weather<br>
            2: Weather on a specific date<br>
            3: 7 days forecast<br>
            4: Something else<br>
            '''
        question = "weather_type"
        conversation = True
        temp_response_type = 'string'

    elif response == 'ask_location':
        temp_response = f'''
            In which location you want to know the weather of?<br>
            Please let us konw the location.
            '''

        question = "location"
        conversation = True
        temp_response_type = 'string'

    elif response == 'ask_date':
        question = 'date'
        conversation = True
        weather_type = '2'
        temp_response_type = 'string'

        if date:
            temp_response = f'Please type date between {current_date} and {date_7days}.'
        else:
            temp_response = '''
                Weatcher: Which date do you want to know the weather for?<br>
                Please type the date in YYYY-MM-DD format.
            '''

    else:
        temp_response = response
        temp_response_type = response_type if response_type else 'string'

    

    temp_response_json = {
        "response": temp_response,
        "conversation": conversation,
        "question": question,
        "location" : location,
        "latitude" : latitude,
        "longitude": longitude,
        "weather_type": weather_type,
        "date": date,
        "response_type": temp_response_type
    }

    return temp_response_json

        



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
        weather_query_keywords = ['weather', 'forecast', 'temperature']
        asked_weather = any(x for x in bot_input_words if x in weather_query_keywords)
    

        #####################################
        # process input and produce output #
        ####################################

        # If location list is not empty
        if len(temp_location) > 0:

            # Check if the location is valid
            try:
                location, latitude, longitude = search_geocode(temp_location[0])
                # Check if they want to know the weather in the location
                response_json = response_generator('ask_weather', location=location, latitude=latitude, longitude=longitude)

            except:
                # Check if they want to know the weather in the location
                response_json = response_generator(f'We could not find {temp_location}. Please try somewhere else', 
                                                    question = "location", conversation = True, response_type = 'string')

            
            return response_json
            # weather_conversation(temp_location=location[0])


        # If there is no location mentioned but no location was included 
        elif asked_weather:
            # Ask location
            response_json = response_generator('ask_location')

            return response_json


        # If the input does not have weather or location related word
        elif bot_input.lower() not in quit_words:
            bot_output = bot.get_response(bot_input)
            response = str(bot_output)

            response_json = response_generator(response)

            return response_json


    elif conversation:
        if question == "location":
            # Check if the location is valid
            temp_location = input

            try:
                location, latitude, longitude = search_geocode(temp_location)
                # Check if they want to know the weather in the location
                response_json = response_generator('ask_weather', location=location, latitude=latitude, longitude=longitude)
            except:
                if temp_location != 'quit':
                    response_json = response_generator(f'We could not find {temp_location}. Please try somewhere else.', 
                                                    question = "location", conversation = True, response_type = 'string')
                
                else:
                    response_json = response_generator('Please start again. How can I help?')

            return response_json

        
        elif (question == "weather_type" or question == "date") and location and latitude and longitude:
            temp_weather_type = "2" if question == "date" else input
            temp_date = input if question == "date" else date
            temp_weather = Weather(location, latitude, longitude)

            if temp_weather_type == '1' or temp_weather_type == '3':
                response = temp_weather.search_weather(temp_weather_type)
                response_type = 'weather' if temp_weather_type == '1' else 'forecast'

            elif temp_weather_type == '2':
                if temp_date and temp_date >= temp_weather.datetime_current_date and temp_date <= temp_weather.datetime_7days_after:
                    response = temp_weather.search_weather(temp_weather_type, temp_date)
                    response_type = 'weather specific date'

                else:
                    response_json = response_generator('ask_date', 
                                                        location=location, 
                                                        latitude=latitude, 
                                                        longitude=longitude, 
                                                        date=date if date else '', 
                                                        current_date=temp_weather.datetime_current_date, 
                                                        date_7days=temp_weather.datetime_7days_after)

                    return response_json
            
            else:
                response = 'Please start again. How can I help?'
                response_json = response_generator(response)

                return response_json


            response_json = response_generator(response, response_type=response_type)

            return response_json


    else:
        raise Exception('Quitting Conversation')



