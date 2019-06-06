import time
from datetime import datetime
import datetime as dt
from copy import copy
import json

import mycroft.audio
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from pyowm import OWM
from mycroft.dialog import DialogLoader
from mycroft.api import Api
from mycroft.messagebus.message import Message
from mycroft.util.format import nice_time
from mycroft.util.log import LOG
from mycroft.util.parse import extract_datetime
from mycroft.util.format import nice_number
from requests import HTTPError
import sqlite3

try:
    from mycroft.util.time import to_utc, to_local
except Exception:
    import pytz

class LocationNotFoundError(ValueError):
    pass

APIErrors = (LocationNotFoundError, HTTPError)

class WeatherTest(MycroftSkill):
    def __init__(self):
        super().__init__("WeatherTest")

    @intent_file_handler('test.weather.intent')
    def handle_test_weather_f(self, message):
        self.handle_test_weather(message)   

    # Handle: fetch temperature from company.db
    @intent_handler(IntentBuilder("").require("Query").optionally(
        "Date").optionally("Location").build())
    def handle_test_weather(self, message):

        try:

            res={}
            connection = sqlite3.connect("company.db")

            c = connection.cursor()
            
            c.execute("SELECT degree FROM DAILY_FORECAST WHERE date = date('now')")
            res["degree"] = c.fetchone()
            connection.commit()
            connection.close()

            if(res["degree"] is None):
                self.speak_dialog('test.weather.noforecast')
                return

            self.speak_dialog('test.weather', res)
           

        except APIErrors as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    def __api_error(self, e):
        if isinstance(e, LocationNotFoundError):
            self.speak_dialog('location.not.found')
        elif e.response.status_code == 401:
            from mycroft import Message
            self.bus.emit(Message("mycroft.not.paired"))

def create_skill():
    return WeatherTest()