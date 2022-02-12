from cgitb import text
import imp
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import json
from difflib import get_close_matches

dictionary = {}

with open('dictionary.json', 'r') as file:
    dictionary = json.load(file)

#print(dictionary)

class MainScreen(Screen):

    def update(self, text):
        words = text.split(' ')
        out = ''
        for word in words:
            match_key = get_close_matches(word, dictionary)
            if match_key:
                out += dictionary[match_key[0]] + ' '
            else:
                out += word + ' '

        self.ids.output.text = out

class SecondScreen(Screen):
    def save(self):
        key = self.ids.input.text.lower()
        value = self.ids.output.text.lower()

        dictionary[key] = value

        with open('dictionary.json', 'w') as file:
            file.write(json.dumps(dictionary))

        self.ids.input.text = ''
        self.ids.output.text = ''


class ThirdScreen(Screen):
    def on_pre_enter(self):
        self.ids['dict_elements'].refresh()

class Dict_elements(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        #self.orientation = 'vertical'
        #self.size_hint = (1, None)
        #self.height = self.minimum_height
        self.refresh()

    def refresh(self):
        self.clear_widgets()

        for entry in sorted(list(dictionary.keys())):

            b = Button(text='usuń', padding=(10, 10))
            #b.on_press = self.remove, args=entry
            b.bind(on_press=self.remove)
            self.ids[entry + '_btn'] = b

            l = Label(text=entry)
            l2 = Label(text=dictionary[entry])
            self.add_widget(l)
            self.add_widget(l2)
            self.add_widget(b)

    def remove(self, instance):
            for id in self.ids:
                if self.ids[id] == instance:
                    id = id.replace('_btn', '')

                    del dictionary[id]

                    with open('dictionary.json', 'w') as file:
                        file.write(json.dumps(dictionary))

                    self.refresh()
            





class AplicationApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        return sm


if __name__ == "__main__":
    AplicationApp().run()