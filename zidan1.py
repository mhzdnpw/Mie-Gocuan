from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class LoginScreen(Screen):

  def __init__(self, **kwargs):
    super(LoginScreen, self).__init__(**kwargs)
    layout = FloatLayout()

    self.logo = Image(
        source='logo gocuan.png',
        size_hint=(None, None),
        size=(150, 150),
        pos_hint={'center_x': 0.5, 'top': 0.85},
    )
    layout.add_widget(self.logo)

    self.label = Label(
        text='Selamat Datang',
        font_name='Roboto-Bold.ttf',
        font_size=24,
        bold=True,
        color=(1, 1, 1, 1),
        size_hint=(None, None),
        size=(300, 40),
        pos_hint={'center_x': 0.5, 'top': 0.65},
    )
    layout.add_widget(self.label)

    self.username = TextInput(
        hint_text='Username',
        font_name='Roboto-Regular.ttf',
        multiline=False,
        size_hint=(None, None),
        size=(320, 45),
        pos_hint={'center_x': 0.5, 'top': 0.53},
        halign='center',
        background_color=(0.2,0.2, 0.2,0.2), 
        foreground_color=(1, 1, 1, 1),
        hint_text_color=(0.7, 0.7, 0.7, 1), 
    )
    layout.add_widget(self.username)

    self.password = TextInput(
        hint_text='Password',
        font_name='Roboto-Regular.ttf',
        password=True,
        multiline=False,
        size_hint=(None, None),
        size=(320, 45),
        pos_hint={'center_x': 0.5, 'top': 0.47},
        halign='center',
        background_color=(0.2,0.2, 0.2,0.2),
        foreground_color=(1, 1, 1, 1),
        hint_text_color=(0.7, 0.7, 0.7, 1),
    )
    layout.add_widget(self.password)

    login_btn = Button(
        text='LOGIN',
        font_name='Roboto-Bold.ttf',
        size_hint=(None, None),
        size=(320, 45),
        pos_hint={'center_x': 0.5, 'top': 0.37},
        background_color=(0.9, 0.1, 0.4, 1),
    )
    login_btn.bind(on_press=self.to_beranda)
    layout.add_widget(login_btn)

    self.add_widget(layout)

  def update_username_bg(self, instance, value):
    self.username_bg.pos = instance.pos
    self.username_bg.size = instance.size

  def update_password_bg(self, instance, value):
    self.password_bg.pos = instance.pos
    self.password_bg.size = instance.size

  def to_beranda(self, instance):
    self.manager.current = 'beranda'


class BerandaScreen(Screen):
    def __init__(self, **kwargs):
        super(BerandaScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40)
        layout.add_widget(Label(text='Ini Halaman Beranda Mie Gocuan', font_size=24, color=(1, 1, 1, 1)))
        
        back_btn = Button(text='Keluar / Logout', size_hint_y=None, height=50, background_color=(0.9, 0.1, 0.4, 1))
        back_btn.bind(on_press=self.to_login)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def to_login(self, instance):
        self.manager.current = 'login'

class MieGocuanApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(BerandaScreen(name='beranda'))
        return sm

if __name__ == '__main__':
    MieGocuanApp().run()