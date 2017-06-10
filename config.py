
"""
Define test configuration variables in here
"""
DEBUG = True
TESTING = True

# tokens
SECRET_KEY = "your secret key"

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# maps api
GOOGLEMAPS_KEY = 'your api key'

# forecast api
FORECAST_API_URL = "your api url"
FORECAST_API_KEY = "your api key"