from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from locations import locations


bot = ChatBot(
    'Weacher',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///database.sqlite3'
    
)

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

trainer = ListTrainer(bot)

for location in locations:
    trainer.train([
        location,
        'name of a place'
    ])

def blablabla():
    print("Weacher: That's correct!")

quit_words = ['quit', 'q', 'close']

while True:
    try:
        bot_input = input('You: ')
        bot_output = bot.get_response(bot_input.lower())

        if str(bot_output).lower() == 'name of a place':
            blablabla()
        elif bot_input.lower() not in quit_words:
            print(f'Weacher: {bot_output}')
        else:
            break
    
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
