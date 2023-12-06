from chatterbot.logic import LogicAdapter
from datetime import *
from init.weather_database import WeatherDB
from __main__ import db
import re

# If the input contains the word: forecast or weather, 
class AskWeather(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):

        must_words = ['recommend']
        any_words = ['which','location', 'where']

        if all(x in statement.text.lower().split() for x in must_words) and any(x in statement.text.lower().split() for x in any_words):
            process = True
        else:
            process = False

        return process


    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        input_list = re.sub('[.,;!?]','', str(input_statement).lower()).split()

        date =  'tommorrow' if any(x in input_list for x in ['tomorrow']) else 'today'

        today_date = datetime.utcnow().strftime('%Y-%m-%d')
        tomorrow_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

        if date == 'tomorrow':
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

        if recommend_locations:
            for id, reccomend in enumerate(recommend_locations):
                if id > 0:
                    locations += ' or ' + reccomend.location.capitalize()
                else:
                    locations += reccomend.location.capitalize()
            
            response_statement_string = (f'I reccomend going to {locations} {date} because {weather_reason}.')
        
        else:
            response_statement_string = (f'I cannot recommend anywhere. All places in the itinerary are rainy {date}.')
        

        response_statement = Statement(response_statement_string)

        response_statement.confidence = 1

        return response_statement