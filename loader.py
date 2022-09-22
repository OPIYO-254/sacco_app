from kaki.app import App
from kivy.factory import Factory
from kivymd.app import MDApp


class MDLive(App, MDApp):

    CLASSES = {
        "SojrelApp": "main"
    }
    AUTORELOADER_PATHS = [
        (".", {'recursive': True})
    ]

    def build_app(self, *args):
        print('inside hotreloader')
        return Factory.SojrelApp()


MDLive().run()
