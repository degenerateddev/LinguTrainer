from kivy.config import Config
from kivy.app import App
from kivymd.theming import ThemeManager
import kivy
import json
import requests

### CUSTOM IMPORTS ###
from modules import floatlayout

kivy.require('1.11.0')

class KivyGUI(App):
    def __init__(self, **kwargs):
        super(KivyGUI, self).__init__(**kwargs)                         #### App.__init__(self) also works! ####
        self.firebaseURL = ("https://lingutrainer.firebaseio.com/")

    theme_cls = ThemeManager()
    theme_cls.primary_palette = ("Teal")
    theme_cls.theme_style = ("Dark")
    title = ("Lingu Trainer")
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


    """ Syntax to create databases: {"Parent": {"Child1": "Value", "Child2": "Value2"}} """

    def patchWordlists(self, languageDownloadChoice, Checkbox):
        #floatlayout.LayoutPy.ids.ckbxe or floatlayout.LayoutPy.ids.ckbxe or floatlayout.LayoutPy.ids.ckbxe
        if Checkbox in floatlayout.LayoutPy.checkboxes:
            print(f"You already have the language: {languageDownloadChoice} installed, we continue now...")
        elif Checkbox not in floatlayout.LayoutPy.checkboxes:
            to_database = json.loads(languageDownloadChoice)
            requests.patch(url=self.firebaseURL, to=to_database)

    def postWordlists(self, languageDownloadChoice, Checkbox):
        if Checkbox in floatlayout.LayoutPy.checkboxes:
            print(f"You already have the language: {languageDownloadChoice} installed, we continue now...")
        elif Checkbox not in floatlayout.LayoutPy.checkboxes:
            to_database = json.loads(languageDownloadChoice)
            requests.post(url=self.firebaseURL, to=to_database)

    def putWordlists(self, languageDownloadChoice, Checkbox):
        if Checkbox in floatlayout.LayoutPy.checkboxes:
            print(f"You already have the language: {languageDownloadChoice} installed, we continue now...")
        elif Checkbox not in floatlayout.LayoutPy.checkboxes:
            to_database = json.loads(languageDownloadChoice)
            requests.put(url=self.firebaseURL, to=to_database)

    def deleteWordlists(self, languageDownloadChoice, Checkbox):
        if Checkbox in floatlayout.LayoutPy.checkboxes:
            print(f"You already have the language: {languageDownloadChoice} installed, we continue now...")
        elif Checkbox not in floatlayout.LayoutPy.checkboxes:
            to_database = json.loads(languageDownloadChoice)
            requests.delete(url=self.firebaseURL, to=to_database)

    def build(self):
        c = floatlayout.LayoutPy()
        return c


if __name__ == "__main__":
    KivyGUI().run()