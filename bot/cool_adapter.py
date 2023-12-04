from chatterbot.logic import LogicAdapter
from datetime import *
from init.weather_database import WeatherDB
from __main__ import db

# If the input contains the word: forecast or weather, 
class AskWeather(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):

        must_words = ['reccomend']
        any_words = ['which','location', 'where']
        return all(x in statement.text.split() for x in must_words) and any(x in statement.text.split() for x in any_words)

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        today =  all(x in statement.text.split() in 'today')
        tomorrow = all(x in statement.text.split() in 'tomorrow')

        today_date = datetime.utcnow().strftime('%Y-%m-%d')
        tomorrow_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

        if tomorrow:
            temp_reccommended_weather = db.session.query(WeatherDB).filter(
                WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                WeatherDB.date == tomorrow_date,
                WeatherDB.pop != None
            ).all()

            response_statement = temp_reccommended_weather

        else:
            temp_reccommended_weather = db.session.query(WeatherDB).filter(
                WeatherDB.location==self.location.lower(),
                WeatherDB.created_timestamp >= datetime.utcnow() - timedelta(hours=24),
                WeatherDB.date == today_date,
                WeatherDB.pop != None
            ).all()

            response_statement = temp_reccommended_weather




        response_statement.confidence = 1
        return response_statement