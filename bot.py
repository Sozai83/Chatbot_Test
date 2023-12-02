from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from locations import locations


bot = ChatBot(
    'Weacher',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        # {
        #     'import_path': 'cool_adapter.AskWeather',
        #     'default_response ': 'I am sorry, I do not understand. Please contact XXX for further assistance.',
            
        # },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response ': 'I am sorry, I do not understand. Please contact XXX for further assistance.',
            'maximum_similarity_threshold': 0.95
        },

    ],
    database_uri='sqlite:///database.sqlite3',
    preprocessors=['chatterbot.preprocessors.clean_whitespace',
                   'chatterbot.preprocessors.unescape_html',
                   'chatterbot.preprocessors.convert_to_ascii']
    
)
