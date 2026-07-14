import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.graphics import Rotate, PushMatrix, PopMatrix
from plyer import accelerometer
# --- MÜLKİYET: TUNCAY KARACA ---
# Bu yazılım, Arvexa Emlak faaliyetlerinde kullanılmak üzere
# Tuncay Karaca tarafından özel olarak geliştirilmiştir.
# İzinsiz kopyalanamaz ve paylaşılamaz.
# --------------------------------

# ALGAN PROTOKOLÜ: MUTLAK YOL VE DOKU
YOL = "."
ALTIN_RENK = [1, 0.84, 0, 1]


class ImageButton(ButtonBehavior, Image):
    pass


class RotatableImage(Image):
    def __init__(self, **kwargs):
        super(RotatableImage, self).__init__(**kwargs)
        self.angle = 0
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=self.angle, axis=(0, 0, 1))
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self.update_rotation_origin, size=self.update_rotation_origin)

    def update_rotation_origin(self, *args):
        self.rot.origin = (int(self.x + self.width / 2.0), int(self.y + self.height / 2.0))

    def set_angle(self, angle):
        self.angle = angle
        self.rot.angle = self.angle


class ArvexaPusula(FloatLayout):
    def __init__(self, **kwargs):
        super(ArvexaPusula, self).__init__(**kwargs)

        try:
            accelerometer.enable()
        except:
            pass

        self.aci = 0

        # --- 1. ARKA PLAN VE ÜST LOGO ---
        self.add_widget(Image(source=os.path.join(YOL, 'background.png'), allow_stretch=True, keep_ratio=False))
        self.add_widget(Image(source=os.path.join(YOL, 'arvexapusula.png'), size_hint=(0.85, 0.85),
                              pos_hint={'center_x': 0.5, 'center_y': 0.85}))

        # --- 2. ANA KADRAN ÜNİTESİ ---
        self.ana_kare = FloatLayout(size_hint=(0.95, 0.45), pos_hint={'center_x': 0.5, 'center_y': 0.555})
        self.add_widget(self.ana_kare)

        self.altin_yon = RotatableImage(
            source=os.path.join(YOL, 'altin_yon.png'),
            size_hint=(0.30, 0.30),
            pos_hint={'center_x': 0.5, 'center_y': 0.835}
        )
        self.altin_yon.set_angle(180)


        self.pusula_cerceve = RotatableImage(
            source=os.path.join(YOL, 'pusula_cerceve.png'),
            size_hint=(0.83, 0.83),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        self.ana_kare.add_widget(self.pusula_cerceve)
        # Hataları gizleyen sabit üst çerçeve eklemesi
        self.sabit_cerceve = Image(
            source=os.path.join(YOL, 'cerceve.png'),
            size_hint=(1.0, 1.0),
            pos_hint={'center_x': 0.5, 'center_y': 0.490},
            allow_stretch=True,
            keep_ratio=True
        )
        self.ana_kare.add_widget(self.sabit_cerceve)
        self.ana_kare.add_widget(self.altin_yon)
        self._terazi_kur()

        # --- 3. ÜST PANEL (YÖN TABELASI) ---
        self.panel = Image(source=os.path.join(YOL, 'panel.png'), size_hint=(0.8, 0.09),
                           pos_hint={'center_x': 0.5, 'y': 0.26})
        self.add_widget(self.panel)
        self.panel_metni = Label(text="PUSULA", font_size='22sp', bold=True, color=ALTIN_RENK,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.307})
        self.add_widget(self.panel_metni)

        # --- 4. BUTONLAR ---
        self.btn_pusula = ImageButton(source=os.path.join(YOL, 'pusula_buton.png'), size_hint=(0.33, 0.33),
                                      pos_hint={'center_x': 0.28, 'center_y': 0.10})
        self.btn_terazi = ImageButton(source=os.path.join(YOL, 'suterazisi_buton.png'), size_hint=(0.33, 0.33),
                                      pos_hint={'center_x': 0.72, 'center_y': 0.10})
        self.add_widget(self.btn_pusula)
        self.add_widget(self.btn_terazi)

        self.btn_pusula.bind(on_press=self.ekran_pusula)
        self.btn_terazi.bind(on_press=self.ekran_terazi)

        # --- 5. EN ALT KOORDİNAT TABELASI ---
        self.panel_2 = Image(source=os.path.join(YOL, 'panel.png'), size_hint=(0.8, 0.08),
                             pos_hint={'center_x': 0.5, 'y': 0.18})
        self.add_widget(self.panel_2)

        self.panel_koordinat = Label(
            text="Enlem: 41.001254\nBoylam: 28.934587",
            font_size='13sp',
            bold=True,
            color=ALTIN_RENK,
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.220}
        )
        self.add_widget(self.panel_koordinat)

        Clock.schedule_interval(self.motor_guncelle, 1 / 30)
        self.ekran_pusula(None)

    def _terazi_kur(self):
        # 1. Dikey Terazi
        self.terazi_dikey = Image(source=os.path.join(YOL, 'dikey_terazi.png'), size_hint=(0.18, 0.45),
                                  pos_hint={'center_x': 0.15, 'center_y': 0.42}, opacity=0)
        self.damla_dikey = Image(source=os.path.join(YOL, 'damla_kabarcik.png'), size_hint=(0.12, 0.12),
                                 pos_hint={'center_x': 0.15, 'center_y': 0.42}, opacity=0)

        # 2. Yatay Terazi
        self.terazi_yatay = Image(source=os.path.join(YOL, 'yatay_terazi.png'), size_hint=(0.7, 0.18),
                                  pos_hint={'center_x': 0.50, 'center_y': 0.70}, opacity=0)
        self.damla_yatay = Image(source=os.path.join(YOL, 'damla_kabarcik.png'), size_hint=(0.12, 0.12),
                                 pos_hint={'center_x': 0.50, 'center_y': 0.70}, opacity=0)

        # 3. 45 Derecelik Eğim Terazisi
        self.terazi_egimli = RotatableImage(source=os.path.join(YOL, 'dikey_terazi.png'), size_hint=(0.18, 0.45),
                                            pos_hint={'center_x': 0.65, 'center_y': 0.40}, opacity=0)
        self.terazi_egimli.set_angle(-45)

        self.damla_egimli = Image(source=os.path.join(YOL, 'damla_kabarcik.png'), size_hint=(0.12, 0.12),
                                  pos_hint={'center_x': 0.65, 'center_y': 0.40}, opacity=0)

        # 4. Merkez Terazi
        self.terazi_merkez = Image(source=os.path.join(YOL, 'merkez_terazi.png'), size_hint=(0.40, 0.40),
                                   pos_hint={'center_x': 0.45, 'center_y': 0.50}, opacity=0)
        self.damla_merkez = Image(source=os.path.join(YOL, 'damla_kabarcik.png'), size_hint=(0.11, 0.11),
                                  pos_hint={'center_x': 0.45, 'center_y': 0.50}, opacity=0)

        for w in [self.terazi_dikey, self.damla_dikey, self.terazi_yatay, self.damla_yatay,
                  self.terazi_egimli, self.damla_egimli, self.terazi_merkez, self.damla_merkez]:
            self.add_widget(w)

    def _temizle(self):
        self.ana_kare.opacity = 0
        self.panel.opacity, self.panel_metni.opacity = 0, 0
        self.panel_2.opacity, self.panel_koordinat.opacity = 0, 0
        for attr in ['terazi_yatay', 'terazi_dikey', 'terazi_egimli', 'terazi_merkez',
                     'damla_yatay', 'damla_dikey', 'damla_egimli', 'damla_merkez']:
            if hasattr(self, attr):
                getattr(self, attr).opacity = 0

    def ekran_pusula(self, instance):
        self._temizle()
        self.ana_kare.opacity = 1
        self.panel.opacity, self.panel_metni.opacity = 1, 1
        self.panel_2.opacity, self.panel_koordinat.opacity = 1, 1

    def ekran_terazi(self, instance):
        self._temizle()
        for attr in ['terazi_dikey', 'terazi_yatay', 'terazi_egimli', 'terazi_merkez',
                     'damla_dikey', 'damla_yatay', 'damla_egimli', 'damla_merkez']:
            if hasattr(self, attr):
                getattr(self, attr).opacity = 1

    def yon_metni_al(self, derece):
        derece = derece % 360
        if (derece >= 337.5) or (derece < 22.5):
            return "KUZEY"
        elif 22.5 <= derece < 67.5:
            return "KUZEY DOĞU"
        elif 67.5 <= derece < 112.5:
            return "DOĞU"
        elif 112.5 <= derece < 157.5:
            return "GÜNEY DOĞU"
        elif 157.5 <= derece < 202.5:
            return "GÜNEY"
        elif 202.5 <= derece < 247.5:
            return "GÜNEY BATI"
        elif 247.5 <= derece < 292.5:
            return "BATI"
        elif 292.5 <= derece < 337.5:
            return "KUZEY BATI"
        return ""

    def motor_guncelle(self, dt):
        try:
            accel = accelerometer.acceleration
            if accel and len(accel) >= 3 and accel[0] is not None:
                mx = (accel[0] * Window.width / 20) + (Window.width / 2)
                my = (accel[1] * Window.height / 20) + (Window.height / 2)
            else:
                mx, my = Window.mouse_pos
        except:
            mx, my = Window.mouse_pos

        ham_aci = (mx / Window.width) * 360
        sensor_angle = (ham_aci + 2) % 360

        # AMORTİSÖR SİSTEMİ (Mevcut yapıyı bozmayan esnek bağ)
        if not hasattr(self, 'current_angle'):
            self.current_angle = sensor_angle

        fark = sensor_angle - self.current_angle
        if fark > 180:
            fark -= 360
        elif fark < -180:
            fark += 360

        self.current_angle += fark * 0.15
        self.aci = self.current_angle % 360
        import math
        radyan = math.radians(self.aci)
        yalpalama_x = math.sin(radyan) * 0.01  # Bu çarpan milimetrik kaymayı sönümler
        yalpalama_y = math.cos(radyan) * 0.01
        self.pusula_cerceve.pos_hint = {'center_x': 0.5 - yalpalama_x, 'center_y': 0.5 - yalpalama_y}
        if self.ana_kare.opacity == 1:
            yon_adi = self.yon_metni_al(self.aci)
            gosterilecek_aci = 0 if int(self.aci) == 0 else int(self.aci)
            self.panel_metni.text = f"{yon_adi}  {gosterilecek_aci}°"
            self.pusula_cerceve.set_angle(self.aci)

        if self.terazi_merkez.opacity == 1:
            dx = (mx / Window.width - 0.5)
            dy = (my / Window.height - 0.5)

            # Dikey Terazi: Hareket alanı damla boyu kadar
            self.damla_dikey.pos_hint = {'center_x': 0.15, 'center_y': 0.42 + max(-0.10, min(0.10, dy * 0.5))}

            # Yatay Terazi
            self.damla_yatay.pos_hint = {'center_x': 0.50 + (max(-0.22, min(0.22, dx * 0.92))), 'center_y': 0.70}

            # Eğimli Terazi
            oranli_hareket = max(-0.07, min(0.07, dy))
            self.damla_egimli.pos_hint = {'center_x': 0.65 + (oranli_hareket * 2.16), 'center_y': 0.40 + oranli_hareket}

            # Merkez Terazi
            self.damla_merkez.pos_hint = {'center_x': 0.45 + max(-0.04, min(0.04, dx * 0.2)),
                                          'center_y': 0.50 + max(-0.04, min(0.04, dy * 0.2))}


class ArvexaApp(App):
    def build(self):
        Window.size = (300, 650)
        return ArvexaPusula()


if __name__ == '__main__':
    ArvexaApp().run()