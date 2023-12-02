from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from bot import bot
from flask import *
import re
from get_weather_location import Geocode,Weather
from weather_database import LocationDB, db
from init_db import init_db
from datetime import *


app = Flask(__name__)


def blablabla():
    print("Weacher: That's correct!")

quit_words = ['quit', 'q', 'close']


asked_weather = False
location = ''
weather_type = ''
init_db()


print('Hello. My name is Weacher. How can I help?')


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
        else:
            return

while True:
    try:
        # Get locations list from the LocationDB
        locations = [x.location for x in db.session.query(LocationDB).all()]


        bot_input = input('You: ')

        bot_input_words = re.sub('[.,;!?]','', bot_input.lower()).split()

        # Check if the location in the locations dictionary is in the bot_input
        location = [x for x in bot_input_words if x in locations]

        # Check if the bot_input has weather related words (weather or forecast or temprature)
        weather_query_keywords = ['weather', 'forecast', 'temprature']
        asked_weather = any(x for x in bot_input_words if x in weather_query_keywords)

        print('It is my turn', location, asked_weather, weather_type)

        # If location list is not empty
        if len(location) > 0:
            # For each location in the list, check if they want to know 
            for l in location:
                try:
                    location, latitude, longitude = search_geocode(l)
                except:
                    raise Exception('Finish converstaion')

                # Ask what sort of weather the user want to know
                print(f'Weatcher: You mentioned {location.capitalize()}. Do you want to know about weather in {location}?')
                print(f'Weatcher: Select number to tell us what you want to know in {location.capitalize()}. 1: Current Weather, 2: Weather on a specific date, 3: 7 days forecast, 4: No I do not need to')
                weather_type = input ('You: ')
                try:
                    temp_weather = Weather(location, latitude, longitude)
                    print(temp_weather.search_weather(weather_type))
                except:
                    print('Something went wrong. Please try again.')


        # If there is no location mentioned but no location was included 
        elif asked_weather:
            print(f'Weatcher: In which location you want to know the weather of? Please let us konw the location')
            location = input ('You: ')

            # Check location data
            try:
                location, latitude, longitude= search_geocode(location)
            except:
                raise Exception('Finish converstaion')


            print(f'Weatcher: Selected Location: {location}. 1: Current Weather, 2: Weather on a specific date, 3: 7 days forecast, 4: Change location')
            weather_type = input ('You: ')
            try:
                temp_weather = Weather(location, latitude, longitude)
                print(temp_weather.search_weather(weather_type))
            except:
                print('Something went wrong. Please try again.')


        # If the input does not have weather or location related word
        elif bot_input.lower() not in quit_words:
            bot_output = bot.get_response(bot_input)
            print(f'Weacher: {bot_output}')
        else:
            break


    except(KeyboardInterrupt, EOFError, SystemExit):
        break





if __name__ == '__main__':
    app.run()