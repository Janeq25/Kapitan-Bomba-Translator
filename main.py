from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import NumericProperty

import json
from difflib import get_close_matches

'''
Kurwa po strogich myślenicach dochodzę do wniosku,
że lepiej to zrobić na tablicy 2 wymiarowej zamiast
na dictionary.
W dictionary klucze nie mogą się powtarzać, czyli jak teraz ktoś
doda np penis = cazzo i potem penis = kutaczi, to cyborg zapamięta
tylko to drugie.
Kuuuurwa lepiej
zrobie liste 3 wymiarową i bedzie tak lista = [[polskie, zjebane, numerek], []...]
numerek to będzie ile razy dane tłumaczenie zostało wybrane
bo zrobie jeszcze taki paseczek gdzie program będzie podawał
ze trzy najlepsze wyniki i se będzie można wybrać
'''


dictionary = [[]] # [['polskie', 'kosmiczne', 'cyferka'], [p, k, c], [p, k, c]]
keys = []
values = []

def load_dictionary():
    global dictionary, keys, values
    with open('dictionary.json', 'r') as file:
        dictionary = json.load(file)

    #sorting aplhabetically for keys
    dictionary = sorted(dictionary)

    keys = []
    values = []

    for entry in dictionary:
        keys.append(entry[0])
        values.append(entry[1])


    print(dictionary)
    print('================')
    print(keys)
    print('================')
    print(values)



load_dictionary()

class MainScreen(Screen):
    translation_mode = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)

    def switch_mode(self):
        if self.translation_mode == 0:
            self.translation_mode = 1
        elif self.translation_mode == 1:
            self.translation_mode = 0

    def update(self, text):

        if self.translation_mode == 0:
            words = text.split(' ')
            out = ''
            for word in words:
                matching_keys = get_close_matches(word, keys) #list of potential key candidates
                matching_values = []
                for entry in dictionary:
                    for key in matching_keys:
                        if key == entry[0]:
                            matching_values.append(entry[1])

                if matching_keys:
                    out += matching_values[0] + ' '
                else:
                    out += word + ' '

            self.ids.output.text = out

        elif self.translation_mode == 1:
            words = text.split(' ')
            out = ''
            for word in words:
                matching_values = get_close_matches(word, values) #list of potential key candidates
                matching_keys = []
                for entry in dictionary:
                    for value in matching_values:
                        if value == entry[1]:
                            matching_keys.append(entry[2])

                if matching_values:
                    out += matching_keys[0] + ' '
                else:
                    out += word + ' '

            self.ids.output.text = out




class SecondScreen(Screen):
    def save(self):
        key = self.ids.input.text.lower()
        value = self.ids.output.text.lower()

        already_in_database = False

        for i, entry in enumerate(dictionary):
            if entry[0] == key and entry[1] == value:
                dictionary[i][2] += 1
                already_in_database = True
                break

        if not already_in_database:
            print(key, value, 0)
            dictionary.append([key, value, 0])            

        with open('dictionary.json', 'w') as file:
            file.write(json.dumps(dictionary))

        self.ids.input.text = ''
        self.ids.output.text = ''


class ThirdScreen(Screen):
    
    def on_pre_enter(self):
        self.ids['dict_elements'].refresh()
        print('refreshing')

class Dict_elements(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        #self.orientation = 'vertical'
        #self.size_hint = (1, None)
        #self.height = self.minimum_height
        load_dictionary()
        self.refresh()

    def refresh(self):
        self.clear_widgets()

        for i, key in enumerate(keys):

            b = Button(text='usuń', padding=(10, 10))
            #b.on_press = self.remove, args=entry
            b.bind(on_press=self.remove)
            self.ids[key + '_' + values[i] + '_btn'] = b

            l = Label(text=key)
            l2 = Label(text=values[i])
            self.add_widget(l)
            self.add_widget(l2)
            self.add_widget(b)

    def remove(self, instance):
            for id in self.ids:
                if self.ids[id] == instance:
                    id = id.replace('_btn', '').split('_')
                    key = id[0]
                    value = id[1]

                    for i, entry in enumerate(dictionary):
                        if entry[0] == key and entry[1] == value:
                            del keys[i]
                            del values[i]
                            del dictionary[i]

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