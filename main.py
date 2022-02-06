from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

import json
from difflib import get_close_matches

dictionary = {}

with open('dictionary.json', 'w') as file:

    dictionary = {

        'Paweł' : "Pablo",
        'ty' : 'duo',
        'chuju' : 'kutaczi',
        'twoja' : 'donna',
        'mama' : 'mamma',
        'to' : 'es',
        'chuj' : 'chujoczita',

    }

    file.write(json.dumps(dictionary))



with open('dictionary.json', 'r') as file:
    dictionary = json.load(file)

print(dictionary)

class MainScreen(Screen):

    def update(self, text):
        words = text.split(' ')
        out = ''
        for word in words:
            match_key = get_close_matches(word, dictionary)
            if match_key:
                out += dictionary[match_key[0]] + ' '

        self.ids.output.text = out

class SecondScreen(Screen):
    pass


class AplicationApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        return sm


if __name__ == "__main__":
    AplicationApp().run()