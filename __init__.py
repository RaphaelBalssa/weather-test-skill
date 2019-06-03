from mycroft import MycroftSkill, intent_file_handler


class WeatherTest(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('test.weather.intent')
    def handle_test_weather(self, message):
        self.speak_dialog('test.weather')


def create_skill():
    return WeatherTest()

