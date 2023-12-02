from bot.bot import bot
from flask import *
import re
from classes.Geocode import Geocode
from classes.Weather import Weather
from init.weather_database import LocationDB, db
from init.init_db import init_db
from datetime import *

def search_geocode(location):
    try:
        temp_location = Geocode(location)
        temp_geolocation = temp_location.check_geocode()

        return (temp_location.location, temp_location.latitude, temp_location.longitude)

    except:
        print('Weacher: The location could not be found. Please try again by typing location or type "quit" to start over.')
        temp_input_location = input("You: ")
        if temp_input_location != 'quit':
            return search_geocode(temp_input_location)


asked_weather = False
location = ''
quit_words = ['quit', 'q', 'close']


# Initiate converstaion
def full_converstaion(locations):

    # Get input from the user
    bot_input = input('You: ')

    #################
    # Analyze input #
    ##################

    bot_input_words = re.sub('[.,;!?]','', bot_input.lower()).split()

    # Check if the location in the locations dictionary is in the bot_input
    location = [x for x in bot_input_words if x in locations]

    # Check if the bot_input has weather related words (weather or forecast or temprature)
    weather_query_keywords = ['weather', 'forecast', 'temprature']
    asked_weather = any(x for x in bot_input_words if x in weather_query_keywords)


    #####################################
    # process input and produce output #
    ####################################

    # If location list is not empty
    if len(location) > 0:
        # For each location in the list, check if they want to know 
        for l in location:
            weather_conversation(l)

        # Reset values to check weather query
        asked_weather = False
        location = ''

    # If there is no location mentioned but no location was included 
    elif asked_weather:
        weather_conversation()

        # Reset values to check weather query
        asked_weather = False
        location = ''

    # If the input does not have weather or location related word
    elif bot_input.lower() not in quit_words:
        bot_output = bot.get_response(bot_input)
        print(f'Weacher: {bot_output}')

    else:
        raise Exception('Quitting Converstaion')


# Initiate converstaion related weather
def weather_conversation(temp_location=None):

    if temp_location:
        print(f'Weatcher: You mentioned about {temp_location.capitalize()}. Did you want to know about the weather in that location?')
    else:
        print(f'Weatcher: In which location you want to know the weather of? Please let us konw the location')
        temp_location = input ('You: ')

    try:
        location, latitude, longitude = search_geocode(temp_location)
    except:
        raise Exception('Something went wrong. Please try again.')
    
    print(f'Weatcher: Select number to tell us what you want to know in {location.capitalize()}. \n1: Current Weather, 2: Weather on a specific date, 3: 7 days forecast, 4: Something else')
    weather_type = input ('You: ')

    try:
        temp_weather = Weather(location, latitude, longitude)
        print(f'Weacher: {temp_weather.search_weather(weather_type)}')
        print('Weacher: What else can we help?')

    except:
        raise Exception('Something went wrong. Please try again.')