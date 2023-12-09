from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from init.locations import locations
from bot.bot import bot

trainer = ListTrainer(bot)

template = '''
Weacher can tell you weathers in locations.<br>
If you want to know the weather in a location, you can ask "What's the weather in XXX?"<br>
If you want Weacher to recommend a location in your itenerary to go today or tomorrow, you can ask "Where do you recommend to go today?".
'''

greeting = [
    'Hello.',
    f'Hi. Howe can I help?<br>{template}'
]

greeting2 = [
    'hello',
    f'Hi there, how can I help?<br>{template}'
]

greeting3 = [
    'Hi',
    f'Hello, how can I help?<br>{template}'
]

def train_greeing():
    trainer.train(greeting)