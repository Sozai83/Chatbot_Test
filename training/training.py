from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from init.locations import locations
from bot.bot import bot

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

trainer = ListTrainer(bot)

greeting = [
    'Hello.',
    'Hi. Howe can I help?'
]

trainer.train(greeting)

for location in locations:
    trainer.train([
        location,
        'name of a place',
        f'What is the weather in {location}?',
        'weather',
    ])
