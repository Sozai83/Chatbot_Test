from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from locations import locations
from bot import bot


def blablabla():
    print("Weacher: That's correct!")

quit_words = ['quit', 'q', 'close']

while True:
    try:
        bot_input = input('You: ')
        bot_output = bot.get_response(bot_input)

        if str(bot_output) == 'name of a place':
            blablabla()
        elif bot_input.lower() not in quit_words:
            print(f'Weacher: {bot_output}')
        else:
            break
    
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
