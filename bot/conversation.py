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


#####################################
# Check geocode using Geocode class #
#####################################
def search_geocode(location):
    try:
        temp_location = Geocode(location)
        location, latitude, longitude = temp_location.check_geocode()

        return (location, latitude, longitude)

    except:
        raise Exception()


#####################
# Generate response #
#####################

def response_generator(response, 
                        conversation="",
                        question="",
                        location="",
                        latitude="",
                        longitude="",
                        weather_type="",
                        date="",
                        response_type="", 
                        current_date="", 
                        date_7days="",
                        multilocation=""):


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

    elif response == 'ask_weather_multilocation':
        locations = ''
        for id, loc in enumerate(location):
            if id == 0:
                locations += loc.capitalize()
            else:
                locations += f' and {loc.capitalize()}'

        temp_response = f'''
            You mentioned about {locations}.<br>
            Did you want to know about the weather in those locations?<br>
            Select number to tell us what you want to know in {locations}.<br>
            1: Today's weather<br>
            2: Tomorrow's weather<br>
            3: 7 days forecast<br>
            4: Something else<br>
            '''

        question = "weather_type"
        conversation = True
        temp_response_type = 'string'

    elif response == 'ask_location':
        temp_response = f'''
            In which location you want to know the weather of?<br>
            Please tell us the location.
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
            temp_response = f'''
                Weatcher: Which date do you want to know the weather for?<br>
                Please type the date in YYYY-MM-DD format.<br>
                Please type date between {current_date} and {date_7days}.
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
        "response_type": temp_response_type,
        "multilocation": multilocation
    }

    return temp_response_json

        

###################################################
# This function is used to process converstaion #
##################################################

def full_conversation(temp_input, 
                        conversation="", 
                        question="", 
                        location="", 
                        latitude="", 
                        longitude="", 
                        weather_type="", 
                        date="",
                        multilocation=""):


    if not conversation:
        # Get input from the user
        bot_input = temp_input

        #################
        # Analyze input #
        ##################

        bot_input_words = re.sub('[.,;!?]','', bot_input.lower()).split()

        # Check if the location in the locations dictionary is in the bot_input
        temp_location = [x for x in locations if x in bot_input.lower()]

        # Check if the bot_input has weather related words (weather or forecast or temprature)
        weather_query_keywords = ['weather', 'forecast', 'temperature']
        asked_weather = any(x for x in bot_input_words if x in weather_query_keywords)
    

        #####################################
        # process input and produce output #
        ####################################
    
        # If location list is not empty
        if len(temp_location) > 0:
            temp_location_list = []

            ############################################################
            # Loop through the location to check all of them are valid #
            ############################################################
            for temp in temp_location:
                # Check if the location is valid
                try:
                    location, latitude, longitude = search_geocode(temp)
                    temp_location_list.append(location)

                # If one of the locations failed to retrieve the location, latitude and longitude get back to the user and ask to try again.ss
                except:
                    # Check if they want to know the weather in the location
                    response_json = response_generator(f'We could not find {temp}. Please try again')
                    
                    return response_json
            

            # If there are multiple locations in the input, response back with the "Ask_weather_multilocation" question
            if len(temp_location_list) > 1:
                response_json = response_generator('ask_weather_multilocation', location=temp_location_list, multilocation=True)

            # If there is only one location in the input, ask user the weather type they want to know.
            elif len(temp_location_list) == 1:
                response_json = response_generator('ask_weather', location=location, latitude=latitude, longitude=longitude)
            
            # If the location could not be found, ask the user to start over.
            else:
                response_json = response_generator(f'We could not find {temp}. Please try again')



        ############################################################################################
        # IF the user included weather related keywords but no location in the input, ask location #
        #############################################################################################
        elif asked_weather:
            # Ask location
            response_json = response_generator('ask_location')


        ###############################################################################################################################
        # If this is continuous conversation and no location/weather related keywords, response back with the bot generated reseponse #
        ###############################################################################################################################
        elif bot_input.lower() not in quit_words:
            bot_output = bot.get_response(bot_input)
            response = str(bot_output)

            response_json = response_generator(response)
    
    # Return API reseponse
    return response_json


    ###############################################################################
    # If the converstaion value is not empty = we asked some questions to the user#
    ################################################################################
    elif conversation:

        #####################################################
        # If the location was asked in the last converstaion#
        #####################################################

        if question == "location":
            temp_location = temp_input

            # Check if the location is valid
            try:
                location, latitude, longitude = search_geocode(temp_location)

                # Generates reseponse to ask which weather type the user wants to know for the location
                response_json = response_generator('ask_weather', location=location, latitude=latitude, longitude=longitude)
            
           
            except:
                # If the location geo data could not be retrieved successfully, ask location again
                if temp_location != 'quit':
                    response_json = response_generator(f'We could not find {temp_location}. Please try somewhere else.', 
                                                    question = "location", conversation = True, response_type = 'string')
                
                # If the input is quit, quit converstaion
                else:
                    response_json = response_generator('Please start again. How can I help?')
        

        ##########################################################################
        # If the weather type was asked in the last converstaion (Multi locations#
        ##########################################################################
        elif question == "weather_type" and multilocation and location:
            temp_weather_type = temp_input
            temp_locations =  re.sub(' [.,;!?]','', location.lower()).split(',')

            response = []
            
            # If the temp_weather_type is to check current (1) /forecast (3) weather
            if temp_weather_type == "1" or temp_weather_type == "3":

                # Iterate through weather for each location
                for temp_location in temp_locations:

                    # Check if the location is valid
                    try:
                        location, latitude, longitude = search_geocode(temp_location)
                        temp_weather = Weather(location, latitude, longitude)

                        # Check weather for locations
                        temp_response = temp_weather.search_weather(temp_weather_type)

                        if temp_weather_type == "1":
                           temp_response["location"] = location.capitalize()
                        
                        # Append weather data to response
                        response.append(temp_response)

                    # If there was an issue with retrieving weather, return error message below
                    except:
                        response_json = response_generator('Something went wrong. Please try again')

                    
                response_type = 'multiWeatherToday' if temp_weather_type == "1" else "multiForecast"
                response_json = response_generator(response, response_type=response_type)


            # If the temp_weather_type is to check tomorrow's weather (2)
            elif temp_weather_type == "2":
                temp_tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

                # Iterate through weather for each location
                for temp_location in temp_locations:

                    # Check if the location is valid
                    try:
                        location, latitude, longitude = search_geocode(temp_location)
                        temp_weather = Weather(location, latitude, longitude)

                        # Check weather for locations
                        temp_response = temp_weather.search_weather('2', temp_tomorrow)
                        temp_response['location'] = location.capitalize()

                        # Append weather data to response
                        response.append(temp_response)

                    # If there was an issue with retrieving weather, return error message below
                    except:
                        response_json = response_generator('Something went wrong. Please try again')
                
                response_json = response_generator(response, response_type="multiWeatherTomorrow")
                

            # If something goes wrong, start over
            else:
                response = 'Please start again. How can I help?'
                response_json = response_generator(response)


        
        #########################################################
        # If the weather type was asked in the last converstaion#
        ##########################################################
        
        elif (question == "weather_type" or question == "date") and location and latitude and longitude and not multilocation:

            temp_weather_type = "2" if question == "date" else temp_input
            temp_date = temp_input if question == "date" else date
            temp_weather = Weather(location, latitude, longitude)

            # If the temp_weather_type is to check current (1) /forecast (3) weather
            if temp_weather_type == '1' or temp_weather_type == '3':
                response = temp_weather.search_weather(temp_weather_type)
                response_type = 'weather' if temp_weather_type == '1' else 'forecast'

            # If the temp_weather_type is to check a weather for a specific date (2)
            elif temp_weather_type == '2':

                # If the date is present and it is within the current week check the weather
                if temp_date and temp_date >= temp_weather.datetime_current_date and temp_date <= temp_weather.datetime_7days_after:
                    response = temp_weather.search_weather(temp_weather_type, temp_date)
                    response_type = 'weather specific date'

                # If date is not present or it is out of range we can check, ask the date
                else:
                    response_json = response_generator('ask_date', 
                                                        location=location, 
                                                        latitude=latitude, 
                                                        longitude=longitude, 
                                                        date=date if date else '', 
                                                        current_date=temp_weather.datetime_current_date, 
                                                        date_7days=temp_weather.datetime_7days_after)

            # If something is wrong, start over
            else:
                response = 'Please start again. How can I help?'
                response_json = response_generator(response)
                response_type = 'string'


            #generate response based on the response we have
            response_json = response_generator(response, response_type=response_type)


    # Return API reseponse
    return response_json


    else:
        raise Exception('Quitting Conversation')



