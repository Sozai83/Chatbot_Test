from chatterbot.logic import LogicAdapter
from datetime import *
from init.weather_database import WeatherDB
from __main__ import db
import re

# If the input contains special keyword i.e. recommend this adapter is used.
class AskWeather(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):

        must_words = ['recommend']
        any_words = ['which','location', 'where']
        input_list = re.sub('[.,;!?]','', str(statement).lower()).split()

        # If the input contains 'recommend' and have at least one of 'which', 'location', 'where', return True for can_process
        if all(x in input_list for x in must_words) and any(x in input_list for x in any_words):
            process = True
        else:
            process = False

        return process


    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        # Create a list of words in the input
        input_list = re.sub('[.,;!?]','', str(input_statement).lower()).split()

        # If tomorrow is included in the input_list, date = tomorrow. Otherwise, it's today
        date =  'tommorrow' if any(x in input_list for x in ['tomorrow']) else 'today'

        today_date = datetime.utcnow().strftime('%Y-%m-%d')
        tomorrow_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

        # If the user is asking recommendation for tomorrow
        if date == 'tomorrow':
            # Get location that is Clear weather tomorrow
            clear_weathers = db.session.query(WeatherDB).filter(
                WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                WeatherDB.desc == 'Clear',
                WeatherDB.date == tomorrow_date,
                WeatherDB.itinerary == True,
                WeatherDB.pop != None
            ).all()

            if len(clear_weathers) > 0:
                recommend_locations = clear_weathers
                weather_reason = 'it is sunny'
            
            else:
                # If there is no location that has Clear weather, search for cloudy weather
                cloud_weathers = db.session.query(WeatherDB).filter(
                    WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                    WeatherDB.desc == 'Clouds',
                    WeatherDB.date == tomorrow_date,
                    WeatherDB.itinerary == True,
                    WeatherDB.pop != None
                ).all()
                
                if len(cloud_weathers) > 0:
                    recommend_locations = cloud_weathers
                    weather_reason = 'there is no sunny locations but these locations are not rainy'
                
                else:
                    recommend_locations = False


        else:
            # Get location that is Clear weather today
            clear_weathers = db.session.query(WeatherDB).filter(
                WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                WeatherDB.desc == 'Clear',
                WeatherDB.date == today_date,
                WeatherDB.itinerary == True,
                WeatherDB.pop != None
            ).all()

            if len(clear_weathers) > 0:
                recommend_locations = clear_weathers
                weather_reason = 'it is sunny'
            else:
                # If there is no location that has Clear weather, search for cloudy weather
                cloud_weathers = db.session.query(WeatherDB).filter(
                    WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                    WeatherDB.desc == 'Clouds',
                    WeatherDB.date == today_date,
                    WeatherDB.itinerary == True,
                    WeatherDB.pop != None
                ).all()

                if len(cloud_weathers) > 0:
                    recommend_locations = cloud_weathers
                    weather_reason = 'there is no sunny locations but these locations are not rainy'
                
                else:
                    recommend_locations = False
        
        locations = ''

        # If there are locations we can recommend, response with the location and the reason for recommendation
        if recommend_locations:
            for id, reccomend in enumerate(recommend_locations):
                if id > 0:
                    locations += ' or ' + reccomend.location.capitalize()
                else:
                    locations += reccomend.location.capitalize()
            
            response_statement_string = (f'I reccomend going to {locations} {date} because {weather_reason}.')
        
        # If there is no location we can recommend, response that all locations in the itenreray are rainy
        else:
            response_statement_string = (f'I cannot recommend anywhere. All places in the itinerary are rainy {date}.')
        

        response_statement = Statement(response_statement_string)

        response_statement.confidence = 1

        return response_statement