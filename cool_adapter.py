from chatterbot.logic import LogicAdapter


class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'what' and 'is' and 'temperature'.
        """
        words = ['what', 'is', 'temperature']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import requests

        # Make a request to the temperature API
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita')
        data = response.json()

        # Let's base the confidence value on if the request was successful
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0

        drink = data['drinks'][0]['strDrink']

        response_statement = Statement(text=f'The current temperature is {drink}')

        response_statement.confidence = confidence
        return response_statement