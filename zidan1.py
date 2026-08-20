from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text='Selamat Datang', font_size=28, bold=True, color=(1, 1, 1, 1)))
        
        self.username = TextInput(hint_text='Username', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.username)
        
        self.password = TextInput(hint_text='Password', password=True, multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.password)
        
        login_btn = Button(text='LOGIN', size_hint_y=None, height=50, background_color=(0.9, 0.1, 0.4, 1))
        login_btn.bind(on_press=self.to_beranda)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)

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