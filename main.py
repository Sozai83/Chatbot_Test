from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


app = Flask(__name__)
db_name = r'./database/weather_app.db' #replace with your file path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from init.init_db import init_db

init_db()

conversation = False
question = ""
location = ""
latitude = ""
longitude = ""
weather_type = ""
date = ""

from bot.conversation import full_conversation


@app.route('/askWeacher', methods=['POST'])
def ask_weacher():
    try:
        temp_input = name = request.args.get('input')
        conversation = request.args.get('conversation') if request.args.get('conversation') else ""
        question = request.args.get('question') if request.args.get('question') else ""
        location = request.args.get('location') if request.args.get('location') else ""
        latitude = request.args.get('latitude') if request.args.get('latitude') else ""
        longitude = request.args.get('longitude') if request.args.get('longitude') else ""
        weather_type = request.args.get('weather_type') if request.args.get('weather_type') else ""
        date = request.args.get('date') if request.args.get('date') else ""

        response_json = full_conversation(temp_input, 
                                            conversation, 
                                            question, 
                                            location, 
                                            latitude,
                                            longitude,
                                            weather_type,
                                            date )
        
        if response_json:
            return response_json
        else:
            return 'Something went wrong. Try again.'

    except(KeyboardInterrupt, EOFError, SystemExit):
        raise Exception('Something went wrong. Please refresh browser.')

        

# while True:
#     temp_input = input('You: ')
#     try:
#         response_json = full_conversation(temp_input, 
#                                             conversation, 
#                                             question, 
#                                             location, 
#                                             latitude,
#                                             longitude,
#                                             weather_type,
#                                             date )

#         if response_json:
#             response = response_json['response']
#             conversation = response_json['conversation']
#             question = response_json['question']
#             location = response_json['location']
#             latitude = response_json['latitude']
#             longitude = response_json['longitude']
#             weather_type = response_json['weather_type']
#             date = response_json['date']


#             print(f'Weacher: {response}')
#         else:
#             print('Weacher: Something went wrong. Try again.')

#     except(KeyboardInterrupt, EOFError, SystemExit):
#         raise Exception('Something went wrong. Please refresh browser.')


if __name__ == '__main__':
    app.run()