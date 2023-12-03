from flask import *
from init.init_db import init_db
from bot.conversation import full_conversation


app = Flask(__name__)

init_db()

conversation = False
question = ""
location = ""
latitude = ""
longitude = ""
weather_type = ""
date = ""

# @app.route('/askWeacher',  methods=['POST'])
# def ask_weacher():
#     try:
#         input = request.form['ask_weacher']
#         continuous_conversation, asked_weather, location, response = full_conversation(input)

#         return response

#     except(KeyboardInterrupt, EOFError, SystemExit):
#         raise Exception('Something went wrong. Please refresh browser.')
        

while True:
    temp_input = input('You: ')
    try:
        response_json = full_conversation(temp_input, 
                                            conversation, 
                                            question, 
                                            location, 
                                            latitude,
                                            longitude,
                                            weather_type,
                                            date )

        if response_json:
            response = response_json['response']
            conversation = response_json['conversation']
            question = response_json['question']
            location = response_json['location']
            latitude = response_json['latitude']
            longitude = response_json['longitude']
            weather_type = response_json['weather_type']
            date = response_json['date']


            print(f'Weacher: {response}')
        else:
            print('Weacher: Something went wrong. Try again.')

    except(KeyboardInterrupt, EOFError, SystemExit):
        raise Exception('Something went wrong. Please refresh browser.')


# if __name__ == '__main__':
#     app.run()