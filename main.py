from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput


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


    # print(dictionary)
    # print('================')
    # print(keys)
    # print('================')
    # print(values)


def find_matching_keys(maching_values):
    global keys, values
    '''
    funkcja dostaje liste słówek po niepolsku
    zwraca poukładaną listę słówek po polsku
    '''
    maching_keys = []
    for i, value in enumerate(values):
        for j, maching_value in enumerate(maching_values):
            if value == maching_value:
                maching_keys.append(keys[i])
                del maching_values[j]
            if len(maching_values) <= 0:
                return maching_keys
    return maching_keys

def find_matching_values(maching_keys):
    global keys, values
    '''
    funkcja dostaje liste słówek po polsku
    zwraca poukładaną listę słówek po niepolsku
    '''
    maching_values = []
    for i, key in enumerate(keys):
        for j, maching_key in enumerate(maching_keys):
            if key == maching_key:
                maching_values.append(values[i])
                del maching_keys[j]
            if len(maching_keys) <= 0:
                return maching_values
    return maching_values




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

    def translate(self, *args):
        #he he

        '''
        Co sie tu odpierdala?
        świetne pytanie
        nie wiem
        ale tak sprawdzamy status guziczka do zmiany kierunku tłumaczenia
        na 0 tłumaczymy z polskiego na nasze
        na 1 z naszego na polskie

        tłumaczenie polega na podzieleniu wpisanego tekstu
        niestety według spacji czyli związki takie jak cyborg -> umo del mahineri
        działają tylko w jedną stronę
        Moze kiedyś wymyślę jak to naprawić

        potem po podzieleniu szukamy najbliżej wyglądających słów w listach keys (wyrazy po polsku) lub values (wyrazy po niepolsku)
        potem wiedząc, że listy keys i values są w takiej samej kolejności, czyli key[0] to polskie tłumaczenie value[0],
        tworzymy listę znalezionych tłumaczeń
        pierwszy element tej listy zostaje wpisany do okienka z tłumaczeniem
        '''

        if self.translation_mode == 0:
            text = self.ids['input'].text
            words = text.split(' ')
            out = ''
            #print(words)
            for word in words:
                matching_keys = get_close_matches(word, keys) #list of potential key candidates
                matching_values = find_matching_values(matching_keys)

                #print(matching_values)

                if matching_values:
                    if len(matching_values) > 1:
                        self.ids['input1'].text = matching_values[1]
                    else:
                        self.ids['input1'].text = ''
                    if len(matching_values) > 2:
                        self.ids['input2'].text = matching_values[2]
                    else:
                        self.ids['input2'].text = ''
                    if len(matching_values) > 3:
                        self.ids['input3'].text = matching_values[3]
                    else:
                        self.ids['input3'].text = ''

                    out += matching_values[0] + ' '
                else:
                    out += word + ' '

            self.ids.output.text = out

        elif self.translation_mode == 1:
            text = self.ids['output'].text
            words = text.split(' ')
            out = ''
            #print(words)
            for word in words:
                matching_values = get_close_matches(word, values) #list of potential key candidates
                matching_keys = find_matching_keys(matching_values)
 
                #print(matching_keys)

                if matching_keys:
                    if len(matching_keys) > 1:
                        self.ids['output1'].text = matching_keys[1]
                    else:
                        self.ids['output1'].text = ''
                    if len(matching_keys) > 2:
                        self.ids['output2'].text = matching_keys[2]
                    else:
                        self.ids['output2'].text = ''
                    if len(matching_keys) > 3:
                        self.ids['output3'].text = matching_keys[3]
                    else:
                        self.ids['output3'].text = ''

                    out += matching_keys[0] + ' '
                else:
                    out += word + ' '

            self.ids.input.text = out




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
            print('saving', dictionary)
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
        self.refresh()

    def refresh(self):
        load_dictionary()
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