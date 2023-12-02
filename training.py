from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from locations import locations
from bot import bot

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

trainer = ListTrainer(bot)

greeting = [
    'Hello.',
    'Hi. How can I help?'
]

trainer.train(greeting)