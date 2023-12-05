from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from bot.bot import bot


weather_mistypes = ['wether','weater', 'wheather', 'weaher', 'weathr']
temperature_mistypes = ['temperture', 'temprature', 'temperaure', 'temerature', 'temperaturee', 'temprature']
forecast_mistypes = ['forcast', 'forecat', 'forescast', 'forecsat', 'forcaset', 'forrecast', 'forecaat']

convo_weather_mistypes = []
convo_temperature_mistypes = []
convo_forecast_mistypes = []
trainer = ListTrainer(bot)

for weather_mistype in weather_mistypes:
    response = '''
        Did you mean weather?<br>
        Hint: What is the weather in London?
    '''

    convo_weather_mistypes.extend((weather_mistype, response))


for temperature_mistype in temperature_mistypes:
    response = '''
        Did you mean temperature?<br>
        Hint: What is the temperature in London?
    '''

    convo_weather_mistypes.extend((temperature_mistype, response))


for forecast_mistype in forecast_mistypes:
    response = '''
        Did you mean temperature?<br>
        Hint: What is the forecast in London this week?
    '''

    convo_weather_mistypes.extend((forecast_mistype, response))

def train_mistype_temp():
    trainer.train(convo_weather_mistypes)
    trainer.train(convo_temperature_mistypes)
    trainer.train(convo_forecast_mistypes)


def train_mistype():
    return train_mistype_temp()