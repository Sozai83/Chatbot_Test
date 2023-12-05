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


conversation = ""
question = ""
location = ""
latitude = ""
longitude = ""
weather_type = ""
date = ""

from mistyping import train_mistype
train_mistype()

from bot.conversation import full_conversation
@app.route('/askWeacher', methods=['POST'])
def ask_weacher():
    try:
        temp_input = request.args.get('input') if request.args.get('input') else ""
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
        
        response = jsonify(response_json)
        response.headers.add('Access-Control-Allow-Origin', '*')

        if response:
            return response
        else:
            return 'Something went wrong. Try again.'

    except(KeyboardInterrupt, EOFError, SystemExit):
        raise Exception('Something went wrong. Please refresh browser.')

       

if __name__ == '__main__':
    app.run()