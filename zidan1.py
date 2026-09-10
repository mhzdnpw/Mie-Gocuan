import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.size = (360, 640)

def init_db():
    conn = sqlite3.connect('gocuan.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            item_name TEXT,
            price TEXT,
            quantity INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            details TEXT,
            total TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            time TEXT
        )
    ''')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES ('zidan', '123')")
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

init_db()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=[25, 30, 25, 30], 
            spacing=12, 
            size_hint=(0.9, None), 
            height=460,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        with main_layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.bg_rect = RoundedRectangle(size=main_layout.size, pos=main_layout.pos, radius=[16])
        main_layout.bind(size=self._update_bg, pos=self._update_bg)

        self.logo = Image(
            source='logo gocuan.png',
            size_hint=(None, None),
            size=(75, 75),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(self.logo)

        self.title_label = Label(
            text='Selamat Datang',
            font_size=20,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=30,
            halign='center'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        main_layout.add_widget(self.title_label)

        self.subtitle_label = Label(
            text='Silakan masuk ke akun Anda',
            font_size=13,
            color=(0.65, 0.65, 0.65, 1),
            size_hint=(1, None),
            height=22,
            halign='center'
        )
        self.subtitle_label.bind(size=self.subtitle_label.setter('text_size'))
        main_layout.add_widget(self.subtitle_label)

        main_layout.add_widget(Label(size_hint=(1, None), height=2))

        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint=(1, None),
            height=44,
            font_size=13,
            padding_x=[12, 12],
            padding_y=[12, 10],
            background_color=(0.18, 0.18, 0.18, 1), 
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
        )
        main_layout.add_widget(self.username)

        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=44,
            font_size=13,
            padding_x=[12, 12],
            padding_y=[12, 10],
            background_color=(0.18, 0.18, 0.18, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
        )
        main_layout.add_widget(self.password)

        self.error_label = Label(
            text='',
            font_size=12,
            color=(1, 0.35, 0.35, 1),
            size_hint=(1, None),
            height=20,
            halign='center'
        )
        self.error_label.bind(size=self.error_label.setter('text_size'))
        main_layout.add_widget(self.error_label)

        login_btn = Button(
            text='MASUK',
            font_size=14,
            bold=True,
            size_hint=(1, None),
            height=44,
            background_color=(0.9, 0.1, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.to_beranda)
        main_layout.add_widget(login_btn)

        reg_btn = Button(
            text='Belum punya akun? Buat Akun',
            font_size=12,
            size_hint=(1, None),
            height=28,
            background_color=(0, 0, 0, 0),
            color=(0.6, 0.7, 1, 1)
        )
        reg_btn.bind(on_press=self.to_register)
        main_layout.add_widget(reg_btn)

        root = FloatLayout()
        root.add_widget(main_layout)
        self.add_widget(root)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def to_beranda(self, instance):
        u = self.username.text.strip()
        p = self.password.text.strip()
        
        if not u or not p:
            self.error_label.text = "Username dan Password tidak boleh kosong!"
            return

        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        account = cursor.fetchone()
        conn.close()
        
        if account:
            self.error_label.text = ""
            self.username.text = ""
            self.password.text = ""
            app = App.get_running_app()
            app.current_user = u
            app.root.get_screen('beranda').update_greeting()
            app.root.get_screen('keranjang').load_cart()
            app.root.get_screen('pesanan').load_orders()
            app.root.get_screen('profil').load_profile()
            app.root.current = 'beranda'
        else:
            self.error_label.text = "Username atau Password salah!"

    def to_register(self, instance):
        self.error_label.text = ""
        self.username.text = ""
        self.password.text = ""
        self.manager.current = 'register'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=[25, 30, 25, 30], 
            spacing=12, 
            size_hint=(0.9, None), 
            height=400,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        with main_layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.bg_rect = RoundedRectangle(size=main_layout.size, pos=main_layout.pos, radius=[16])
        main_layout.bind(size=self._update_bg, pos=self._update_bg)

        self.title_label = Label(
            text='Buat Akun Baru',
            font_size=20,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=32,
            halign='center'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        main_layout.add_widget(self.title_label)

        main_layout.add_widget(Label(size_hint=(1, None), height=5))

        self.username = TextInput(
            hint_text='Username Baru',
            multiline=False,
            size_hint=(1, None),
            height=44,
            font_size=13,
            padding_x=[12, 12],
            padding_y=[12, 10],
            background_color=(0.18, 0.18, 0.18, 1), 
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
        )
        main_layout.add_widget(self.username)

        self.password = TextInput(
            hint_text='Password Baru',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=44,
            font_size=13,
            padding_x=[12, 12],
            padding_y=[12, 10],
            background_color=(0.18, 0.18, 0.18, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
        )
        main_layout.add_widget(self.password)

        self.error_label = Label(
            text='',
            font_size=12,
            color=(1, 0.35, 0.35, 1),
            size_hint=(1, None),
            height=20,
            halign='center'
        )
        self.error_label.bind(size=self.error_label.setter('text_size'))
        main_layout.add_widget(self.error_label)

        save_btn = Button(
            text='DAFTAR',
            font_size=14,
            bold=True,
            size_hint=(1, None),
            height=44,
            background_color=(0.1, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.register_user)
        main_layout.add_widget(save_btn)

        back_btn = Button(
            text='Sudah punya akun? Login',
            font_size=12,
            size_hint=(1, None),
            height=28,
            background_color=(0, 0, 0, 0),
            color=(0.8, 0.8, 0.8, 1)
        )
        back_btn.bind(on_press=self.to_login)
        main_layout.add_widget(back_btn)

        root = FloatLayout()
        root.add_widget(main_layout)
        self.add_widget(root)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def register_user(self, instance):
        u = self.username.text.strip()
        p = self.password.text.strip()

        if not u or not p:
            self.error_label.color = (1, 0.35, 0.35, 1)
            self.error_label.text = "Username & Password tidak boleh kosong!"
            return

        try:
            conn = sqlite3.connect('gocuan.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            conn.commit()
            conn.close()
            self.error_label.color = (0.3, 1, 0.4, 1)
            self.error_label.text = "Registrasi Berhasil! Silakan Login."
            self.username.text = ""
            self.password.text = ""
        except sqlite3.IntegrityError:
            self.error_label.color = (1, 0.35, 0.35, 1)
            self.error_label.text = "Username sudah terpakai!"

    def to_login(self, instance):
        self.error_label.text = ""
        self.username.text = ""
        self.password.text = ""
        self.manager.current = 'login'


class MenuCard(FloatLayout):
    def __init__(self, img_src, title_text, price_text, **kwargs):
        super(MenuCard, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 165
        
        self.img_src = img_src
        self.title_text = title_text
        self.price_text = price_text

        with self.canvas.before:
            Color(0.18, 0.18, 0.18, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(size=self._update_canvas, pos=self._update_canvas)
        
        self.add_widget(Image(source=img_src, size_hint=(0.82, 0.46), pos_hint={'center_x': 0.5, 'top': 0.91}))
        
        title = Label(text=title_text, font_size=13, bold=True, color=(1,1,1,1), size_hint=(0.85, None), height=18, pos_hint={'x': 0.08, 'top': 0.37}, halign='left', valign='middle')
        title.bind(size=title.setter('text_size'))
        self.add_widget(title)
        
        price = Label(text=price_text, font_size=12, color=(0.85, 0.85, 0.85, 1), size_hint=(0.85, None), height=16, pos_hint={'x': 0.08, 'top': 0.21}, halign='left', valign='middle')
        price.bind(size=price.setter('text_size'))
        self.add_widget(price)
        
        self.btn = Button(background_color=(0,0,0,0), size_hint=(1, 1), pos_hint={'x':0, 'y':0})
        self.btn.bind(on_press=self.add_to_cart)
        self.add_widget(self.btn)

    def _update_canvas(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def add_to_cart(self, instance):
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, quantity FROM cart WHERE username=? AND item_name=?", (username, self.title_text))
        existing = cursor.fetchone()
        
        if existing:
            new_qty = existing[1] + 1
            cursor.execute("UPDATE cart SET quantity=? WHERE id=?", (new_qty, existing[0]))
        else:
            cursor.execute("INSERT INTO cart (username, item_name, price, quantity) VALUES (?, ?, ?, 1)", (username, self.title_text, self.price_text))
            
        conn.commit()
        conn.close()
        app.root.get_screen('keranjang').load_cart()
        
        box = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        msg_label = Label(
            text=f"Berhasil ditambahkan ke keranjang:\n[b]{self.title_text}[/b]",
            markup=True,
            font_size=13,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        msg_label.bind(size=msg_label.setter('text_size'))
        box.add_widget(msg_label)
        
        ok_btn = Button(
            text="OK",
            font_size=13,
            bold=True,
            size_hint=(1, None),
            height=40,
            background_color=(0.9, 0.1, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        box.add_widget(ok_btn)
        
        popup = Popup(
            title="Informasi Keranjang",
            title_size=14,
            title_align='center',
            content=box,
            size_hint=(None, None),
            size=(280, 160),
            auto_dismiss=True
        )
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()


def create_bottom_nav(current_screen_name):
    nav_layout = BoxLayout(size_hint=(1, 0.085), pos_hint={'bottom': 1, 'left': 1}, padding=4, spacing=4)
    with nav_layout.canvas.before:
        Color(0.1, 0.1, 0.1, 1)
        nav_bg = RoundedRectangle(size=nav_layout.size, pos=nav_layout.pos)
    nav_layout.bind(size=lambda i, v: setattr(nav_bg, 'size', v), pos=lambda i, v: setattr(nav_bg, 'pos', v))
    
    screens = [
        ('Beranda', 'beranda'), 
        ('Pesanan', 'pesanan'), 
        ('Keranjang', 'keranjang'), 
        ('Profil', 'profil')
    ]
    
    for text, name in screens:
        is_current = (current_screen_name == name)
        
        btn = Button(
            text=text,
            font_size=12,
            bold=is_current,
            halign='center',
            valign='middle',
            background_color=(0, 0, 0, 0),
            color=(0.9, 0.1, 0.4, 1) if is_current else (0.65, 0.65, 0.65, 1)
        )
        btn.bind(size=btn.setter('text_size'))
        btn.bind(on_press=lambda x, s_name=name: setattr(App.get_running_app().root, 'current', s_name))
        
        nav_layout.add_widget(btn)
        
    return nav_layout


class BerandaScreen(Screen):
    def __init__(self, **kwargs):
        super(BerandaScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        self.scroll = ScrollView(size_hint=(1, 0.915), pos_hint={'top': 1, 'left': 1})
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=12, spacing=12)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        header_layout = FloatLayout(size_hint=(1, None), height=44)
        menu_icon_btn = Button(text='Menu', size_hint=(None, None), size=(50, 32), pos_hint={'left': 0, 'center_y': 0.5}, background_color=(0,0,0,0), font_size=13, color=(1,1,1,1), bold=True)
        menu_icon_btn.bind(on_press=self.open_menu_popup)
        
        logo_img = Image(source='logo gocuan.png', size_hint=(None, None), size=(34, 34), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        notif_btn = Button(text='Info', size_hint=(None, None), size=(45, 32), pos_hint={'right': 1, 'center_y': 0.5}, background_color=(0,0,0,0), font_size=13, color=(1,1,1,1), bold=True)
        notif_btn.bind(on_press=self.open_notif_popup)
        
        header_layout.add_widget(menu_icon_btn)
        header_layout.add_widget(logo_img)
        header_layout.add_widget(notif_btn)
        self.content_layout.add_widget(header_layout)

        self.greeting_label = Label(text="Hi, Zidan\nMau makan apa hari ini?", font_size=17, bold=True, halign='left', valign='middle', size_hint=(1, None), height=52, color=(1, 1, 1, 1))
        self.greeting_label.bind(size=self.greeting_label.setter('text_size'))
        self.content_layout.add_widget(self.greeting_label)

        self.search_input = TextInput(hint_text='Cari menu...', multiline=False, size_hint=(1, None), height=40, font_size=13, background_color=(0.15, 0.15, 0.15, 1), foreground_color=(1, 1, 1, 1), hint_text_color=(0.6, 0.6, 0.6, 1))
        self.search_input.bind(text=self.filter_menu)
        self.content_layout.add_widget(self.search_input)

        self.menu_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12)
        self.menu_container.bind(minimum_height=self.menu_container.setter('height'))
        
        self.load_all_menus()
        self.content_layout.add_widget(self.menu_container)

        self.scroll.add_widget(self.content_layout)
        self.root_layout.add_widget(self.scroll)
        self.root_layout.add_widget(create_bottom_nav('beranda'))

        self.add_widget(self.root_layout)

    def load_all_menus(self):
        self.menu_container.clear_widgets()
        
        fav_title = Label(text='Menu Favorit', font_size=15, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=24, halign='left', valign='middle')
        fav_title.bind(size=fav_title.setter('text_size'))
        self.menu_container.add_widget(fav_title)

        self.fav_grid = GridLayout(cols=3, spacing=8, size_hint_y=None, height=165)
        self.cards = [
            MenuCard('gocuan.jpg', 'Mie Gocuan', 'Rp 10.000'),
            MenuCard('gambreng.jpg', 'Mie Gambreng', 'Rp 10.000'),
            MenuCard('cemen.jpg', 'Mie Cemen', 'Rp 10.000'),
            MenuCard('kopsu.jpg', 'Es Kopsu', 'Rp 7.000'),
            MenuCard('kasmaran.jpg', 'Es Kasmaran', 'Rp 7.000'),
            MenuCard('mrengut.jpg', 'Es Mrengut', 'Rp 7.000'),
            MenuCard('gocuan.jpg', 'Paket Hemat 1', 'Rp 15.000'),
            MenuCard('gambreng.jpg', 'Paket Hemat 2', 'Rp 15.000'),
            MenuCard('kopsu.jpg', 'Bundle Es', 'Rp 12.000')
        ]
        
        for card in self.cards[:3]:
            self.fav_grid.add_widget(card)
        self.menu_container.add_widget(self.fav_grid)

        drink_title = Label(text='Minuman', font_size=15, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=24, halign='left', valign='middle')
        drink_title.bind(size=drink_title.setter('text_size'))
        self.menu_container.add_widget(drink_title)

        self.drink_grid = GridLayout(cols=3, spacing=8, size_hint_y=None, height=165)
        for card in self.cards[3:6]:
            self.drink_grid.add_widget(card)
        self.menu_container.add_widget(self.drink_grid)

        promo_title = Label(text='Spesial Hari Ini', font_size=15, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=24, halign='left', valign='middle')
        promo_title.bind(size=promo_title.setter('text_size'))
        self.menu_container.add_widget(promo_title)

        self.promo_grid = GridLayout(cols=3, spacing=8, size_hint_y=None, height=165)
        for card in self.cards[6:]:
            self.promo_grid.add_widget(card)
        self.menu_container.add_widget(self.promo_grid)

    def filter_menu(self, instance, value):
        query = value.lower().strip()
        self.menu_container.clear_widgets()
        
        filtered_cards = [c for c in self.cards if query in c.title_text.lower()]
        
        if not filtered_cards:
            lbl = Label(text="Menu tidak ditemukan.", font_size=13, color=(0.7,0.7,0.7,1), size_hint_y=None, height=40, halign='center')
            lbl.bind(size=lbl.setter('text_size'))
            self.menu_container.add_widget(lbl)
            return

        result_title = Label(text=f"Hasil Pencarian ('{value}')", font_size=15, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=24, halign='left', valign='middle')
        result_title.bind(size=result_title.setter('text_size'))
        self.menu_container.add_widget(result_title)

        rows_needed = (len(filtered_cards) + 2) // 3
        grid = GridLayout(cols=3, spacing=8, size_hint_y=None, height=rows_needed * 165)
        for card in filtered_cards:
            grid.add_widget(card)
        self.menu_container.add_widget(grid)

    def open_menu_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=12, spacing=10)
        box.add_widget(Label(text="Kategori Pilihan", font_size=15, bold=True, color=(1,1,1,1), size_hint_y=None, height=28))
        
        categories = ["Semua Menu", "Makanan Berat", "Minuman", "Paket Hemat"]
        for cat in categories:
            btn = Button(text=cat, size_hint_y=None, height=38, font_size=13, background_color=(0.9, 0.1, 0.4, 1))
            btn.bind(on_press=lambda x, c=cat: self.select_category(c))
            box.add_widget(btn)
            
        self.menu_popup = Popup(title="Menu Navigasi", title_size=14, content=box, size_hint=(None, None), size=(280, 270))
        self.menu_popup.open()

    def select_category(self, cat):
        self.menu_popup.dismiss()
        self.search_input.text = ""
        if cat == "Minuman":
            self.search_input.text = "Es"
        elif cat == "Paket Hemat":
            self.search_input.text = "Paket"
        elif cat == "Makanan Berat":
            self.search_input.text = "Mie"

    def open_notif_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=12, spacing=10)
        box.add_widget(Label(text="Pemberitahuan Terbaru", font_size=15, bold=True, color=(1,1,1,1), size_hint_y=None, height=28))
        
        notif_scroll = ScrollView(size_hint=(1, 1))
        notif_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        notif_layout.bind(minimum_height=notif_layout.setter('height'))
        
        notifications = [
            "Diskon Spesial 20% hari ini untuk semua menu mie!",
            "Pesanan Mie Gocuan Anda sebelumnya telah selesai.",
            "Selamat datang di aplikasi Mie Gocuan!"
        ]
        
        for msg in notifications:
            lbl = Label(text=f"• {msg}", font_size=12, color=(0.9,0.9,0.9,1), size_hint_y=None, height=38, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            notif_layout.add_widget(lbl)
            
        notif_scroll.add_widget(notif_layout)
        box.add_widget(notif_scroll)
        
        close_btn = Button(text="Tutup", size_hint_y=None, height=38, font_size=13, background_color=(0.5, 0.5, 0.5, 1))
        self.notif_popup = Popup(title="Notifikasi", title_size=14, content=box, size_hint=(None, None), size=(300, 290))
        close_btn.bind(on_press=self.notif_popup.dismiss)
        box.add_widget(close_btn)
        
        self.notif_popup.open()

    def update_greeting(self):
        app = App.get_running_app()
        username = app.current_user.capitalize() if hasattr(app, 'current_user') else "Zidan"
        self.greeting_label.text = f"Hi, {username}\nMau makan apa hari ini?"


class PesananScreen(Screen):
    def __init__(self, **kwargs):
        super(PesananScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        content = BoxLayout(orientation='vertical', padding=12, spacing=10, size_hint=(1, 0.915), pos_hint={'top': 1})
        title = Label(text="Daftar Pesanan Saya", font_size=17, bold=True, color=(1,1,1,1), size_hint_y=None, height=32, halign='left')
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        self.scroll = ScrollView(size_hint=(1, 1))
        self.order_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.order_list_layout.bind(minimum_height=self.order_list_layout.setter('height'))
        self.scroll.add_widget(self.order_list_layout)
        content.add_widget(self.scroll)
        
        self.root_layout.add_widget(content)
        self.root_layout.add_widget(create_bottom_nav('pesanan'))
        self.add_widget(self.root_layout)

    def load_orders(self):
        self.order_list_layout.clear_widgets()
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT details, total, status FROM orders WHERE username=?", (username,))
        orders = cursor.fetchall()
        conn.close()
        
        if not orders:
            empty_lbl = Label(text="Belum ada pesanan aktif.", font_size=13, color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=40, halign='center')
            empty_lbl.bind(size=empty_lbl.setter('text_size'))
            self.order_list_layout.add_widget(empty_lbl)
            return
            
        for details, total, status in orders:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=85, padding=10, spacing=6)
            with box.canvas.before:
                Color(0.18, 0.18, 0.18, 1)
                self.rect = RoundedRectangle(size=box.size, pos=box.pos, radius=[6])
            box.bind(size=self._update_box_rect, pos=self._update_box_rect)
            
            lbl_det = Label(text=details, font_size=12, color=(1,1,1,1), halign='left', valign='middle')
            lbl_det.bind(size=lbl_det.setter('text_size'))
            
            lbl_tot = Label(text=f"Total: {total} | Status: {status}", font_size=12, bold=True, color=(0.9, 0.3, 0.5, 1), halign='left', valign='middle')
            lbl_tot.bind(size=lbl_tot.setter('text_size'))
            
            box.add_widget(lbl_det)
            box.add_widget(lbl_tot)
            self.order_list_layout.add_widget(box)

    def _update_box_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.18, 0.18, 0.18, 1)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[6])


class KeranjangScreen(Screen):
    def __init__(self, **kwargs):
        super(KeranjangScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        content = BoxLayout(orientation='vertical', padding=12, spacing=10, size_hint=(1, 0.915), pos_hint={'top': 1})
        title = Label(text="Keranjang Belanja", font_size=17, bold=True, color=(1,1,1,1), size_hint_y=None, height=32, halign='left')
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        self.scroll = ScrollView(size_hint=(1, 0.74))
        self.cart_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.cart_list_layout.bind(minimum_height=self.cart_list_layout.setter('height'))
        self.scroll.add_widget(self.cart_list_layout)
        content.add_widget(self.scroll)
        
        checkout_box = BoxLayout(orientation='vertical', size_hint_y=None, height=75, spacing=6)
        self.total_label = Label(text="Total Pembayaran: Rp 0", font_size=14, bold=True, color=(1,1,1,1), halign='left', size_hint_y=None, height=24)
        self.total_label.bind(size=self.total_label.setter('text_size'))
        checkout_box.add_widget(self.total_label)
        
        checkout_btn = Button(text='CHECKOUT SEKARANG', font_size=13, bold=True, size_hint=(1, None), height=40, background_color=(0.9, 0.1, 0.4, 1))
        checkout_btn.bind(on_press=self.checkout)
        checkout_box.add_widget(checkout_btn)
        
        content.add_widget(checkout_box)
        
        self.root_layout.add_widget(content)
        self.root_layout.add_widget(create_bottom_nav('keranjang'))
        self.add_widget(self.root_layout)

    def load_cart(self):
        self.cart_list_layout.clear_widgets()
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, price, quantity FROM cart WHERE username=?", (username,))
        items = cursor.fetchall()
        conn.close()
        
        total_price = 0
        
        if not items:
            empty_lbl = Label(text="Keranjang masih kosong.", font_size=13, color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=40, halign='center')
            empty_lbl.bind(size=empty_lbl.setter('text_size'))
            self.cart_list_layout.add_widget(empty_lbl)
            self.total_label.text = "Total Pembayaran: Rp 0"
            return
            
        for item_id, name, price_str, qty in items:
            clean_val = int(price_str.replace("Rp", "").replace(".", "").strip())
            total_price += clean_val * qty
            
            row = BoxLayout(size_hint_y=None, height=44, spacing=8)
            lbl = Label(text=f"{name} (x{qty})", font_size=12, color=(1,1,1,1), halign='left', valign='middle', size_hint_x=0.58)
            lbl.bind(size=lbl.setter('text_size'))
            
            prc = Label(text=f"Rp {clean_val * qty:,}".replace(",", "."), font_size=12, color=(0.85,0.85,0.85,1), halign='right', valign='middle', size_hint_x=0.27)
            prc.bind(size=prc.setter('text_size'))
            
            del_btn = Button(text='X', font_size=11, size_hint_x=0.15, background_color=(0.6, 0.1, 0.1, 1))
            del_btn.bind(on_press=lambda x, i_id=item_id: self.remove_item(i_id))
            
            row.add_widget(lbl)
            row.add_widget(prc)
            row.add_widget(del_btn)
            self.cart_list_layout.add_widget(row)
            
        self.total_label.text = f"Total Pembayaran: Rp {total_price:,}".replace(",", ".")

    def remove_item(self, item_id):
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        self.load_cart()

    def checkout(self, instance):
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, price, quantity FROM cart WHERE username=?", (username,))
        items = cursor.fetchall()
        
        if not items:
            conn.close()
            return
            
        details_list = []
        total_price = 0
        for name, price_str, qty in items:
            details_list.append(f"{name} x{qty}")
            clean_val = int(price_str.replace("Rp", "").replace(".", "").strip())
            total_price += clean_val * qty
            
        details_str = ", ".join(details_list)
        total_str = f"Rp {total_price:,}".replace(",", ".")
        
        cursor.execute("INSERT INTO orders (username, details, total, status) VALUES (?, ?, ?, ?)", (username, details_str, total_str, "Diproses"))
        cursor.execute("DELETE FROM cart WHERE username=?", (username,))
        conn.commit()
        conn.close()
        
        self.load_cart()
        app.root.get_screen('pesanan').load_orders()
        app.root.current = 'pesanan'


class ProfilScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfilScreen, self).__init__(**kwargs)
        root_layout = FloatLayout()
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=14, size_hint=(1, 0.915), pos_hint={'top': 1})
        content.add_widget(Label(text="Profil Pengguna", font_size=19, bold=True, color=(1,1,1,1), size_hint_y=None, height=32))
        
        self.info_label = Label(text="Nama: Zidan\nStatus: Member", font_size=13, color=(0.85,0.85,0.85,1), size_hint_y=None, height=50)
        content.add_widgets = content.add_widget(self.info_label)
        
        logout_btn = Button(text='Keluar / Logout', size_hint=(1, None), height=40, font_size=13, background_color=(0.5, 0.1, 0.2, 1))
        logout_btn.bind(on_press=self.to_login)
        content.add_widget(logout_btn)
        
        root_layout.add_widget(content)
        root_layout.add_widget(create_bottom_nav('profil'))
        self.add_widget(root_layout)

    def load_profile(self):
        app = App.get_running_app()
        uname = getattr(app, 'current_user', 'Zidan')
        self.info_label.text = f"Nama: {uname.capitalize()}\nStatus: Member"

    def to_login(self, instance):
        self.manager.current = 'login'


class MieGocuanApp(App):
    current_user = 'zidan'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(BerandaScreen(name='beranda'))
        sm.add_widget(PesananScreen(name='pesanan'))
        sm.add_widget(KeranjangScreen(name='keranjang'))
        sm.add_widget(ProfilScreen(name='profil'))
        return sm

if __name__ == '__main__':
    MieGocuanApp().run()