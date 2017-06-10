"""
Define global configuration variables in here
"""
DEBUG = True

# tokens
SECRET_KEY = "secret"

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:///point.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# maps api
GOOGLEMAPS_KEY = 'AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4'

# forecast api
FORECAST_API_URL = "http://35.187.52.226/api/v1.0/data/forecast/companies/intern"
FORECAST_API_KEY = "i7nAtke5r7n5"
