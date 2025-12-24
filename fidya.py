from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import pygame
import os

# Fullscreen + red background
Window.fullscreen = True
Window.clearcolor = (1, 0, 0, 1)

# Safe sound init
try:
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

SOUND_FILE = "error.wav"
CORRECT_CODE = "my love kali"

class LockScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 50
        self.spacing = 20

        self.label = Label(
            text="Enter the code:",
            font_size=40,
            color=(1, 1, 1, 1)
        )

        self.input = TextInput(
            font_size=32,
            multiline=False,
            halign="right"
        )

        self.button = Button(
            text="Check",
            font_size=32
        )
        self.button.bind(on_release=self.check_code)

        self.add_widget(self.label)
        self.add_widget(self.input)
        self.add_widget(self.button)

    def check_code(self, instance):
        if self.input.text.strip() == CORRECT_CODE:
            # ✅ العودة للوضع الطبيعي
            Window.fullscreen = False
            App.get_running_app().stop()
        else:
            self.label.text = "Wrong code ✖"
            if SOUND_AVAILABLE and os.path.exists(SOUND_FILE):
                pygame.mixer.music.load(SOUND_FILE)
                pygame.mixer.music.play()

class LockApp(App):
    def build(self):
        return LockScreen()

if __name__ == "__main__":
    LockApp().run()
