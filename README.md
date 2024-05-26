## Weacher -  Your Weather Companion for Travel Planning - 

### What can it do?
Weacher will assist you in checking the weather conditions for various locations during both the planning phase and throughout their travels.

![Weacher Sample](https://github.com/Sozai83/Weacher/assets/58994580/802a4a7b-1339-4f0e-8fa8-cc9b4b455a6e)

### How to install and run Weacher?
1. Clone this repogitry. Run the following command.    
  _git clone https://github.com/Sozai83/Weacher.git_  
2. Run the main.py program  
   _py -m venv env_  
   _env\scripts\activate  
   pip install -r requirements.txt
   py main.py_
4. Run the frontend application in weather_chatbot repogitory    
   _cd .\weather_chatbot\_  
   _npm install_  
   _npm run dev_  

Now you are ready to use Weacher!


### How to use Weacher?
#### 1. Ask weather related questions
You can ask questions with a weather related keyword (weather, temprature, forecast) to trigger weather converstaion with Weacher.
Sample: What's the weather in London and Brisbane?

Once you ask a weather related question, Weacher will ask you some details so they can provide the weather data you are after!

#### 2. Ask recommendation for a location to go today or tomorrow
Weacher can suggest recommended location(s) depending on the weather in the traveler's itenerary.
Sample: Where do you recommend to go tomorrow?

#### 3. Ask random questions
Weacher is also trained to be able to respond for random queries.


### Folder structure - What is stored where?
#### Backend
main.py - Main program to run the application

**bot**
- bot.py: Initializes the chatbot
- converstaion.py: Contains functions to navigate the converstaion flow
- recommendation_adapter.py: Contains logical adapter for recommendation of locations

**classes**
- Geocode.py: Contains Geocode class along with geocode related functions
- Weather.py: Contains Weather class along with searching weather related functions

**init**
- init_db.py: Initialize database
- locations.py: Contains locations dictionary storing locations in the itenerary
- weather_database.py: Contains WeatherDB and LocationDB classes and functions to add data in those tables

**training_files**
- general_training.py: Contains corpus training
- mistyping.py: Contains function to list train chatbot for mistyping
- training.py: Contains function to list train chatbot with greetings

**database**
- weather_app.db: Contains location and weather data

#### Frontend
**weather_chatbot**
Frontend application built with Next.js
