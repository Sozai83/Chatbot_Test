from chatterbot.logic import LogicAdapter
from locations import locations

# If the input contains the word: forecast or weather, 
class AskWeather(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'what' and 'is' and 'temperature'.
        """
        words = ['forecast','weather']
        return any(x in statement.text.split() for x in words)

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        location = []

        for x in input_statement.text.split():
            if x.capitalize() in locations:
                try: 
                    location.append(locations[x.capitalize()]['name'])
                except:
                    raise Exception(f'Filed to retrieve location. Please try again. Error:{resp.status_code}')
        

        if len(location) > 0:
            response_statement = Statement(f'Search weather with location: {location}')
        else:
            response_statement = Statement(f'Search weather')

        response_statement.confidence = 1
        return response_statement