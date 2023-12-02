from flask import *
from init.init_db import init_db
from bot.conversation import full_conversation


app = Flask(__name__)

init_db()


continuous_conversation = ''
temp_location = ''
asked_weather = False


@app.route('/askWeacher',  methods=['POST'])
def ask_weacher():
    try:
        input = request.form['ask_weacher']
        continuous_conversation, asked_weather, location, response = full_conversation(input)

        return response

    except(KeyboardInterrupt, EOFError, SystemExit):
        raise Exception('Something went wrong. Please refresh browser.')
        




if __name__ == '__main__':
    app.run()