from chatterbot.logic import LogicAdapter


class AskWeather(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'what' and 'is' and 'temperature'.
        """
        words = ['what', 'is', 'weather']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        # Ask about location

        response_statement = Statement(text=f'The current temperature is {drink}')

        response_statement.confidence = 1
        return response_statement