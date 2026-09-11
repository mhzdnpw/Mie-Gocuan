import sqlite3
from datetime import datetime
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
from kivy.clock import Clock

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
            payment_method TEXT,
            timestamp TEXT,
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
    
    migrations = [
        ("payment_method", "TEXT"),
        ("timestamp", "TEXT")
    ]
    for col_name, col_type in migrations:
        try:
            cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass

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
    def __init__(self, img_src, title_text, price_text, description_text="", **kwargs):
        super(MenuCard, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 165
        
        self.img_src = img_src
        self.title_text = title_text
        self.price_text = price_text
        self.description_text = description_text or "Menu istimewa pilihan terbaik dari Mie Gocuan."

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
        self.btn.bind(on_press=self.open_detail_popup)
        self.add_widget(self.btn)

    def _update_canvas(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_detail_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=12, spacing=8)
        
        img = Image(source=self.img_src, size_hint=(1, 0.38))
        box.add_widget(img)
        
        lbl_name = Label(text=f"[b]{self.title_text}[/b]", markup=True, font_size=14, color=(1,1,1,1), size_hint_y=None, height=20, halign='center')
        lbl_name.bind(size=lbl_name.setter('text_size'))
        box.add_widget(lbl_name)
        
        lbl_price = Label(text=self.price_text, font_size=12, color=(0.9, 0.3, 0.5, 1), bold=True, size_hint_y=None, height=18, halign='center')
        lbl_price.bind(size=lbl_price.setter('text_size'))
        box.add_widget(lbl_price)
        
        desc_scroll = ScrollView(size_hint=(1, None), height=75)
        lbl_desc = Label(text=self.description_text, font_size=11, color=(0.85, 0.85, 0.85, 1), size_hint_y=None, halign='center', valign='top')
        lbl_desc.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        lbl_desc.bind(texture_size=lambda s, t: setattr(s, 'height', t[1]))
        desc_scroll.add_widget(lbl_desc)
        box.add_widget(desc_scroll)

        action_layout = BoxLayout(size_hint_y=None, height=36, spacing=8)
        
        self.qty_value = 1
        self.qty_label = Label(text=str(self.qty_value), font_size=13, bold=True, color=(1,1,1,1), size_hint_x=0.3)
        
        btn_min = Button(text='-', font_size=13, bold=True, size_hint_x=0.25, background_color=(0.3, 0.3, 0.3, 1))
        btn_plus = Button(text='+', font_size=13, bold=True, size_hint_x=0.25, background_color=(0.3, 0.3, 0.3, 1))
        
        btn_min.bind(on_press=lambda x: self.change_qty(-1))
        btn_plus.bind(on_press=lambda x: self.change_qty(1))
        
        action_layout.add_widget(btn_min)
        action_layout.add_widget(self.qty_label)
        action_layout.add_widget(btn_plus)
        box.add_widget(action_layout)

        add_cart_btn = Button(
            text="Tambah ke Keranjang",
            font_size=12,
            bold=True,
            size_hint=(1, None),
            height=38,
            background_color=(0.9, 0.1, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        
        self.popup = Popup(
            title="Detail Menu",
            title_size=13,
            title_align='center',
            content=box,
            size_hint=(None, None),
            size=(300, 390),
            auto_dismiss=True
        )
        
        add_cart_btn.bind(on_press=lambda x: self.confirm_add_to_cart())
        box.add_widget(add_cart_btn)
        
        self.popup.open()

    def change_qty(self, delta):
        if self.qty_value + delta >= 1:
            self.qty_value += delta
            self.qty_label.text = str(self.qty_value)

    def confirm_add_to_cart(self):
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, quantity FROM cart WHERE username=? AND item_name=?", (username, self.title_text))
        existing = cursor.fetchone()
        
        if existing:
            new_qty = existing[1] + self.qty_value
            cursor.execute("UPDATE cart SET quantity=? WHERE id=?", (new_qty, existing[0]))
        else:
            cursor.execute("INSERT INTO cart (username, item_name, price, quantity) VALUES (?, ?, ?, ?)", (username, self.title_text, self.price_text, self.qty_value))
            
        conn.commit()
        conn.close()
        app.root.get_screen('keranjang').load_cart()
        self.popup.dismiss()
        
        box = BoxLayout(orientation='vertical', padding=15, spacing=12)
        msg_label = Label(
            text=f"Berhasil menambahkan [b]{self.qty_value}x {self.title_text}[/b] ke keranjang!",
            markup=True,
            font_size=12,
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
            height=38,
            background_color=(0.9, 0.1, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        box.add_widget(ok_btn)
        
        success_popup = Popup(
            title="Berhasil",
            title_size=14,
            title_align='center',
            content=box,
            size_hint=(None, None),
            size=(270, 150),
            auto_dismiss=True
        )
        ok_btn.bind(on_press=success_popup.dismiss)
        success_popup.open()


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
        
        logo_img = Image(source='logo gocuan.png', size_hint=(None, None), size=(34, 34), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        notif_btn = Button(text='Info', size_hint=(None, None), size=(45, 32), pos_hint={'left': 0, 'center_y': 0.5}, background_color=(0,0,0,0), font_size=13, color=(1,1,1,1), bold=True)
        notif_btn.bind(on_press=self.open_notif_popup)
        
        header_layout.add_widget(notif_btn)
        header_layout.add_widget(logo_img)
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
            MenuCard('gocuan.jpg', 'Mie Gocuan', 'Rp 10.000', 'Menu legendaris! Mie kenyal berpadu sempurna dengan bumbu kecap manis gurih dan sensasi pedas yang bikin nagih. Lengkap dengan taburan ayam cincang dan 2 pcs pangsit goreng renyah. Tersedia level 1-8.'),
            MenuCard('gambreng.jpg', 'Mie Gambreng', 'Rp 10.000', 'Kombinasi sempurna mie kenyal dengan bumbu asin gurih yang pedasnya nendang. Dilengkapi taburan ayam cincang halus dan 2 pcs pangsit goreng crispy. Pilih level pedasmu (1-8) dan rasakan tantangannya!'),
            MenuCard('cemen.jpg', 'Mie Cemen', 'Rp 10.000', 'Mie kenyal dengan bumbu racikan gurih alami yang ramah di lidah. Sama sekali tidak pedas, disajikan dengan taburan ayam cincang melimpah dan 2 pcs pangsit goreng renyah. Cocok untuk semua usia!'),
            MenuCard('kopsu.jpg', 'Es Kopsu', 'Rp 7.000', 'Kombinasi sempurna untuk pencinta kopi! Perpaduan espresso yang mantap, susu yang gurih, dan manisnya gula aren alami. Rasa creamy dan bold-nya tidak hanya bikin melek, tapi juga pas banget jadi penyeimbang rasa mie pedas favoritmu!'),
            MenuCard('kasmaran.jpg', 'Es Kasmaran', 'Rp 7.000', 'Peredam pedas paling ampuh! Perpaduan mewah antara susu yang lembut, sirup manis, jeli kenyal, dan kombinasi potongan buah segar. Rasanya manis, dingin, dan buahnya melimpah, siap mengembalikan kesegaran lidahmu setelah makan pedas!'),
            MenuCard('mrengut.jpg', 'Es Mrengut', 'Rp 7.000', 'Sensasi kesegaran yang bikin mata melek! Kombinasi rasa asam segar jeruk nipis/lemon premium dengan tambahan jeli kenyal. Cocok banget untuk kamu yang butuh kesegaran instan pendamping mie pedas.'),
            MenuCard('gocuan.jpg', 'Paket Hemat 1', 'Rp 15.000', 'Paket hemat nikmat berisi 1 porsi legendaris Mie Gocuan (pilih level 1-8) dipadukan dengan kesegaran Es Kopsu yang creamy dan manis. Solusi pas kenyang dan puas dalam satu paket!'),
            MenuCard('gambreng.jpg', 'Paket Hemat 2', 'Rp 15.000', 'Paket spesial tantangan pedas! Berisi 1 porsi Mie Gambreng favoritmu dengan bumbu asin gurih pedas nendang, lengkap ditemani kesegaran Es Kasmaran manis berlimpah buah.'),
            MenuCard('kopsu.jpg', 'Bundle Es', 'Rp 12.000', 'Bundel hemat dua varian minuman menyegarkan (Es Kasmaran & Es Mrengut) untuk menetralkan lidah dan menemani waktu santai bersama teman-teman.')
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


class NotaScreen(Screen):
    def __init__(self, **kwargs):
        super(NotaScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        with self.root_layout.canvas.before:
            Color(0.12, 0.12, 0.14, 1)
            self.bg_rect = RoundedRectangle(size=Window.size)
        self.root_layout.bind(size=lambda i, v: setattr(self.bg_rect, 'size', v))

        main_box = BoxLayout(orientation='vertical', padding=[16, 14, 16, 14], spacing=6, size_hint=(0.88, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        with main_box.canvas.before:
            Color(0.16, 0.16, 0.19, 1)
            self.card_rect = RoundedRectangle(size=main_box.size, pos=main_box.pos, radius=[14])
        main_box.bind(size=self._update_card, pos=self._update_card)

        main_box.add_widget(Label(text="[b]MIE GOCUAN OFFICIAL[/b]", markup=True, font_size=15, color=(1,1,1,1), size_hint_y=None, height=20, halign='center'))
        main_box.add_widget(Label(text="Jl. Veteran No. 09, Mojoroto, Kota Kediri", font_size=10, color=(0.75,0.75,0.75,1), size_hint_y=None, height=14, halign='center'))
        
        separator1 = Label(text="----------------------------------------------------------------", font_size=9, color=(0.4,0.4,0.4,1), size_hint_y=None, height=10, halign='center')
        separator1.bind(size=separator1.setter('text_size'))
        main_box.add_widget(separator1)

        info_grid = GridLayout(cols=2, size_hint_y=None, height=58, spacing=[4, 2])
        
        self.lbl_trans_id_key = Label(text="No. Transaksi", font_size=11, color=(0.75,0.75,0.75,1), halign='left', valign='middle')
        self.lbl_trans_id_key.bind(size=self.lbl_trans_id_key.setter('text_size'))
        self.lbl_trans_id_val = Label(text="#GOCUAN-0002", font_size=11, bold=True, color=(1,1,1,1), halign='right', valign='middle')
        self.lbl_trans_id_val.bind(size=self.lbl_trans_id_val.setter('text_size'))
        
        self.lbl_time_key = Label(text="Waktu / Tanggal", font_size=11, color=(0.75,0.75,0.75,1), halign='left', valign='middle')
        self.lbl_time_key.bind(size=self.lbl_time_key.setter('text_size'))
        self.lbl_time_val = Label(text="-", font_size=11, color=(1,1,1,1), halign='right', valign='middle')
        self.lbl_time_val.bind(size=self.lbl_time_val.setter('text_size'))

        self.lbl_method_key = Label(text="Metode Bayar", font_size=11, color=(0.75,0.75,0.75,1), halign='left', valign='middle')
        self.lbl_method_key.bind(size=self.lbl_method_key.setter('text_size'))
        self.lbl_method_val = Label(text="Tunai", font_size=11, color=(1,1,1,1), halign='right', valign='middle')
        self.lbl_method_val.bind(size=self.lbl_method_val.setter('text_size'))

        info_grid.add_widget(self.lbl_trans_id_key)
        info_grid.add_widget(self.lbl_trans_id_val)
        info_grid.add_widget(self.lbl_time_key)
        info_grid.add_widget(self.lbl_time_val)
        info_grid.add_widget(self.lbl_method_key)
        info_grid.add_widget(self.lbl_method_val)
        
        main_box.add_widget(info_grid)

        separator2 = Label(text="----------------------------------------------------------------", font_size=9, color=(0.4,0.4,0.4,1), size_hint_y=None, height=10, halign='center')
        separator2.bind(size=separator2.setter('text_size'))
        main_box.add_widget(separator2)

        lbl_rincian_title = Label(text="[b]Rincian Pesanan:[/b]", markup=True, font_size=11, color=(0.9,0.9,0.9,1), size_hint_y=None, height=16, halign='left')
        lbl_rincian_title.bind(size=lbl_rincian_title.setter('text_size'))
        main_box.add_widget(lbl_rincian_title)

        details_scroll = ScrollView(size_hint=(1, None), height=65)
        self.lbl_details = Label(text="-", font_size=11, color=(1,1,1,1), size_hint_y=None, halign='left', valign='top')
        self.lbl_details.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        self.lbl_details.bind(texture_size=lambda s, t: setattr(s, 'height', t[1]))
        details_scroll.add_widget(self.lbl_details)
        main_box.add_widget(details_scroll)

        separator3 = Label(text="----------------------------------------------------------------", font_size=9, color=(0.4,0.4,0.4,1), size_hint_y=None, height=10, halign='center')
        separator3.bind(size=separator3.setter('text_size'))
        main_box.add_widget(separator3)

        bottom_grid = GridLayout(cols=2, size_hint_y=None, height=22, spacing=[4, 2])
        
        lbl_tot_title = Label(text="TOTAL", font_size=12, bold=True, color=(1,1,1,1), halign='left', valign='middle')
        lbl_tot_title.bind(size=lbl_tot_title.setter('text_size'))
        
        self.lbl_total = Label(text="Rp 0", font_size=13, bold=True, color=(0.9, 0.1, 0.4, 1), halign='right', valign='middle')
        self.lbl_total.bind(size=self.lbl_total.setter('text_size'))

        bottom_grid.add_widget(lbl_tot_title)
        bottom_grid.add_widget(self.lbl_total)
        main_box.add_widget(bottom_grid)

        self.lbl_status = Label(text="STATUS: LUNAS / SUDAH DIBAYAR", font_size=10, bold=True, color=(0.3, 1, 0.4, 1), size_hint_y=None, height=18, halign='center')
        self.lbl_status.bind(size=self.lbl_status.setter('text_size'))
        main_box.add_widget(self.lbl_status)

        main_box.add_widget(Label(size_hint_y=None, height=4))

        back_btn = Button(
            text="Kembali ke Daftar Pesanan",
            font_size=11,
            bold=True,
            size_hint=(1, None),
            height=36,
            background_color=(0.9, 0.1, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'pesanan'))
        main_box.add_widget(back_btn)

        main_box.height = 370
        
        self.root_layout.add_widget(main_box)
        self.add_widget(self.root_layout)

    def _update_card(self, instance, value):
        self.card_rect.pos = instance.pos
        self.card_rect.size = instance.size

    def set_nota_data(self, order_id, details, total, pay_method, timestamp):
        self.lbl_trans_id_val.text = f"#GOCUAN-{order_id:04d}"
        self.lbl_time_val.text = f"{timestamp or datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        self.lbl_method_val.text = f"{pay_method or 'Tunai'}"
        
        formatted_items = "\n".join([f"• {item.strip()}" for item in details.split(",")])
        self.lbl_details.text = formatted_items
        self.lbl_total.text = f"{total}"


class PesananScreen(Screen):
    def __init__(self, **kwargs):
        super(PesananScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        content = BoxLayout(orientation='vertical', padding=[16, 20, 16, 16], spacing=16, size_hint=(1, 0.915), pos_hint={'top': 1})
        
        title = Label(
            text="Daftar Pesanan Saya", 
            font_size=18, 
            bold=True, 
            color=(1, 1, 1, 1), 
            size_hint_y=None, 
            height=32, 
            halign='left', 
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.order_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12)
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
        cursor.execute("SELECT id, details, total, payment_method, timestamp, status FROM orders WHERE username=?", (username,))
        orders = cursor.fetchall()
        conn.close()
        
        if not orders:
            empty_lbl = Label(
                text="Belum ada pesanan aktif.", 
                font_size=13, 
                color=(0.65, 0.65, 0.65, 1), 
                size_hint_y=None, 
                height=60, 
                halign='center', 
                valign='middle'
            )
            empty_lbl.bind(size=empty_lbl.setter('text_size'))
            self.order_list_layout.add_widget(empty_lbl)
            return
            
        for order_id, details, total, pay_method, timestamp, status in orders:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=130, padding=12, spacing=6)
            
            with card.canvas.before:
                Color(0.15, 0.15, 0.17, 1)
                self.rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[12])
            card.bind(size=self._update_box_rect, pos=self._update_box_rect)
            
            top_row = BoxLayout(size_hint_y=None, height=22)
            lbl_det = Label(
                text=details, 
                font_size=12, 
                bold=True, 
                color=(0.95, 0.95, 0.95, 1), 
                halign='left', 
                valign='middle'
            )
            lbl_det.bind(size=lbl_det.setter('text_size'))
            
            status_color = (1, 0.75, 0.2, 1) if status.lower() == 'diproses' else (0.3, 1, 0.4, 1)
            lbl_status = Label(
                text=status, 
                font_size=11, 
                bold=True, 
                color=status_color, 
                halign='right', 
                valign='middle'
            )
            lbl_status.bind(size=lbl_status.setter('text_size'))
            
            top_row.add_widget(lbl_det)
            top_row.add_widget(lbl_status)
            
            info_row = BoxLayout(size_hint_y=None, height=20)
            lbl_time = Label(text=f"Waktu: {timestamp or 'Baru saja'}", font_size=10, color=(0.6, 0.6, 0.65, 1), halign='left', valign='middle')
            lbl_time.bind(size=lbl_time.setter('text_size'))
            lbl_pay = Label(text=f"Metode: {pay_method or 'Tunai'}", font_size=10, color=(0.6, 0.6, 0.65, 1), halign='right', valign='middle')
            lbl_pay.bind(size=lbl_pay.setter('text_size'))
            info_row.add_widget(lbl_time)
            info_row.add_widget(lbl_pay)
            
            separator = BoxLayout(size_hint_y=None, height=1)
            with separator.canvas.before:
                Color(0.25, 0.25, 0.28, 1)
                sep_rect = RoundedRectangle(size=separator.size, pos=separator.pos)
            separator.bind(
                size=lambda i, v: setattr(sep_rect, 'size', v),
                pos=lambda i, v: setattr(sep_rect, 'pos', v)
            )

            bottom_row = BoxLayout(size_hint_y=None, height=24)
            lbl_total_title = Label(
                text="Total Pembayaran", 
                font_size=11, 
                color=(0.6, 0.6, 0.65, 1), 
                halign='left', 
                valign='middle'
            )
            lbl_total_title.bind(size=lbl_total_title.setter('text_size'))
            
            lbl_tot = Label(
                text=total, 
                font_size=13, 
                bold=True, 
                color=(0.9, 0.1, 0.4, 1), 
                halign='right', 
                valign='middle'
            )
            lbl_tot.bind(size=lbl_tot.setter('text_size'))
            
            bottom_row.add_widget(lbl_total_title)
            bottom_row.add_widget(lbl_tot)
            
            btn_nota = Button(text="Lihat Nota Transaksi", font_size=11, bold=True, size_hint_y=None, height=26, background_color=(0.2, 0.5, 0.8, 1), color=(1,1,1,1))
            btn_nota.bind(on_press=lambda x, o_id=order_id, dt=details, tot=total, pm=pay_method, ts=timestamp: self.open_nota_page(o_id, dt, tot, pm, ts))

            card.add_widget(top_row)
            card.add_widget(info_row)
            card.add_widget(separator)
            card.add_widget(bottom_row)
            card.add_widget(btn_nota)
            
            self.order_list_layout.add_widget(card)

    def open_nota_page(self, order_id, details, total, pay_method, timestamp):
        app = App.get_running_app()
        nota_screen = app.root.get_screen('nota')
        nota_screen.set_nota_data(order_id, details, total, pay_method, timestamp)
        app.root.current = 'nota'

    def _update_box_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.15, 0.17, 1)
            RoundedRectangle(size=instance.size, pos=instance.pos, radius=[12])


class KeranjangScreen(Screen):
    def __init__(self, **kwargs):
        super(KeranjangScreen, self).__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        content = BoxLayout(orientation='vertical', padding=12, spacing=10, size_hint=(1, 0.915), pos_hint={'top': 1})
        title = Label(text="Keranjang & Pembayaran", font_size=17, bold=True, color=(1,1,1,1), size_hint_y=None, height=32, halign='left')
        title.bind(size=title.setter('text_size'))
        content.add_widget(title)
        
        self.scroll = ScrollView(size_hint=(1, 0.60))
        self.cart_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.cart_list_layout.bind(minimum_height=self.cart_list_layout.setter('height'))
        self.scroll.add_widget(self.cart_list_layout)
        content.add_widget(self.scroll)
        
        payment_box = BoxLayout(orientation='vertical', size_hint_y=None, height=130, spacing=6)
        
        self.total_label = Label(text="Total Pembayaran: Rp 0", font_size=13, bold=True, color=(1,1,1,1), halign='left', size_hint_y=None, height=22)
        self.total_label.bind(size=self.total_label.setter('text_size'))
        payment_box.add_widget(self.total_label)
        
        payment_method_label = Label(text="Pilih Metode Pembayaran:", font_size=11, color=(0.8,0.8,0.8,1), halign='left', size_hint_y=None, height=18)
        payment_method_label.bind(size=payment_method_label.setter('text_size'))
        payment_box.add_widget(payment_method_label)
        
        btn_layout = BoxLayout(size_hint_y=None, height=38, spacing=8)
        self.btn_tunai = Button(text="Tunai (Cash)", font_size=12, bold=True, background_color=(0.9, 0.1, 0.4, 1))
        self.btn_qris = Button(text="QRIS", font_size=12, bold=True, background_color=(0.3, 0.3, 0.3, 1))
        
        self.btn_tunai.bind(on_press=lambda x: self.set_payment_method("Tunai"))
        self.btn_qris.bind(on_press=lambda x: self.set_payment_method("QRIS"))
        
        btn_layout.add_widget(self.btn_tunai)
        btn_layout.add_widget(self.btn_qris)
        payment_box.add_widget(btn_layout)
        
        self.selected_method = "Tunai"
        
        checkout_btn = Button(text='PROSES PEMBAYARAN', font_size=12, bold=True, size_hint=(1, None), height=38, background_color=(0.1, 0.7, 0.4, 1))
        checkout_btn.bind(on_press=self.checkout)
        payment_box.add_widget(checkout_btn)
        
        content.add_widget(payment_box)
        
        self.root_layout.add_widget(content)
        self.root_layout.add_widget(create_bottom_nav('keranjang'))
        self.add_widget(self.root_layout)

    def set_payment_method(self, method):
        self.selected_method = method
        if method == "Tunai":
            self.btn_tunai.background_color = (0.9, 0.1, 0.4, 1)
            self.btn_qris.background_color = (0.3, 0.3, 0.3, 1)
        else:
            self.btn_qris.background_color = (0.9, 0.1, 0.4, 1)
            self.btn_tunai.background_color = (0.3, 0.3, 0.3, 1)

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
        conn.close()
        
        if not items:
            return
            
        total_price = 0
        details_list = []
        for name, price_str, qty in items:
            details_list.append(f"{name} x{qty}")
            clean_val = int(price_str.replace("Rp", "").replace(".", "").strip())
            total_price += clean_val * qty
            
        total_str_clean = f"Rp {total_price:,}".replace(",", ".")

        box = BoxLayout(orientation='vertical', padding=15, spacing=10)
        box.add_widget(Label(text="[b]Konfirmasi Pembayaran[/b]", markup=True, font_size=15, color=(1,1,1,1), size_hint_y=None, height=26, halign='center'))
        box.add_widget(Label(text=f"Metode: [b]{self.selected_method}[/b]\nTotal: [b]Rp {total_price:,}".replace(",", ".") + "[/b]", markup=True, font_size=13, color=(0.9,0.9,0.9,1), size_hint_y=None, height=45, halign='center'))

        if self.selected_method == "QRIS":
            box.add_widget(Label(text="Silakan scan QRIS di bawah ini:", font_size=11, color=(0.8,0.8,0.8,1), size_hint_y=None, height=20, halign='center'))
            box.add_widget(Image(source='logo gocuan.png', size_hint=(1, None), height=110))
            box.add_widget(Label(text="[color=#00FF66]Status: Menunggu Scan QRIS...[/color]", markup=True, font_size=12, size_hint_y=None, height=22, halign='center'))
        else:
            box.add_widget(Label(text="----------------------------------------------------------------", font_size=10, color=(0.5,0.5,0.5,1), size_hint_y=None, height=12, halign='center'))
            box.add_widget(Label(text="[color=#FFD700]Silakan lakukan pembayaran Tunai\nke kasir/pelayan toko kami.[/color]", markup=True, font_size=12, size_hint_y=None, height=45, halign='center'))

        btn_layout = BoxLayout(size_hint_y=None, height=38, spacing=8)
        btn_batal = Button(text="Batal", font_size=12, background_color=(0.5, 0.5, 0.5, 1))
        btn_konfirmasi = Button(text="Konfirmasi & Bayar", font_size=12, bold=True, background_color=(0.1, 0.7, 0.4, 1))

        self.confirm_popup = Popup(
            title="Konfirmasi Pesanan", 
            title_size=13, 
            content=box, 
            size_hint=(None, None), 
            size=(310, 360) if self.selected_method == "QRIS" else (310, 270)
        )

        btn_batal.bind(on_press=self.confirm_popup.dismiss)
        btn_konfirmasi.bind(on_press=lambda x: self.execute_final_checkout(details_list, total_str_clean, self.selected_method))

        btn_layout.add_widget(btn_batal)
        btn_layout.add_widget(btn_konfirmasi)
        box.add_widget(btn_layout)

        self.confirm_popup.open()

    def execute_final_checkout(self, details_list, total_str, payment_method):
        app = App.get_running_app()
        username = getattr(app, 'current_user', 'zidan')
        
        details_str = ", ".join(details_list)
        timestamp_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (username, details, total, payment_method, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)", 
                       (username, details_str, total_str, payment_method, timestamp_str, "Diproses"))
        cursor.execute("DELETE FROM cart WHERE username=?", (username,))
        conn.commit()
        conn.close()

        self.confirm_popup.dismiss()
        self.load_cart()
        app.root.get_screen('pesanan').load_orders()
        app.root.current = 'pesanan'


class ProfilScreen(Screen):
    name = 'profil'

    def __init__(self, **kwargs):
        super(ProfilScreen, self).__init__(**kwargs)
        root_layout = FloatLayout()
        
        with root_layout.canvas.before:
            Color(0.12, 0.12, 0.14, 1)
            self.bg_rect = RoundedRectangle(size=Window.size)
        root_layout.bind(size=lambda i, v: setattr(self.bg_rect, 'size', v))

        main_box = BoxLayout(
            orientation='vertical', 
            padding=[20, 24, 20, 20], 
            spacing=16, 
            size_hint=(0.88, None), 
            height=430,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        with main_box.canvas.before:
            Color(0.16, 0.16, 0.19, 1)
            self.card_rect = RoundedRectangle(size=main_box.size, pos=main_box.pos, radius=[16])
        main_box.bind(size=self._update_card, pos=self._update_card)

        title = Label(
            text="[b]Profil Pengguna[/b]", 
            markup=True, 
            font_size=18, 
            bold=True, 
            color=(1, 1, 1, 1), 
            size_hint_y=None, 
            height=28, 
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        main_box.add_widget(title)

        avatar_layout = FloatLayout(size_hint=(None, None), size=(75, 75), pos_hint={'center_x': 0.5})
        with avatar_layout.canvas.before:
            Color(0.9, 0.1, 0.4, 1)
            self.avatar_bg = RoundedRectangle(size=(75, 75), radius=[37.5])
        
        self.avatar_label = Label(
            text="Z", 
            font_size=28, 
            bold=True, 
            color=(1, 1, 1, 1), 
            size_hint=(1, 1), 
            halign='center', 
            valign='middle'
        )
        self.avatar_label.bind(size=self.avatar_label.setter('text_size'))
        avatar_layout.add_widget(self.avatar_label)
        main_box.add_widget(avatar_layout)

        main_box.add_widget(Label(size_hint_y=None, height=4))

        info_card = BoxLayout(orientation='vertical', padding=12, spacing=8, size_hint=(1, None), height=110)
        with info_card.canvas.before:
            Color(0.13, 0.13, 0.15, 1)
            self.info_bg = RoundedRectangle(size=info_card.size, pos=info_card.pos, radius=[10])
        info_card.bind(size=lambda i, v: setattr(self.info_bg, 'size', v), pos=lambda i, v: setattr(self.info_bg, 'pos', v))

        self.lbl_username = Label(
            text="Username: -", 
            font_size=13, 
            color=(0.9, 0.9, 0.9, 1), 
            halign='left', 
            valign='middle', 
            size_hint_y=None, 
            height=24
        )
        self.lbl_username.bind(size=self.lbl_username.setter('text_size'))

        self.lbl_status = Label(
            text="Status Akun: Member Resmi Gocuan", 
            font_size=13, 
            color=(0.3, 1, 0.4, 1), 
            bold=True, 
            halign='left', 
            valign='middle', 
            size_hint_y=None, 
            height=24
        )
        self.lbl_status.bind(size=self.lbl_status.setter('text_size'))

        self.lbl_store = Label(
            text="Lokasi: Outlet Resmi Kediri", 
            font_size=12, 
            color=(0.7, 0.7, 0.75, 1), 
            halign='left', 
            valign='middle', 
            size_hint_y=None, 
            height=22
        )
        self.lbl_store.bind(size=self.lbl_store.setter('text_size'))

        info_card.add_widget(self.lbl_username)
        info_card.add_widget(self.lbl_status)
        info_card.add_widget(self.lbl_store)
        main_box.add_widget(info_card)

        main_box.add_widget(Label(size_hint_y=None, height=6))

        logout_btn = Button(
            text='Keluar / Logout Akun', 
            size_hint=(1, None), 
            height=42, 
            font_size=13, 
            bold=True, 
            background_color=(0.85, 0.15, 0.25, 1), 
            color=(1, 1, 1, 1)
        )
        logout_btn.bind(on_press=self.to_login)
        main_box.add_widget(logout_btn)

        root_layout.add_widget(main_box)
        root_layout.add_widget(create_bottom_nav('profil'))
        self.add_widget(root_layout)

    def _update_card(self, instance, value):
        self.card_rect.pos = instance.pos
        self.card_rect.size = instance.size

    def load_profile(self):
        app = App.get_running_app()
        uname = getattr(app, 'current_user', 'Zidan')
        self.lbl_username.text = f"Username : {uname.capitalize()}"
        self.avatar_label.text = uname[0].upper() if uname else "Z"

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
        sm.add_widget(NotaScreen(name='nota'))
        sm.add_widget(ProfilScreen(name='profil'))
        
        Clock.schedule_interval(self.update_orders_status, 30)
        
        return sm

    def update_orders_status(self, dt):
        conn = sqlite3.connect('gocuan.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status='Selesai' WHERE status='Diproses'")
        conn.commit()
        conn.close()
        
        try:
            self.root.get_screen('pesanan').load_orders()
        except Exception:
            pass

if __name__ == '__main__':
    MieGocuanApp().run()