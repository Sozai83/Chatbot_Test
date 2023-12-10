from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from bot.bot import bot


weather_mistypes = ['wether','weater', 'wheather', 'weaher', 'weathr']
temperature_mistypes = ['temperture', 'temprature', 'temperaure', 'temerature', 'temperaturee', 'temprature']
forecast_mistypes = ['forcast', 'forecat', 'forescast', 'forecsat', 'forcaset', 'forrecast', 'forecaat']
recommend_mistypes = ['reccomend', 'recomend', 'recommned', 'recommed','recommmend']

convo_weather_mistypes = []
convo_temperature_mistypes = []
convo_forecast_mistypes = []
trainer = ListTrainer(bot)

for weather_mistype in weather_mistypes:
    response = '''
        Did you mean weather?<br>
        Hint: What is the weather in London?
    '''
    question = f'what is the {weather_mistype} in'
    question2 = f'what\'s the {weather_mistype} in'
    question3 = f'{weather_mistype} in'

    convo_weather_mistypes.extend((weather_mistype, response,
                                    question,response,question2,
                                    response,question3,response))


for temperature_mistype in temperature_mistypes:
    response = '''
        Did you mean temperature?<br>
        Hint: What is the temperature in London?
    '''

    question = f'what is the {temperature_mistype} in'
    question2 = f'what\'s the {temperature_mistype} in'
    question3 = f'{temperature_mistype} in'

    convo_temperature_mistypes.extend((temperature_mistype, response,
                                    question,response,question2,
                                    response,question3,response))


for forecast_mistype in forecast_mistypes:
    response = '''
        Did you mean temperature?<br>
        Hint: What is the forecast in London this week?
    '''
    question = f'what is the {forecast_mistype} in'
    question2 = f'what\'s the {forecast_mistype} in'
    question3 = f'{forecast_mistype} in'
    question4 = f'{forecast_mistype}?'

    convo_forecast_mistypes.extend((forecast_mistype, response,
                                    question,response,question2,
                                    response,question3,response,
                                    question4, response))

for recommend_mistype in recommend_mistypes:
    response = '''
        Would you like me to recommend a place for travel in the itinerary?<br>
        I can check weather for each location for today or tomorrow.<br>
        Hint: Where do you recommend to go today?
    '''

    question = f'where do you {recommend_mistype}'
    question2 = f'which location do you {recommend_mistype}'
    question3 = f'what do you {recommend_mistype}'

    convo_forecast_mistypes.extend((recommend_mistype, response,
                                    question,response,question2,
                                    response,question3,response))


def train_mistype():
    trainer.train(convo_weather_mistypes)
    trainer.train(convo_temperature_mistypes)
    trainer.train(convo_forecast_mistypes)
    trainer.train(recommend_mistype)