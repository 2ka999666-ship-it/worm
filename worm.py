from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import pygame
import os
import random

# Fullscreen + red background
Window.fullscreen = True
Window.clearcolor = (0.7, 0, 0, 1)

# Sound init
try:
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

SOUND_FILE = "error.wav"
CORRECT_CODE = "my love kali"
VICTIM_ID = f"ID-{random.randint(100000,999999)}"

class LockScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 40
        self.spacing = 15

        # Countdown time (seconds)
        self.time_left = 300  # 5 minutes
        self.blink_state = True

        # Warning text
        self.warning_label = Label(
            text=self.warning_text(),
            font_size=36,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle"
        )
        self.warning_label.bind(size=self.warning_label.setter("text_size"))

        # Timer label
        self.timer_label = Label(
            text="Time Remaining: 05:00",
            font_size=28,
            color=(1, 1, 0, 1)
        )

        # Input
        self.input = TextInput(
            font_size=28,
            multiline=False,
            halign="center"
        )

        # Button
        self.button = Button(
            text="DECRYPT FILES",
            font_size=28
        )
        self.button.bind(on_release=self.check_code)

        self.add_widget(self.warning_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.input)
        self.add_widget(self.button)

        # Start countdown + blinking
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.blink_text, 0.5)

        # Play looping sound
        if SOUND_AVAILABLE and os.path.exists(SOUND_FILE):
            pygame.mixer.music.load(SOUND_FILE)
            pygame.mixer.music.play(-1)

    def warning_text(self):
        return (
            "!!! WARNING !!!\n\n"
            "YOUR DEVICE HAS BEEN INFECTED WITH RANSOMWARE\n\n"
            "All your files have been encrypted.\n"
            "Do NOT close this window.\n\n"
            f"Victim ID: {VICTIM_ID}\n\n"
            "Enter the correct decryption code\n"
            "before the timer reaches zero."
        )

    def update_timer(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            m = self.time_left // 60
            s = self.time_left % 60
            self.timer_label.text = f"Time Remaining: {m:02d}:{s:02d}"
        else:
            self.timer_label.text = "TIME EXPIRED!"
            self.timer_label.color = (1, 0, 0, 1)

    def blink_text(self, dt):
        # Text blinking effect
        self.blink_state = not self.blink_state
        if self.blink_state:
            self.warning_label.color = (1, 1, 1, 1)
        else:
            self.warning_label.color = (1, 0.2, 0.2, 1)

    def check_code(self, instance):
        if self.input.text.strip() == CORRECT_CODE:
            if SOUND_AVAILABLE:
                pygame.mixer.music.stop()
            Window.fullscreen = False
            App.get_running_app().stop()
        else:
            self.warning_label.text = (
                "INVALID CODE!\n\n"
                "FILES REMAIN ENCRYPTED.\n\n"
                f"Victim ID: {VICTIM_ID}"
            )

class LockApp(App):
    def build(self):
        return LockScreen()

if __name__ == "__main__":
    LockApp().run()
