import random
import numpy as np
import matplotlib
import sys
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.base import runTouchApp
import buildozer
from kivymd.theming import ThemeManager
from kivymd.label import MDLabel
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from collections import namedtuple
from kivymd.toast.kivytoast import toast
from kivymd.dialog import MDInputDialog, MDDialog
from kivy.utils import get_hex_from_color
from kivymd.list import IRightBodyTouch, ILeftBody
from kivymd.selectioncontrols import MDCheckbox
from kivymd.progressloader import MDProgressLoader
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from googleads import ad_manager
from kivymd.material_resources import DEVICE_IOS            # Checking for device (android or ios)
import time
import socket
from plyer import vibrator
from plyer import stt, tts
from plyer import notification

### CUSTOM IMPORTS ###
from LinguTrainer import main
from modules import getLists

kivy.require('1.11.0')

TOTAL = 0
RIGHT = 0

class LayoutPy(FloatLayout):
    def __init__(self, **kwargs):
        super(LayoutPy, self).__init__(**kwargs)
        Window.clearcolor = (1, 0, 0, 1)
        self.scr_mngr = ObjectProperty(None)
        self.frgz = ("src/fragezeichen.png")
        self.fs = ("src/falsch.png")
        self.rtg = ("src/richtig.png")
        self.input_language = ("German")        ### Has to be user input! ###
        self.checkboxes = [self.ids.ckbxe, self.ids.ckbxs, self.ids.ckbxhv, self.ids.ckbxg]

        self.show_lbl = MDLabel(text="", font_style="H6", font_size=30, size_hint=((0.55, 0.1)), pos_hint={"x": 0.5, "top": 0.85})
        self.add_widget(self.show_lbl)

    def GetVocs(self, language):                    # Executed when a language is set and the main window is shown
        with open(f"languages/{language}.txt", "r") as file:  # Open the file (language = if button = english then language = english (has to be implemented!))
            self.entries = []                               # List of vocs
            for i in file.readlines():              # Reading all vocs from list
                i = i.strip(" = ").strip("\n").lower()
                self.language_word, self.input_language_word = i.split(" = ")
                self.Entry = namedtuple("Entry", ["language_word", "input_language_word"])
                self.entries.append(self.Entry(self.language_word, self.input_language_word))
            self.random_voc = random.choice(self.entries)
            self.show_lbl.text = str(self.random_voc.language_word)
            return str(self.random_voc.language_word)

    def check(self, total, right):
        #total = total
        #right = right
        global TOTAL, RIGHT
        self.defaultAttempts = 10

        if self.check_input_words() == "True":
            RIGHT += 1
            TOTAL += 1
            print(TOTAL, RIGHT)
            self.ids.counter_lbl.text = (f"Right: {RIGHT} \nFalse: {TOTAL - RIGHT}")
        elif self.check_input_words() == "False":
            TOTAL += 1
            print(TOTAL, RIGHT)
            self.ids.counter_lbl.text = (f"Right: {RIGHT} \nFalse: {TOTAL - RIGHT}")
        elif self.check_input_words() == "No input":
            print("No input!")
        elif TOTAL >= self.defaultAttempts:
            ratio = RIGHT * 100 / TOTAL  # Maybe right / wrong of total as labels
            if ratio > 50:
                print(f"You answered {RIGHT} question out of {TOTAL} correct.")
                print(f"Your right/false ratio is {ratio}% \nThis is pretty good!")
                self.ids.counter_lbl.text = (f"Right/false ratio after {defaultAttempts} : {ratio} ... not bad!")
            elif ratio < 50:
                print(f"You answered {RIGHT} question out of {TOTAL} correct.")
                print(f"Your right/false ratio is {ratio}% \n Don't worry... you will get better!")
                self.ids.counter_lbl.text = (f"Right/false ratio after {defaultAttempts} : {ratio} ... you should practice more!")

    def check_input_words(self):                        # Executed when "check" button is clicked
        input_words = self.ids.input_words.text.lower()
        question_words = self.show_lbl.text.lower()
        print("Input: ", input_words)
        print("Vocab: ", question_words)
        #print(self.total, self.right)
        if input_words == "":
            #print("No input!")
            img = self.frgz
            state = ("None")
            self.showIfRightOrFalse(state)
            return str("No input")
        elif input_words == self.random_voc.input_language_word:
            print(f"You are right: {input_words} = {self.random_voc.language_word} !")
            #self.right += 1
            #self.total += 1
            self.show_lbl.text = self.GetVocs(self.language_set)
            self.ids.input_words.text = ("")
            img = self.rtg
            state = ("Correct")
            self.showIfRightOrFalse(state)
            return "True"
        elif input_words != self.random_voc.input_language_word:
            print(f"Wrong translation: {input_words} != {self.random_voc.language_word}")
            #self.total += 1
            img = self.fs
            state = ("Incorrect")
            self.showIfRightOrFalse(state)
            return "False"

    def open2ndScreen(self, screen):
        if self.ids.scr_mngr.current != ("screen_main") and self.ids.scr_mngr.current != ("hidden_screen"):
            self.ids.scr_mngr.current = ("screen_main")
        else:
            self.show_lbl.text = ("")
            self.ids.scr_mngr.current = screen

    def setLanguage(self, language, screen, checkbox):                  # Executed when checkboxes are clicked to set the language to train with
        self.ids.scr_mngr.current = screen          # Switching back
        self.language_set = language
        self.Downloaded = True                                                  # Checking if the wordlist for the language is already downloaded
        print(self.language_set)
        self.ids.language_label.text = (f"Language: {self.language_set}")       # Showing the user which language is set
        try:
            self.GetVocs(self.language_set)                                 # Getting vocab list of chosen language
            # Need method for switching 'Downloaded' boolean
            if self.Downloaded:
                pass
            else:
                main.KivyGUI.patchWordlists(language, checkbox)
        except IndexError as ie:
            print(ie)

    def add_Own_Wordlist(self): ### Add bubble with wordlist syntax ###
        pass

    def Switch_Languages(self):
        print(f"Actual Language: {self.language_set}")
        print(f"Language to be set: {self.input_language}")
        self.input_language_word = self.language_word

    def setImgPlaceholder(self):
        with self.ids.right_false_lbl.canvas.before:
            Color(.4, .4, .4, 1)
            texture = CoreImage("src/platzhalterTransparent.png").texture
            texture.wrap = "repeat"
            return Rectangle(pos=self.ids.right_false_lbl.pos, size=self.ids.right_false_lbl.size, texture=texture)

    def showIfRightOrFalse(self, state):        # Setting images here for right / false state
        activeImage = []
        imgLbl = self.ids.right_false_lbl
        if state == ("Correct"):
            #imgLbl.canvas.clear()
            #self.setImgPlaceholder()
            del activeImage[0:5]
            with imgLbl.canvas.before:
                activeImage.append("src/richtigTransparent.png")
                Color(.4, .4, .4, 1)
                texture = CoreImage(str(activeImage).strip("[").strip("]").strip("'")).texture
                texture.wrap = "repeat"
                Rectangle(pos=imgLbl.pos, size=imgLbl.size, texture=texture)
        elif state == ("Incorrect"):
            #imgLbl.canvas.clear()
            #self.setImgPlaceholder()
            del activeImage[0:5]
            with imgLbl.canvas.before:
                activeImage.append("src/falschTransparent.png")
                Color(.4, .4, .4, 1)
                texture = CoreImage(str(activeImage).strip("[").strip("]").strip("'")).texture
                texture.wrap = "repeat"
                Rectangle(pos=imgLbl.pos, size=imgLbl.size, texture=texture)
        elif state == ("None"):
            #imgLbl.canvas.clear()
            #self.setImgPlaceholder()
            del activeImage[0:5]

    def Popup(self, *args):
        Isinput = args[0]
        if Isinput != True:
            popup = MDDialog(
                            title=f'{args[1]}',
                            text=f'[color=%s][b]{args[2]}[/b][/color]' % get_hex_from_color(
                                main.KivyGUI.theme_cls.primary_color),
                            events_callback=self.callback,
                            size_hint=(.5, .5), text_button_ok='Ok', text_button_cancel='Cancel')
            popup.open()
        elif Isinput == True:
            popup = MDInputDialog(
                            title=f'{args[1]}',
                            events_callback=self.callback,
                            size_hint=(.8, .4), text_button_ok='Sent', hint_text='Hint text')               # .8, .4
            self.open2ndScreen("screen_main")
            popup.open()

    def backend(self):      ### NOT FINISHED!!! ###
        # Server - side Backend
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_server = ("placeholder.eu")
        port = 8000
        print(host_server)
        print(port)
        server_socket.bind((host_server, port))
        server_socket.send(self.ids.dev_msg)

    def callback(self, *args):
        toast(args[0])

    def hide_screen(self):
        if self.ids.nav_drawer.active_item:
            self.ids.nav_layout.toggle_nav_drawer()
            setattr(self.ids.scr_mngr, "current", "hidden_screen")
            self.show_lbl.text = ""

    def progressLoader(self):
        link = ("https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/c1/c18022bda4bedb3756b3464166b46259b32ecda1_full.jpg")
        self.directory = "src/"
        progress = MDProgressLoader(
            url_on_image=link,
            path_to_file=os.path.join(self.directory, 'image.jpg'),
            download_complete=self.download_complete,
            download_hide=self.download_progress_hide
        )
        progress.start(self.ids.box)

    def exit(self):
        #vibrator.vibrate(1)
        sys.exit(1)

Builder.load_file("design.kv")