from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


app = Flask(__name__)
db_name = './database/weather_app.db' #replace with your file path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

conversation = ""
question = ""
location = ""
latitude = ""
longitude = ""
weather_type = ""
date = ""


from init.init_db import init_db
# If no weather is retrieved wihtin 24 hours for locations in the itenerary, retireve weather and save it in the database
init_db()

from training_files.mistyping import train_mistype
# List training Weacher for mistyped keywords
train_mistype()

from training_files.training import train_greeing
# List training Weacher for greetings
train_greeing()

from bot.conversation import full_conversation
@app.route('/askWeacher', methods=['POST'])
def ask_weacher():
    try:
        # Check the API attiributes and assign value if there is one
        temp_input = request.args.get('input') if request.args.get('input') else ""
        conversation = request.args.get('conversation') if request.args.get('conversation') else ""
        question = request.args.get('question') if request.args.get('question') else ""
        location = request.args.get('location') if request.args.get('location') else ""
        latitude = request.args.get('latitude') if request.args.get('latitude') else ""
        longitude = request.args.get('longitude') if request.args.get('longitude') else ""
        weather_type = request.args.get('weather_type') if request.args.get('weather_type') else ""
        date = request.args.get('date') if request.args.get('date') else ""
        multilocation = request.args.get('multilocation') if request.args.get('multilocation') else ""

        # Run full_converstaion function to retrieve appropreate reseponse for the input
        response_json = full_conversation(temp_input, 
                                            conversation, 
                                            question, 
                                            location, 
                                            latitude,
                                            longitude,
                                            weather_type,
                                            date,
                                            multilocation)
        
        response = jsonify(response_json)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    except(KeyboardInterrupt, EOFError, SystemExit):
        raise Exception('Something went wrong. Please refresh browser.')

       

if __name__ == '__main__':
    app.run()