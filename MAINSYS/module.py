from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Ellipse, InstructionGroup, Rectangle, Canvas
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.graphics.texture import Texture


import cv2
import numpy as np
import os
import csv
import time
from datetime import datetime
import datetime 
import japanize_kivy
import subprocess
import math
import pytz
import requests
import pandas as pd




pixels_per_inch = 96
width_cm = 15
height_cm = 8
width_pixels = int(width_cm * pixels_per_inch / 2.54)
height_pixels = int(height_cm * pixels_per_inch / 2.54)
Window.size = (width_pixels, height_pixels)



################################↓↓↓syoki↓↓↓##############################################################



class SyokiScreen(Screen):
    def __init__(self, **kwargs):
        super(SyokiScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        

        title_label = Label(
            text="朝の目覚めにこのシステム",
            font_size=66,
            size_hint_y=None,
            height=500,
            halign="center",
        )

        subtitle_label = Label(
            text="Morning Pi",
            font_size=51,
            size_hint_y=None,
            height=100,
            halign="center",
        )

        layout.add_widget(Label())  # 上部の余白用
        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)

        button = Button(text="実行", size_hint=(None, None), size=(150, 50))
        button.bind(on_press=self.show_confirmation_popup)

        center_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        center_layout.add_widget(Label())  # 左側の余白
        center_layout.add_widget(button)
        center_layout.add_widget(Label())  # 右側の余白
        layout.add_widget(center_layout)

        #Window.bind(on_resize=self.on_window_resize)

        self.add_widget(layout)

    def on_window_resize(self, instance, width, height):
        self.set_background_color(self.background_color, width, height)

    def on_start(self):
        self.background_color = (0.5, 0.5, 0.5, 1)
        title_color = (1, 1, 1, 1)
        subtitle_color = (1, 1, 1, 1)
        self.set_background_color(self.background_color, Window.width, Window.height)
        self.set_text_color(title_color, subtitle_color)

    def set_background_color(self, color, width, height):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            Rectangle(pos=self.pos, size=(width, height))

    def set_text_color(self, title_color, subtitle_color):
        self.children[1].color = title_color
        self.children[2].color = title_color

    def show_confirmation_popup(self, instance):
        flg = self.optflg(11)
        if flg == "1":
            self.manager.current = 'maindisplay_screen'
        else:
            self.manager.current = 'colorpicker_screen'

    def optflg(self, val):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[val][1]
        return optdata


################################↓↓↓haikei↓↓↓##############################################################


class BackgroundColorScreen(Screen):
    def __init__(self, **kwargs):
        super(BackgroundColorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        label_background = Label(text="背景色変更")
        self.label_background = label_background

        self.background_color_picker = ColorPicker()
        self.background_color_picker.bind(color=self.on_background_color)

        label_text = Label(text="文字色変更")
        self.label_text = label_text

        self.text_color_picker = ColorPicker()
        self.text_color_picker.bind(color=self.on_text_color)

        button = Button(text="背景色を変更", on_press=self.change_background_and_text_color)

        layout.add_widget(label_background)
        layout.add_widget(self.background_color_picker)
        layout.add_widget(button)

        Window.bind(on_resize=self.on_window_resize)

        self.add_widget(layout)

    def on_window_resize(self, instance, width, height):
        font_size = int(0.04 * height)
        self.label_background.font_size = font_size
        self.label_text.font_size = font_size

    def on_background_color(self, instance, value):
        pass

    def on_text_color(self, instance, value):
        self.label_background.color = value
        self.label_text.color = value

    def change_background_and_text_color(self, instance):
        self.setflg(2)
        background_color = self.background_color_picker.color
        text_color = self.text_color_picker.color

        background_red, background_green, background_blue, background_alpha = background_color
        text_red, text_green, text_blue, text_alpha = text_color



        #self.save_colors_to_csv(csv_path, background_red, background_green, background_blue, background_alpha, text_red, text_green, text_blue, text_alpha)



        setflg_row = 10
        syokiflg_row = 11
        setflg = self.optflg(setflg_row)
        syokiflg = self.optflg(syokiflg_row)
        if syokiflg == '0' and setflg == '0':
            self.manager.current = 'posmover_screen'
        elif syokiflg == '1' and setflg == '1':
            pass
        else :
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
            self.manager.current = 'syoki_screen'


    def save_colors_to_csv(self, csv_file, background_red, background_green, background_blue, background_alpha,
                           text_red, text_green, text_blue, text_alpha):
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['BackgroundRed', 'BackgroundGreen', 'BackgroundBlue', 'BackgroundAlpha',
                          'TextRed', 'TextGreen', 'TextBlue', 'TextAlpha']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'BackgroundRed': background_red,
                'BackgroundGreen': background_green,
                'BackgroundBlue': background_blue,
                'BackgroundAlpha': background_alpha,
                'TextRed': text_red,
                'TextGreen': text_green,
                'TextBlue': text_blue,
                'TextAlpha': text_alpha
            })

    def optflg(self, val):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[val][1]
        return optdata

    def setflg(self, flgval):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[4][1] = flgval

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")



################################↓↓↓haikei↓↓↓##############################################################



class MyButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.source = kwargs["source"]
        self.texture = self.button_texture(self.source)
 
    def on_state(self, widget, value):
        if value == 'down':
            self.texture = self.button_texture(self.source, off=True)
        else:
            self.texture = self.button_texture(self.source)
 
    def button_texture(self, data, off=False):
        im = cv2.imread(data)
        im = self.square_image(im)
        if off:
            im = self.adjust(im, alpha=0.6, beta=0.0)
            im = cv2.rectangle(im, (2, 2), (im.shape[1] - 2, im.shape[0] - 2), (255, 255, 0), 10)
 
        buf = cv2.flip(im, 0)
        image_texture = Texture.create(size=(im.shape[1], im.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        return image_texture
 
    def square_image(self, img):
        h, w = img.shape[:2]
        if h > w:
            x = int((h - w) / 2)
            img = img[x:x + w, :, :]
        elif h < w:
            x = int((w - h) / 2)
            img = img[:, x:x + h, :]
 
        return img
 
    def adjust(self, img, alpha=1.0, beta=0.0):
        dst = alpha * img + beta
        return np.clip(dst, 0, 255).astype(np.uint8)
 
 
class Test(Screen):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
 
        image_dir = os.path.join(os.path.dirname(__file__), "")
 
        # BoxLayoutを作成し、その中にImageとScrollViewを配置
        box_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.image = Image(size_hint=(1, 0.1))
        box_layout.add_widget(self.image)
 
        sc_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height*0.2))
        grid_layout = GridLayout(cols=5, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        grid_layout = self.image_load(image_dir, grid_layout)
        sc_view.add_widget(grid_layout)
 
        # ボタンを横に並べるBoxLayoutを作成
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
 
        # 確定ボタンに変更
        self.confirm_button = Button(text="確定", size_hint=(0.5, None), height=50)
        self.confirm_button.bind(on_press=self.confirm_action)
 
        self.prev_button = Button(text="戻る", size_hint=(0.5, None), height=50)
        self.prev_button.bind(on_press=self.prev_image)
 
        button_layout.add_widget(self.prev_button)
        button_layout.add_widget(self.confirm_button)
 
        # BoxLayoutに追加
        box_layout.add_widget(sc_view)
        box_layout.add_widget(button_layout)
 
        # BoxLayoutをScreenに追加
        self.add_widget(box_layout)
 
    def image_load(self, im_dir, grid):
        images = [f for f in os.listdir(im_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        images = sorted(images)
 
        for image in images:
            button = MyButton(size_hint_y=None,
                              height=300,
                              source=os.path.join(im_dir, image),
                              group="g1")
            button.bind(on_press=self.set_image)
            grid.add_widget(button)
 
        return grid
 
    def set_image(self, btn):
        if btn.state == "down":
            self.image_name = btn.source
            Clock.schedule_once(self.update)
 
    def update(self, t):
        self.image.source = self.image_name
 
    def confirm_action(self, instance):
        # 保存機能を削除し、代わりにCSVに保存していた情報をprintで表示
        syokiflg, setflg = self.optflg()
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            if syokiflg == '0':
                print(f"Image confirmed: {self.image_name}")
                # csvに保存
                data[14][1] = self.image_name
                data[4][1] = 1
                with open(filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
                    print("保存されました！")
 


            elif syokiflg == '1':
                print(f"Image confirmed: {self.image_name}")
                # 何らかの処理を追加する場合はここに記述
                # csvに保存
                data[14][1] = self.image_name
                data[4][1] = 1
                with open(filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
                    print("保存されました！")
                
                self.manager.current = 'set_screen'
 
                pass



 
    def prev_image(self, instance):
        # 戻るボタンが押下されたときの処理
        self.manager.current = 'set_screen'
 
    def optflg(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
 
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            syokiopt = data[11][1]
            setopt = data[10][1]
 
        return syokiopt, setopt
 
 




################################↓↓↓posmover↓↓↓##############################################################


class PosMoverScreen(Screen):
    def __init__(self, **kwargs):
        super(PosMoverScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # ボタンリスト
        self.buttons = []  # ここで初期化
        self.background_color = [1, 1, 1, 1]  # デフォルトは白い背景

        bgopt = self.loadhaikei()

        print(bgopt)
        # 背景の色と画像のパスを取得
        background_color, background_image_path = self.get_background_settings(bgopt)
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path == None:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ボタンの名前と初期位置
        button_info = [
            {"name": "時計", "pos": (50, 100)},
            {"name": "天気", "pos": (100, 100)},
            {"name": "予定", "pos": (150, 100)},
            {"name": "追加", "pos": (200, 100)},
        ]

        for info in button_info:
            # ボタンを作成
            button = Button(text=info["name"])
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = info["pos"]

            # ボタンが移動したときのイベントを追加
            button.bind(on_touch_move=self.on_button_move)

            # ボタンの背景色と文字色を設定
            button.background_color = self.background_color
            button.color = [0, 0, 0, 1]  # デフォルトは黒い文字

            # ボタンをレイアウトに追加
            self.layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)  # ここで追加

        # 確定ボタンを作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 50), pos=(self.layout.width - 100, 0))
        confirm_button.bind(on_press=self.on_confirm_button_press)
        self.layout.add_widget(confirm_button)


        self.add_widget(self.layout)


    def on_button_move(self, instance, touch):
        # ボタンがタッチされ、移動したときに呼ばれるメソッド
        if instance.collide_point(*touch.pos):
            instance.pos = (touch.x - instance.width / 2, touch.y - instance.height / 2)



    def get_background_settings(self,bgopt):
        # selected_backgrounds.csvから背景画像のパスを取得
        if bgopt == 1:
            background_image_path = self.get_background_image_path(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            return (1, 1, 1, 1), background_image_path
                
        else:
        # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            return background_color, None

    def get_background_image_path(self, csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        background_image_path = row[0]
                        return background_image_path
        except FileNotFoundError:
            pass
        return None

    def get_background_color(self, csv_file):
        # color_settings.csvから背景色を取得
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                data = list(reader)
                background1 = data[8][1]
                background2 = data[8][2]
                background3 = data[8][3]
                background4 = data[8][4]

                background_color = (float(background1), float(background2), float(background3), float(background4))
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color

    def save_button_positions(self):
        # 各ボタンの座標をCSVファイルに保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            i=1
            for button in self.buttons:
                button_pos = button.pos

                data[16 +i][1] = button_pos[0]
                data[16 +i][2] = button_pos[1]
                i+=1

        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押下されたときの処理
        syokiflg,setflg = self.optflg()
        self.save_button_positions()
        if syokiflg == '0':
            self.save_button_positions()
            self.manager.current = 'maindisplay_screen'
            self.setflg(1)
        elif syokiflg == '1':
            self.manager.current = 'set_screen'
            self.setflg(1)
            pass

        
    def update_time(self, dt):

        self.background_color = [0, 0, 0, 0]  # デフォルトは黒い背景

        bgopt = self.loadhaikei()
        #self.setflg(1)
        print("bgopt:", bgopt)
        if bgopt == "2":
            #背景色
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            background_image_path = None
        else:
            # 背景の色と画像のパスを取得
            background_color, background_image_path = self.get_background_settings()
        
        
        
        
        # 背景の色を設定
        with MainDisplayScreen.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path:
            with MainDisplayScreen.layout.canvas.before:
                self.load_background_image(background_image_path)

    
    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[11][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")

        return 
    

    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)


    def on_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # ウィンドウサイズが変更されたときに呼び出される関数
        self.update_background_size()


    def update_background_size(self):
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size
    
    def loadhaikei(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata
    
    def optflg(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            syokiopt = data[11][1]
            setopt = data[10][1]
            

        return syokiopt, setopt



################################↓↓↓mainfacter↓↓↓##############################################################





# 天気情報：WeatherApp
# 予定情報：CalendarApp
# 時計：ClockApp

## インチあたりのピクセル数
pixels_per_inch = 96

# 縦8cm、横15cmのサイズをピクセルに変換
width_cm = 15
height_cm = 8
width_pixels = int(width_cm * pixels_per_inch / 2.54)
height_pixels = int(height_cm * pixels_per_inch / 2.54)

# ウィンドウサイズの指定
Window.size = (width_pixels, height_pixels)

class MainDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(MainDisplayScreen, self).__init__(**kwargs)
        
        # レイアウトのインスタンスを作成
        self.layout = FloatLayout()
        Clock.schedule_interval(self.bgupdate, 1)
        self.background_color = [0, 0, 0, 0]  # デフォルトは黒い背景

        bgopt = self.loadhaikei()
        print(bgopt)
        #self.setflg(1)
        if bgopt == "2":
            #背景色
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            background_image_path = None
        else:
            # 背景の色と画像のパスを取得
            background_color, background_image_path = self.get_background_settings()

        print("background_color:", background_color)
        print("background_image_path:", background_image_path)
        
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.update_background_size)

        # calenderApp と WeatherApp のインスタンスを作成
        weather_app = WeatherScreen()
        calender_app = CalendarScreen()
        clock_app = DigitalClockScreen()
        #analog_app = AnalogClockScreen()
        #audio_app = MusicPlayerApp()

        weather_app.update_weather_color()

        # 各アプリのレイアウトを作成
        self.weather_layout = weather_app.build()
        self.calendar_layout = calender_app.build()
        #audio_layout = audio_app.build()
        
        clock_judgement = self.loadclockselect()
        print("clock_judgement", clock_judgement)
        if clock_judgement == "2":
            print("デジタル時計を使用します")
            self.clock_layout = clock_app.build()
            # 時間アプリの座標を読み込みif分追加
            posrow = 17
            x, y = self.load_button_position(posrow)
            self.clock_layout.pos = (x, y)
        else:
            print("アナログ時計を使用します")
            print("デジタル時計を使用します")
            clock_layout = clock_app.build()
            # 時間アプリの座標を読み込みif分追加
            posrow = 17
            x, y = self.load_button_position(posrow)
            clock_layout.pos = (x, y)
            #clock_layout = analog_app.build()

            #posrow = 17
            #x, y = self.load_button_position(posrow)
            #clock_layout.pos=(100, 100)
            #clock_layout.pos = (x + 210, y + 115)


        posrow = 17
        x, y = self.load_button_position(posrow)
        self.clock_layout.pos = (x, y)

        # 天気アプリの座標を読み込み
        posrow = 18
        x, y = self.load_button_position(posrow)
        self.weather_layout.pos = (x, y)

        # 予定アプリの座標を読み込み
        posrow = 19
        x, y = self.load_button_position(posrow)
        self.calendar_layout.pos = (x, y)

        # 追加アプリの座標を読み込み
        posrow = 20
        x, y = self.load_button_position(posrow)
        #audio_layout.pos = (x, y)
        #audio_layout.size_hint=(0.15,0.15)

        # 設定ボタンの生成
        button_image_path = os.path.join(os.path.dirname(__file__), '1.png')
        button = Image(source=button_image_path, size_hint=(0.1, 0.15), pos_hint={'top': 1})
        button.bind(on_touch_down=self.on_settings_button_press)

        self.add_widget(self.layout)
        self.layout.add_widget(button)
        weatherumu, calenderumu, clockumu, audioum = self.loadumu()
        if weatherumu == "on":
            self.layout.add_widget(self.weather_layout)
        if calenderumu == "on":
            self.layout.add_widget(self.calendar_layout)
        if clockumu == "on":
            self.layout.add_widget(self.clock_layout)
        #if audioum == "on":
            #self.layout.add_widget(audio_layout)

        

    def bgupdate(self,dt):
        self.background_color = [0, 0, 0, 0]  # デフォルトは黒い背景

        bgopt = self.loadhaikei()
        #self.setflg(1)

        if bgopt == "2":
            #背景色
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            background_image_path = None
        else:
            # 背景の色と画像のパスを取得
            background_color, background_image_path = self.get_background_settings()

        
        posrow = 17
        x, y = self.load_button_position(posrow)
        self.clock_layout.pos = (x, y)
        
        # 天気アプリの座標を読み込み
        posrow = 18
        x, y = self.load_button_position(posrow)
        self.weather_layout.pos = (x, y)

        # 予定アプリの座標を読み込み
        posrow = 19
        x, y = self.load_button_position(posrow)
        self.calendar_layout.pos = (x, y)
        

        
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.update_background_size)


        
    def on_settings_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'set_screen'
            #App.get_running_app().stop()

    def get_background_settings(self):
         # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
        background_image_path = self.get_background_image_path(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
        
        return (1, 1, 1, 1), background_image_path

    def get_background_image_path(self, csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[14][1]

        return optdata

    def get_background_color(self, csv_file):
        # color_settings.csvから背景色を取得
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                data = list(reader)
                background1 = data[8][1]
                background2 = data[8][2]
                background3 = data[8][3]
                background4 = data[8][4]

                background_color = (float(background1), float(background2), float(background3), float(background4))
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color
    
    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

    def update_background_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size

        # 背景画像のサイズも更新
        if hasattr(self, 'background_image'):
            self.background_image.size = self.layout.size
    
    # CSVファイルからアプリの座標を取得するメソッド
    def load_button_position(self, row):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            button_pos_x = data[row][1]
            button_pos_x = button_pos_x
            button_pos_x = float(button_pos_x) - 223.0

            button_pos_y = data[row][2]
            button_pos_y = float(button_pos_y)
            button_pos_y = button_pos_y - 132.0

        return button_pos_x, button_pos_y
    
    def loadhaikei(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata
    
    def loadumu(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata1 = data[12][1]
            optdata2 = data[12][2]
            optdata3 = data[12][3]
            optdata4 = data[12][4]

        return optdata1,optdata2,optdata3,optdata4
    
    def loadclockselect(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[9][1]

        return optdata
    
    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[11][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")

        return 



################################↓↓↓onoD_weather↓↓↓##############################################################



class WeatherScreen(Screen):
    def get_weather_meaning(self, weather_code):
        if 0 <= weather_code <= 3:
            return "晴れ"
        elif 4 <= weather_code <= 9:
            return "霞、ほこり、砂または煙"
        elif 20 <= weather_code <= 29:
            return "降水、霧、氷霧、または雷雨"
        elif 30 <= weather_code <= 35:
            return "塵嵐、砂嵐"
        elif 36 <= weather_code <= 39:
            return "吹雪または吹雪"
        elif 40 <= weather_code <= 49:
            return "霧または氷"
        elif 50 <= weather_code <= 59:
            return "霧または氷"
        elif 60 <= weather_code <= 69:
            return "霧雨"
        elif 70 <= weather_code <= 79:
            return "雨"
        elif 80 <= weather_code <= 89:
            return "にわか降水"
        elif 90 <= weather_code <= 99:
            return "降雪またはしんしゃく"
        elif 100 <= weather_code <= 199:
            return "あられ"
        else:
            return "不明な天気"
        
    def get_fpass(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            fcolor1 = data[7][1]
            fcolor2 = data[7][2]
            fcolor3 = data[7][3]
            fcolor4 = data[7][4]

            fpass = data[27][1]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4


    def format_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
        return formatted_date

    def build(self):

        fsize = "20"

        layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(0.7,0.7))
        coordinates_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'IDOKEIDO-UTF8.csv'))

        if 'latitude' in coordinates_df.columns and 'longitude' in coordinates_df.columns:
            self.selected_data = None


            def update_weather(dt):
                # horizontal_layout のウィジェットをクリア
                
                url = "https://api.open-meteo.com/v1/forecast"

                if self.selected_data is None:
                    user_latitude, user_longitude, selected_days = self.loadopt()

                    params = {
                        "latitude": user_latitude,
                        "longitude": user_longitude,
                        "hourly": "temperature_2m",
                        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
                        "timezone": "Asia/Tokyo"
                    }

                    response = requests.get(url, params=params)

                    data = response.json()
                    hourly_data = data["hourly"]
                    daily_data = data["daily"]

                    # 日数に応じて表示するデータの範囲を調整
                    if selected_days == "1":
                        range_end = 1
                    elif selected_days == "3":
                        range_end = 3
                    else:
                        range_end = 1  # デフォルトは1日

                    for i in range(range_end):
                        date = hourly_data["time"][i*24]
                        #formatted_date = self.format_date(date)
                        temperature = hourly_data["temperature_2m"][i]
                        max_temperature = daily_data["temperature_2m_max"][i]
                        min_temperature = daily_data["temperature_2m_min"][i]
                        weather_code = daily_data["weather_code"][i]
                        weather_meaning = self.get_weather_meaning(weather_code)

                        string_to_remove = "2024-01-"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "2024-02-"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "00:00"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "-"
                        #formatted_date = formatted_date.replace(string_to_remove, "/")

                        # 横に並べて表示するために BoxLayout を使用
                        
                        if i == 0:
                            day = "今日\n"
                        elif i == 1:
                            day = "明日\n"
                        elif i == 2:
                            day = "明後日\n"
                        else: day = "" 

                        fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()

                        weather_label = Label(text=
                                            day      #+f" {formatted_date}日\n" 
                                           +f"\nNow:{temperature} ℃\n"
                                           +f"{max_temperature}℃/{min_temperature}℃\n"
                                           +f"天気: {weather_meaning}\n"
                                           ,font_size=fsize+'sp'
                                           ,font_name=fpass
                                           ,color=[float(fcolor1), float(fcolor2), float(fcolor3), float(fcolor4)])
                        


            
                        # box に各情報を追加
                        layout.add_widget(weather_label)

                        

                        

                else:
                    layout.add_widget(Label(text=f"エラー: {response.status_code}"))

            update_weather(dt = 10)
            Clock.schedule_interval(update_weather, 1800)
            

            return layout
        else:
            return Label(text="エラー: CSVファイルに 'latitude' と 'longitude' の列がありません。")

    def update_weather_color(self):
            fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()
            #weather_label.color = (float(fcolor1), float(fcolor2), float(fcolor3), float(fcolor4))
        

    def loadopt(self):
        # CSVファイルに緯度・経度・日数を保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            idodata = data[5][1]
            keidodata = data[5][2]
            daydata = data[6][1]


        return idodata, keidodata, daydata
    

    


################################↓↓↓onoD_calendar↓↓↓##############################################################



class CalendarScreen(Screen):
    def get_fpass(self):
        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            fpass = data[27][1]

            fcolor1 = data[7][1]
            fcolor2 = data[7][2]
            fcolor3 = data[7][3]
            fcolor4 = data[7][4]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4
    
    def build(self):
        fsize = "18"

        layout = BoxLayout(orientation='vertical')

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        calendar_id = 'j5gr4sa@gmail.com'
        gapi_creds = load_credentials_from_file(
            os.path.join(os.path.dirname(__file__),'j5g-p-403802-f6d11f806041.json'),
            SCOPES
        )
        service = build('calendar', 'v3', credentials=gapi_creds[0])

        day = datetime.date.today()
        start_of_day = datetime.datetime(day.year, day.month, day.day, 0, 0, 0).isoformat() + 'Z'
        end_of_day = datetime.datetime(day.year, day.month, day.day, 23, 59, 59).isoformat() + 'Z'

        event_list = service.events().list(
            calendarId=calendar_id, timeMin=start_of_day, timeMax=end_of_day,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = event_list.get('items', [])
        schedule = "[今日の予定]\n"

        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            summary = event['summary']

            if 'date' in start_time:
                schedule += f'{start_time}: {summary} (終日)\n'
            else:
                schedule += f'{start_time} ～ {end_time}: {summary}\n'

        string_to_remove = "2024-"
        schedule = schedule.replace(string_to_remove, "")
        string_to_remove = ":00+09:00"
        schedule = schedule.replace(string_to_remove, " ")
        string_to_remove = "-"
        schedule = schedule.replace(string_to_remove, "/")
        string_to_remove = "T"
        schedule = schedule.replace(string_to_remove, " ")

        fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()

        # フォントを変更
        schedule_label = Label(text=schedule,
                               font_size=fsize + 'sp', 
                               font_name=fpass,
                               color=[float(fcolor1), float(fcolor2), float(fcolor3), float(fcolor4)])  # color を使用
        layout.add_widget(schedule_label)

        return layout



################################↓↓↓onoD_clock↓↓↓##############################################################



class DigitalClockScreen(Screen):
    def build(self):
        fontname, fcolar1,fcolar2,fcolar3,fcolar4 = self.load_csv()
        fcolar1 = float(fcolar1)
        fcolar2 = float(fcolar2)
        fcolar3 = float(fcolar3)
        fcolar4 = float(fcolar4)
        
        self.font_path = fontname
        LabelBase.register(name=fontname, fn_regular=self.font_path)

        self.layout = BoxLayout(orientation='vertical')
        self.time_label = Label(
            text=self.get_japanese_time(),
            font_name=fontname,  # 初期フォントを指定
            font_size='40sp',
            halign='center',
            valign='middle',
            color=[fcolar1,fcolar2,fcolar3,fcolar4]  # 色を指定
        )
        
        self.layout.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)
        return self.layout

    def update_time(self, dt):
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        return current_time
    
    def load_csv(self):
        # CSVファイルからフォントの色とフォント情報を取得するメソッド

        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            
            fpass = data[24][1]
            fcolor1 = data[23][1]
            fcolor2 = data[23][2]
            fcolor3 = data[23][3]
            fcolor4 = data[23][4]
            

        return fpass,fcolor1,fcolor2,fcolor3,fcolor4
    


################################↓↓↓setting↓↓↓##############################################################


class SetScreen(Screen):
    def __init__(self, **kwargs):
        super(SetScreen, self).__init__(**kwargs)

        # タイトル表示用のラベルを作成
        title_label = Label(text="設定", font_size=24, size_hint_y=None, height=50, pos_hint={'center_x': 0.5, 'top': 0.9})
        self.add_widget(title_label)

        # 上部に縦並びでボタンを配置するBoxLayout
        top_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, #spacing=10, 
                                       pos_hint={'center_x': 0.5, 'top': 1})

        # ボタンの作成と追加
        button_names = ["時間表示設定", "天気予報", "機能選択", "背景色"]
        for i, name in enumerate(button_names):
            button = Button(text=name, size_hint=(None, None), size=(140, 50))
            button.bind(on_press=self.on_button_press)
            
            top_buttons_layout.add_widget(button)

            # 2列目のボタンを挿入
            if i % 2 == 1:
                top_buttons_layout.add_widget(BoxLayout(size_hint_x=None, width=10))

        # 上部のボタンレイアウトを追加
        self.add_widget(top_buttons_layout)

    
        # 下部に横並びでボタンを配置するBoxLayout
        bottom_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, 
                                          #spacing=10, 
                                          pos_hint={'center_x': 0.5, 'top': 0.4})
        
        # ボタンの作成と追加
        button_names = ["背景画像", "追加", "配置設定","フォント"]
        for i, name in enumerate(button_names):
            button = Button(text=name, size_hint=(None, None), size=(140, 50))
            button.bind(on_press=self.on_button_press)
            
            bottom_buttons_layout.add_widget(button)

            if i % 2 == 1:
                bottom_buttons_layout.add_widget(BoxLayout(size_hint_x=None, width=10))

        # 下部のボタンレイアウトを追加
        self.add_widget(bottom_buttons_layout)

        # 戻るボタンを作成して右下に追加
        back_button = Button(text="戻る", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.9, 'y': 0.03})
        back_button.bind(on_press=self.on_button_press)
        self.add_widget(back_button)

    def on_button_press(self, instance):
        button_text = instance.text
        print(f"ボタン {button_text} が押されました！")

        if button_text == "時間表示設定":
            #app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/sentaku.py")
            self.manager.current = 'clockselect_screen'
        elif button_text == "天気予報":
            self.manager.current = 'weatherset_screen' #onoD_weatherSet.py")
        elif button_text == "機能選択":
            self.manager.current = 'appselector_screen'
        elif button_text == "背景色":
            self.manager.current = 'colorpicker_screen'
        elif button_text == "背景画像":
            self.manager.current = 'bgimage_screen'
        elif button_text == "追加":
            app_path = os.path.join(os.getcwd(), "MAINSYS/PROGRAMS/main_facter.py")
        elif button_text == "配置設定":
            self.manager.current = 'posmover_screen'
        elif button_text == "フォント":
            self.manager.current = 'font_screen'
        elif button_text == "戻る":
            self.manager.current = 'maindisplay_screen'
        

    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[10][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")
        
        return 



################################↓↓↓sentaku↓↓↓##############################################################



class ClockSelectScreen(Screen):

#class ImageSelectorApp(App):
    def __init__(self, **kwargs):
        super(ClockSelectScreen, self).__init__(**kwargs)
        # ウィンドウのサイズを設定
        Window.size = (600, 300)

        # レイアウトの作成
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # 左側のボックスレイアウト
        left_layout = BoxLayout(orientation='vertical', spacing=10)

        # 右側のボックスレイアウト
        right_layout = BoxLayout(orientation='vertical', spacing=10)

        # 画像表示用のウィジェットの作成
        image1 = Image(source=os.path.join(os.path.dirname(__file__),'1.jpg'))#hukei.jpg
        image2 = Image(source=os.path.join(os.path.dirname(__file__),'1.jpg'))#haikeihafguruma.jpg

        # 選択ボタンの作成
        button1 = Button(text='アナログ時計を選択', on_press=self.change_text_clock)
        
        button2 = Button(text='デジタル時計を選択', on_press=self.change_clock_text)
        button2.bind(on_press=self.digital_clock)

        # レイアウトにウィジェットを追加
        left_layout.add_widget(image1)
        left_layout.add_widget(button1)

        right_layout.add_widget(image2)
        right_layout.add_widget(button2)

        # メインのレイアウトに左右のレイアウトを追加
        layout.add_widget(left_layout)
        layout.add_widget(right_layout)

        self.add_widget(layout)

    

    def change_text_clock(self, instance):
        
        print("アナログ時計を選択が押されました。")
        # ファイルの読み込みと書き込みはここで行います
        file_path = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
            
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        # 必要な部分を変更
        data[9][1] = 1

        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        self.manager.current = 'set_screen'
        
    

    def change_clock_text(self, instance):
        
        print("デジタル時計を選択が押されました。")
        # ファイルの読み込みと書き込みはここで行います
        file_path = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
            
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        # 必要な部分を変更
        data[9][1] = 2

        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


    def digital_clock (self, instance):
        # "haikeigazou.py" を実行
        self.manager.current = 'timefont_screen' #time_display_app.py



################################↓↓↓tokeifont↓↓↓##############################################################
        



class TimeFontScreen(Screen):
    def __init__(self, **kwargs):
        super(TimeFontScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        fontcolor0,fontcolor1,fontcolor2,fontcolor3,font = self.load_settings_from_csv()
        fontcolor0 = float(fontcolor0)
        fontcolor1 = float(fontcolor1)
        fontcolor2 = float(fontcolor2)
        fontcolor3 = float(fontcolor3)
        
        self.font_path = font

        # 時刻表示用のラベル
        self.time_label = Label(text=self.get_japanese_time(),font_name=font, font_size='40sp', size_hint=(1, 0.6),color=[fontcolor0,fontcolor1,fontcolor2,fontcolor3])
        self.layout.add_widget(self.time_label)

        # フォント変更ボタン
        font_button = Button(text='フォント変更', on_press=self.show_font_chooser, size_hint=(1, 0.2))
        self.layout.add_widget(font_button)

        # 色変更ボタン
        color_button = Button(text='色変更', on_press=self.show_color_picker, size_hint=(1, 0.2))
        self.layout.add_widget(color_button)

        # 定期的に時間を更新するためのClockイベント
        Clock.schedule_interval(self.update_time, 1)

        # 色とフォントの初期設定
        fontcolor0,fontcolor1,fontcolor2,fontcolor3,font = self.load_settings_from_csv()
        self.font_path = font
        # 確定ボタン
        next_button = Button(text='確定', on_press=self.next_page, size_hint=(1, 0.1))
        self.layout.add_widget(next_button)

        # 戻るボタン
        prev_button = Button(text='戻る', on_press=self.prev_page, size_hint=(1, 0.1))
        self.layout.add_widget(prev_button)

        Clock.schedule_interval(self.update_time, 1)

        self.add_widget(self.layout)


    def update_time(self, dt):
        # 時間を更新する
                # 時間を更新する
        self.time_label.text = self.get_japanese_time()
        fontcolor0, fontcolor1, fontcolor2, fontcolor3, _ = self.load_settings_from_csv()
        fontcolor0 = float(fontcolor0)
        fontcolor1 = float(fontcolor1)
        fontcolor2 = float(fontcolor2)
        fontcolor3 = float(fontcolor3)

        # 新しい色を反映
        self.time_label.color = [fontcolor0, fontcolor1, fontcolor2, fontcolor3]


        

    def get_japanese_time(self):
        # 現在時刻を取得する
        return time.strftime("%H:%M:%S", time.localtime())


    def load_settings_from_csv(self):
        # settings.csvから色とフォント情報を読み取り、ラベルに設定
        csv_path = os.path.join(os.path.dirname(__file__),"onoD_opt.csv")
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            fontcolor0 = data[23][1]
            fontcolor1 = data[23][2]
            fontcolor2 = data[23][3]
            fontcolor3 = data[23][4]
            #iro 

            #フォント
            
            font = data[24][1]

        return fontcolor0,fontcolor1,fontcolor2,fontcolor3,font

    def save_settings_to_csv(self):
        # settings.csvに色とフォント情報を保存
        color_values, font_name = self.get_settings_data()

        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        # 絶対パスを相対パスに変換
        font_path_relative = os.path.relpath(font_name, start=os.getcwd())

        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)


            data[24][1] = font_path_relative  # Save the relative font path
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def get_settings_data(self):
        # 現在の色とフォント情報をリストで返す
        color_values = [round(value, 3) for value in self.time_label.color]
        print(color_values)
        # 色情報を4つの要素に固定
        while len(color_values) < 4:
            color_values.append(1.0)  # 不足している場合は1.0で埋める
        font_name = self.time_label.font_name
        return color_values, font_name

    def show_font_chooser(self, instance):
        popup = Popup(title='フォントを選択', size_hint=(0.9, 0.9))

        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path=os.path.dirname(__file__), filters=['*.ttf'])
        content.add_widget(file_chooser)


        def set_font(selected_font):
            self.time_label.font_name = selected_font
            popup.dismiss()




        button_layout = BoxLayout(size_hint_y=None, height=40)
        button_layout.add_widget(Button(text='キャンセル', on_press=popup.dismiss))
        button_layout.add_widget(Button(text='選択', on_press=lambda instance: set_font(file_chooser.selection[0])))

        content.add_widget(button_layout)
        popup.content = content
        popup.open()


    def show_color_picker(self, instance):
        self.manager.current = 'timecolor_screen'

    def next_page(self, instance):
        self.setflg(2)
        # ここに確定ボタンが押されたときの処理を書く
        # subprocessを使用してsettings.pyを実行する
        # 色とフォント情報をCSVに保存（上書き）
        self.save_settings_to_csv()

        # オプションで、新しいスクリプトを開始した後に現在のKivyアプリを終了することができます
        pass
        
    def prev_page(self, instance):
        # ここに戻るボタンが押されたときの処理を書く
        # subprocessを使用してsettings.pyを実行する
        self.manager.current = 'set_screen'

        # オプションで、新しいスクリプトを開始した後に現在のKivyアプリを終了することができます

        pass

    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[9][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")

        return 
    
##########################clockset######################################################


class TimeClolrScreen(Screen):
    def __init__(self, **kwargs):
        super(TimeClolrScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 選択された色を表示するラベル
        self.color_label = Label(text="選択された色がここに表示されます", size_hint_y=None, height=44)

        # パレットのボタン作成
        palette_layout = GridLayout(cols=4, spacing=10)
        for color, name in self.color_names.items():
            button = Button(text=name, background_color=color, on_press=self.on_palette_button_press, border=(5,5,5,5))
            palette_layout.add_widget(button)

        # 上部の色表示用のウィジェット
        self.color_display = BoxLayout(size_hint_y=None, height=44)

        # ボタン作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 40), on_press=self.on_confirm_button_press)
        back_button = Button(text="戻る", size_hint=(None, None), size=(100, 40), on_press=self.on_back_button_press)

        # ボタン用のレイアウト
        button_layout = BoxLayout(spacing=10)
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(back_button)

        # レイアウトに要素を追加
        layout.add_widget(self.color_label)
        layout.add_widget(palette_layout)
        layout.add_widget(self.color_display)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_palette_button_press(self, instance):
        color = instance.background_color
        selected_color = self.get_color_name(color)
        self.color_label.text = f"選択された色: {selected_color}"
        self.color_display.canvas.before.clear()  # 以前の色をクリア
        with self.color_display.canvas.before:
            Color(*color)
            Rectangle(pos=self.color_display.pos, size=self.color_display.size)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押されたときの処理
        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")


        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

            selected_color = self.color_label.text.strip().split(":")[-1].strip()  # "選択された色:" の部分を取り除く
            rgba_components = self.get_rgba(selected_color)


            if rgba_components is not None:
                # data[23][1] から data[23][4] に RGBA 成分を代入
                data[23][1] = rgba_components[0]
                data[23][2] = rgba_components[1]
                data[23][3] = rgba_components[2]
                data[23][4] = rgba_components[3]
            else:
                print("色が見つかりませんでした")



        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
            
        #subprocess.Popen(["python", "MAINSYS\PROGRAMS\pos_mover.py"])
        self.manager.current = 'timefont_screen'

    def on_back_button_press(self, instance):
        # 戻るボタンが押されたときの処理
        self.color_display.canvas.before.clear()  # 色の表示もクリア
        self.manager.current = 'timefont_screen'

    def get_color_name(self, rgba):
        min_distance = float('inf')
        closest_color = None

        for color, name in self.color_names.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgba, color))
            if distance < min_distance:
                min_distance = distance
                closest_color = name

        return closest_color if closest_color else "未知の色"

    def get_rgba(self, color_name):
        for color, name in self.color_names.items():
            if name == color_name:
                return color
        # もし color_name が見つからない場合は、適切に処理する必要があります
        return None

    color_names = {
        (220 / 255, 20 / 255, 60 / 255, 1): "クリムソンレーキ",
        (188 / 255, 63 / 255, 68 / 255, 1): "ローズマダー",
        (227 / 255, 66 / 255, 52 / 255, 1): "バーミリオンヒュー",
        (150 / 255, 111 / 255, 214 / 255, 1): "ジョーンブリヤンNo.2",
        (1, 0.76, 0.03, 1): "パーマネント イエロー ディープ",
        (1, 0.96, 0.23, 1): "パーマネント イエロー レモン",
        (0.34, 0.71, 0.47, 1): "パーマネント グリーン No.1",
        (0.29, 0.59, 0.37, 1): "パーマネント グリーン No.2",
        (0, 0.28, 0.67, 1): "コバルト グリーン",
        (0.09, 0.42, 0.28, 1): "ビリジャン ヒュー",
        (0.16, 0.2, 0.18, 1): "テール ベルト",
        (0, 0.35, 0.34, 1): "コンポーズ ブルー",
        (0.16, 0.32, 0.75, 1): "セルリアン ブルー",
        (0, 0.47, 0.73, 1): "コバルト ブルー ヒュー",
        (0.03, 0.16, 0.34, 1): "ウルトラマリン ディープ",
        (0.07, 0.13, 0.26, 1): "プルシャン ブルー",
        (0.46, 0.25, 0.29, 1): "ミネラル バイオレット",
        (0.93, 0.39, 0.25, 1): "ライト レッド",
        (0.54, 0.12, 0.22, 1): "バーント シェンナ",
        (0.54, 0.27, 0.07, 1): "バーント アンバー",
        (0.6, 0.57, 0.49, 1): "イエロー グレイ",
        (0.89, 0.79, 0.58, 1): "イエロー オーカー",
        (0.98, 0.98, 0.94, 1): "アイボリ ブラック",
        (0.93, 0.91, 0.88, 1): "チャイニーズ ホワイト"
    }



################################↓↓↓onoD_weatherset↓↓↓##############################################################



class WeatherSetScreen(Screen):
    def __init__(self, **kwargs):
        super(WeatherSetScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        coordinates_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'IDOKEIDO-UTF8.csv'))

        # coordinates_df（pd.read_csvで読み込んだデータフレーム）の列に 'latitude' と 'longitude' が存在するかを確認
        if 'latitude' in coordinates_df.columns and 'longitude' in coordinates_df.columns:
            self.selected_data = None 
            self.user_latitude = None # 緯度
            self.user_longitude = None # 経度
            self.selected_days = None # 選択した日数

            # プルダウンメニューで都道府県を選択する
            spinner_values = coordinates_df['都道府県'].tolist() 
            spinner = Spinner(text='都道府県を選択', values=spinner_values)

            # 選択した都道府県の緯度経度を変数に代入
            def on_spinner_change(spinner, text):
                self.selected_data = coordinates_df[coordinates_df['都道府県'] == text].iloc[0]
                self.user_latitude = self.selected_data['latitude']
                self.user_longitude = self.selected_data['longitude']

            spinner.bind(text=on_spinner_change)
            layout.add_widget(spinner)

            # 日数を選択する Spinner を追加
            days_spinner = Spinner(text='日数を選択', values=['1', '3'])
            days_spinner.bind(text=self.on_days_spinner_change) # on_days_spinner_changeは76行あたり
            layout.add_widget(days_spinner)

            self.errcon = 0
            def saveopt(idodata, keidodata, daydata):
                if idodata == None or keidodata == None or daydata == None :
                    if self.errcon == 0:
                        self.errcon += 1
                        print(self.errcon)
                        layout.add_widget(Label(text="エラー: 保存する地域を選択してください",color=(1,0,0,1)))
                        pass
                # CSVファイルに緯度・経度・日数を保存するメソッド
                else:
                    filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

                    with open(filename, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        data = list(reader)

                        data[5][1] = idodata
                        data[5][2] = keidodata
                        data[6][1] = daydata

                    # ここで CSV ファイルに書き込む
                    with open(filename, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerows(data)

            def re_setting(instance):
                #subprocess.Popen(["python", "MAINSYS\PROGRAMS\settings.py"])
                self.manager.current = 'set_screen'
                return

            update_button = Button(text="地域を保存", size_hint=(None, None))
            update_button.bind(on_press=lambda instance: saveopt(idodata=self.user_latitude, keidodata=self.user_longitude, daydata=self.selected_days))
            layout.add_widget(update_button)

            re_button = Button(text="戻る", size_hint=(None, None))
            re_button.bind(on_press=re_setting)
            layout.add_widget(re_button)

            self.add_widget(layout)
        else:
            return Label(text="エラー: CSVファイルに 'latitude' と 'longitude' の列がありません。")
    
    def on_days_spinner_change(self, spinner, text):
        self.selected_days = int(text) # 選択した日数を数値としてselected_days変数に代入



################################↓↓↓tukauka↓↓↓##############################################################


class AppSelectorScreen(Screen):
    def __init__(self, **kwargs):
        super(AppSelectorScreen, self).__init__(**kwargs)


        # レイアウトの作成
        self.layout = BoxLayout(orientation='horizontal', spacing=10)

        # 左側のボックスレイアウト
        self.left_layout = BoxLayout(orientation='vertical', spacing=10)

        # 中央のボックスレイアウト
        self.center_layout = BoxLayout(orientation='vertical', spacing=10)

        # 右側のボックスレイアウト
        self.right_layout = BoxLayout(orientation='vertical', spacing=10)

        self.four_layout = BoxLayout(orientation='vertical', spacing=10)

        # 画像表示用のウィジェットの作成
        self.title_label = Label(text="使用するアプリを選択")
        rebutton = Button(text='完了', size_hint=(None, None), size=(50, 50), on_press=self.rebutton)

        self.loadumu()
        self.button_make()

        # レイアウトにウィジェットを追加
        self.layout.add_widget(rebutton)
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.left_layout)
        self.layout.add_widget(self.center_layout)
        self.layout.add_widget(self.right_layout)
        #self.layout.add_widget(self.four_layout)
        self.add_widget(self.layout)
    
    def loadumu(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            self.clock_states = data[12][1]
            self.weather_states = data[12][2]
            self.schedule_states = data[12][3]
            self.add_states = data[12][4]

    def change_text_clock(self, instance):

        if self.clock_states == "off":
            self.clock_states = "on"
        elif self.clock_states == "on":
            self.clock_states = "off"
        else:
            self.clock_states = "on"
        self.button_make()
        
    def change_clock_text(self, instance):

        if self.weather_states == "off":
            self.weather_states = "on"
        elif self.weather_states == "on":
            self.weather_states = "off"
        else:
            self.weather_states = "on"
        self.button_make()

    def another_button_action(self, instance):

        if self.schedule_states == "off":
            self.schedule_states = "on"
        elif self.schedule_states == "on":
            self.schedule_states = "off"
        else:
            self.schedule_states = "on"
        self.button_make()
    
    def four_button_action(self, instance):

        if self.add_states == "off":
            self.add_states = "on"
        elif self.add_states == "on":
            self.add_states = "off"
        else:
            self.add_states = "on"
        self.button_make()

    def rebutton(self, instance):
        print("完了ボタンが押されました。")
        file_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            data[12][1] = self.clock_states
            data[12][2] = self.weather_states
            data[12][3] = self.schedule_states
            data[12][4] = self.add_states

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        self.manager.current = 'set_screen'
        

    
    def button_make(self):
        new_button1 = Button(text=f'時計:{self.clock_states}', on_press=self.change_text_clock)
        new_button2 = Button(text=f'天気:{self.weather_states}', on_press=self.change_clock_text)
        new_button3 = Button(text=f'予定:{self.schedule_states}', on_press=self.another_button_action)
        new_button4 = Button(text=f'追加:{self.add_states}', on_press=self.four_button_action)

        self.left_layout.clear_widgets()
        self.center_layout.clear_widgets()
        self.right_layout.clear_widgets()
        self.four_layout.clear_widgets()

        self.left_layout.add_widget(new_button1)
        self.center_layout.add_widget(new_button2)
        self.right_layout.add_widget(new_button3)
        #self.four_layout.add_widget(new_button4)


################################↓↓↓haikei↓↓↓##############################################################

class ColorPickerScreen(Screen):
    def __init__(self, **kwargs):
        super(ColorPickerScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 選択された色を表示するラベル
        self.color_label = Label(text="選択された色がここに表示されます", size_hint_y=None, height=44)

        # パレットのボタン作成
        palette_layout = GridLayout(cols=5, spacing=10)
        for color, name in self.color_names.items():
            button = Button(text=name, background_color=color, on_press=self.on_palette_button_press, border=(5,5,5,5), font_size='18sp', size_hint=(None, None), size=(100, 40))  # size_hintとsizeを変更
            palette_layout.add_widget(button)

        # 上部の色表示用のウィジェット
        self.color_display = BoxLayout(size_hint_y=None, height=44)

        # ボタン作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 40), on_press=self.on_confirm_button_press)
        back_button = Button(text="戻る", size_hint=(None, None), size=(100, 40), on_press=self.on_back_button_press)

        # ボタン用のレイアウト
        button_layout = BoxLayout(spacing=10)
        button_layout.add_widget(confirm_button)

        syokiflg = self.optflg(11)

        button_layout.add_widget(back_button)

        # レイアウトに要素を追加
        #layout.add_widget(self.color_label)
        layout.add_widget(self.color_display)
        layout.add_widget(palette_layout)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_palette_button_press(self, instance):
        color = instance.background_color
        selected_color = self.get_color_name(color)
        self.color_label.text = f"選択された色: {selected_color}"
        self.color_display.canvas.before.clear()  # 以前の色をクリア
        with self.color_display.canvas.before:
            Color(*color)
            Rectangle(pos=self.color_display.pos, size=self.color_display.size)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押されたときの処理
        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")


        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

            selected_color = self.color_label.text.strip().split(":")[-1].strip()  # "選択された色:" の部分を取り除く
            rgba_components = self.get_rgba(selected_color)


            if rgba_components is not None:
                # data[23][1] から data[23][4] に RGBA 成分を代入
                data[8][1] = rgba_components[0]
                data[8][2] = rgba_components[1]
                data[8][3] = rgba_components[2]
                data[8][4] = rgba_components[3]
                data[4][1] = 2
            else:
                print("色が見つかりませんでした")
        
        syokiflg=self.optflg(11)
            
        if syokiflg == "0":

            self.manager.current = 'posmover_screen'



        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
            



    def on_back_button_press(self, instance):
        # 戻るボタンが押されたときの処理
        self.color_display.canvas.before.clear()  # 色の表示もクリア

        
        self.manager.current = 'set_screen'

    def optflg(self, val):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[val][1]
        return optdata


    def get_color_name(self, rgba):
        min_distance = float('inf')
        closest_color = None

        for color, name in self.color_names.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgba, color))
            if distance < min_distance:
                min_distance = distance
                closest_color = name

        return closest_color if closest_color else "未知の色"

    def get_rgba(self, color_name):
        for color, name in self.color_names.items():
            if name == color_name:
                return color
        # もし color_name が見つからない場合は、適切に処理する必要があります
        return None

    color_names = {
        (0.929, 0.102, 0.239, 1): "赤",
        (0.945, 0.357, 0.357, 1): "Red",
        (0.973, 0.671, 0.651, 1): "Pink",
        (0.961, 0.596, 0.616, 1): "Rose pink",
        (0.961, 0.51, 0.125, 1): "Orange",
        (1, 0.847, 0, 1): "Yellow",
        (0.906, 0.733, 0.369, 1): "Honey",
        (0.698, 0.824, 0.208, 1): "黄緑",
        (0.698, 0.824, 0.208, 1): "yellow green",
        (0.686, 0.875, 0.894, 1): "Water blue",
        (0.686, 0.875, 0.894, 1): "水縹",
        (0.102, 0.267, 0.447, 1): "狼色",
        (0.396, 0.604, 0.824, 1): "Hyacinth",
        (0.443, 0.349, 0.651, 1): "Violet",
        (0.78, 0.698, 0.839, 1): "Lilac",
        (0.529, 0.361, 0.267, 1): "Brown",
        (0.416, 0.204, 0.153, 1): "錆色",
        (0.941, 0.941, 0.941, 1): "白",
        (0.941, 0.973, 1, 1): "Alice blue",
        (0.051, 0.04, 0.086, 1): "Black",
        (0.467, 0.471, 0.482, 1): "Gray",
        (0.443, 0.451, 0.459, 1): "灰色"
    }





class FontScreen(Screen):
    def __init__(self, **kwargs):
        super(FontScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))


        fontcolor0,fontcolor1,fontcolor2,fontcolor3,font = self.load_settings_from_csv()
        fontcolor0 = float(fontcolor0)
        fontcolor1 = float(fontcolor1)
        fontcolor2 = float(fontcolor2)
        fontcolor3 = float(fontcolor3)
        
        self.font_path = font

        # "Hello World" 表示用のラベル
        self.hello_label = Label(text="A/a/ひら/漢字/カナ",font_name=font, font_size='40sp', size_hint=(1, 0.6),color=[fontcolor0,fontcolor1,fontcolor2,fontcolor3])
        self.layout.add_widget(self.hello_label)

        # フォント変更ボタン
        font_button = Button(text='フォント変更', on_press=self.show_font_chooser, size_hint=(1, 0.2))
        self.layout.add_widget(font_button)

        # 色変更ボタン
        color_button = Button(text='色変更', on_press=self.show_color_picker, size_hint=(1, 0.2))
        self.layout.add_widget(color_button)

        # 色とフォントの初期設定
        fontcolor0,fontcolor1,fontcolor2,fontcolor3,font = self.load_settings_from_csv()
        self.font_path = font
        # 次へボタン
        next_button = Button(text='確定', on_press=self.next_page, size_hint=(1, 0.1))
        self.layout.add_widget(next_button)

        # 戻るボタン
        prev_button = Button(text='戻る', on_press=self.prev_page, size_hint=(1, 0.1))
        self.layout.add_widget(prev_button)

        self.add_widget(self.layout)



    def load_settings_from_csv(self):
        # settings.csvから色とフォント情報を読み取り、ラベルに設定
        csv_path = os.path.join(os.path.dirname(__file__),"onoD_opt.csv")
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            fontcolor0 = data[7][1]
            fontcolor1 = data[7][2]
            fontcolor2 = data[7][3]
            fontcolor3 = data[7][4]
            #iro 

            #フォント
            
            font = data[27][1]

        return fontcolor0,fontcolor1,fontcolor2,fontcolor3,font


    def save_settings_to_csv(self):
        # settings.csvに色とフォント情報を保存
        color_values, font_name = self.get_settings_data()

        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        # 絶対パスを相対パスに変換
        font_path_relative = os.path.relpath(font_name, start=os.getcwd())

        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            data[27][1] = font_path_relative  # Save the relative font path
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def get_settings_data(self):
        # 現在の色とフォント情報をリストで返す
        color_values = [round(value, 3) for value in self.hello_label.color]
        # 色情報を4つの要素に固定
        while len(color_values) < 4:
            color_values.append(1.0)  # 不足している場合は1.0で埋める
        font_name = self.hello_label.font_name
        return color_values, font_name

    def show_font_chooser(self, instance):
        popup = Popup(title='フォントを選択', size_hint=(0.9, 0.9))

        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path=os.path.dirname(__file__), filters=['*.ttf'])
        content.add_widget(file_chooser)

        def set_font(selected_font):
            self.hello_label.font_name = selected_font
            popup.dismiss()

        button_layout = BoxLayout(size_hint_y=None, height=40)
        button_layout.add_widget(Button(text='キャンセル', on_press=popup.dismiss))
        button_layout.add_widget(Button(text='選択', on_press=lambda instance: set_font(file_chooser.selection[0])))

        content.add_widget(button_layout)
        popup.content = content
        popup.open()

    def show_color_picker(self, instance):
        self.manager.current = 'fontcolor_screen'


    def next_page(self, instance):
        # 確定ボタンが押されたときの処理
        # 色とフォント情報をCSVに保存（上書き）
        self.save_settings_to_csv()
        self.manager.current = 'set_screen'
        pass

    def prev_page(self, instance):
        # 戻るボタンが押されたときの処理
        self.manager.current = 'set_screen'
        pass

    def update_label_color(self, rgba_components):
        # ラベルの色を更新
        self.hello_label.color = rgba_components


######################fontset#################################################################

class FontColorScreen(Screen):
    def __init__(self, **kwargs):
        super(FontColorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 選択された色を表示するラベル
        self.color_label = Label(text="選択された色がここに表示されます", size_hint_y=None, height=44)

        # パレットのボタン作成
        palette_layout = GridLayout(cols=5, spacing=10)
        for color, name in self.color_names.items():
            button = Button(text=name, background_color=color, on_press=self.on_palette_button_press, border=(5,5,5,5), font_size='18sp', size_hint=(None, None), size=(100, 40))  # size_hintとsizeを変更
            palette_layout.add_widget(button)

        # 上部の色表示用のウィジェット
        self.color_display = BoxLayout(size_hint_y=None, height=44)

        # ボタン作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 40), on_press=self.on_confirm_button_press)
        back_button = Button(text="戻る", size_hint=(None, None), size=(100, 40), on_press=self.on_back_button_press)

        # ボタン用のレイアウト
        button_layout = BoxLayout(spacing=10)
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(back_button)

        # レイアウトに要素を追加
        layout.add_widget(self.color_display)
        layout.add_widget(palette_layout)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_palette_button_press(self, instance):
        color = instance.background_color
        selected_color = self.get_color_name(color)
        self.color_label.text = f"選択された色: {selected_color}"
        self.color_display.canvas.before.clear()  # 以前の色をクリア
        with self.color_display.canvas.before:
            Color(*color)
            Rectangle(pos=self.color_display.pos, size=self.color_display.size)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押されたときの処理
        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

            selected_color = self.color_label.text.strip().split(":")[-1].strip()  # "選択された色:" の部分を取り除く
            rgba_components = self.get_rgba(selected_color)

            if rgba_components is not None:
                # data[23][1] から data[23][4] に RGBA 成分を代入
                data[7][1] = rgba_components[0]
                data[7][2] = rgba_components[1]
                data[7][3] = rgba_components[2]
                data[7][4] = rgba_components[3]

                # FontScreen に通知してラベルの色を更新
                font_screen = self.manager.get_screen('font_screen')
                font_screen.update_label_color(rgba_components)

            else:
                print("色が見つかりませんでした")

        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        self.manager.current = 'font_screen'

    def on_back_button_press(self, instance):
        # 戻るボタンが押されたときの処理
        self.color_display.canvas.before.clear()  # 色の表示もクリア
        self.manager.current = 'font_screen'

    def get_color_name(self, rgba):
        min_distance = float('inf')
        closest_color = None

        for color, name in self.color_names.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgba, color))
            if distance < min_distance:
                min_distance = distance
                closest_color = name

        return closest_color if closest_color else "未知の色"

    def get_rgba(self, color_name):
        for color, name in self.color_names.items():
            if name == color_name:
                return color
        # もし color_name が見つからない場合は、適切に処理する必要があります
        return None

    color_names = {
        (0.929, 0.102, 0.239, 1): "赤",
        (0.945, 0.357, 0.357, 1): "Red",
        (0.973, 0.671, 0.651, 1): "Pink",
        (0.961, 0.596, 0.616, 1): "Rose pink",
        (0.961, 0.51, 0.125, 1): "Orange",
        (1, 0.847, 0, 1): "Yellow",
        (0.906, 0.733, 0.369, 1): "Honey",
        (0.698, 0.824, 0.208, 1): "黄緑",
        (0.698, 0.824, 0.208, 1): "yellow green",
        (0.686, 0.875, 0.894, 1): "Water blue",
        (0.686, 0.875, 0.894, 1): "水縹",
        (0.102, 0.267, 0.447, 1): "狼色",
        (0.396, 0.604, 0.824, 1): "Hyacinth",
        (0.443, 0.349, 0.651, 1): "Violet",
        (0.78, 0.698, 0.839, 1): "Lilac",
        (0.529, 0.361, 0.267, 1): "Brown",
        (0.416, 0.204, 0.153, 1): "錆色",
        (0.941, 0.941, 0.941, 1): "白",
        (0.941, 0.973, 1, 1): "Alice blue",
        (0.051, 0.04, 0.086, 1): "Black",
        (0.467, 0.471, 0.482, 1): "Gray",
        (0.443, 0.451, 0.459, 1): "灰色"
    }



################################↓↓↓app↓↓↓##############################################################



class AnalogClockScreen(Screen):
    def build(self):
        # ウィジェットのサイズを10%縮小
        

        return 

   

################################↓↓↓app↓↓↓##############################################################
    


class MainApp(App):
    def build(self):
        screen_manager = ScreenManager()

        syoki_screen = SyokiScreen(name='syoki_screen')
        background_screen = BackgroundColorScreen(name='background_screen')
        posmover_screen = PosMoverScreen(name='posmover_screen')
        maindisplay_screen = MainDisplayScreen(name='maindisplay_screen')
        set_screen = SetScreen(name="set_screen")
        clockselect_screen = ClockSelectScreen(name="clockselect_screen")
        appselector_screen = AppSelectorScreen(name='appselector_screen')
        timefont_screen = TimeFontScreen(name='timefont_screen')
        timecolor_screen = TimeClolrScreen(name='timecolor_screen')
        weather_screen = WeatherSetScreen(name='weatherset_screen')
        colorpicker_screen = ColorPickerScreen(name='colorpicker_screen')
        font_screen = FontScreen(name='font_screen')
        fontcolor_screen = FontColorScreen(name='fontcolor_screen')
        analogclock_screen = AnalogClockScreen(name='analogclock_screen')
        bgimage_screen = Test(name='bgimage_screen')

        screen_manager.add_widget(syoki_screen)
        screen_manager.add_widget(background_screen)
        screen_manager.add_widget(posmover_screen)
        screen_manager.add_widget(maindisplay_screen)
        screen_manager.add_widget(set_screen)
        screen_manager.add_widget(clockselect_screen)
        screen_manager.add_widget(timefont_screen)
        screen_manager.add_widget(timecolor_screen)
        screen_manager.add_widget(weather_screen)
        screen_manager.add_widget(appselector_screen)
        screen_manager.add_widget(colorpicker_screen)
        screen_manager.add_widget(font_screen)
        screen_manager.add_widget(fontcolor_screen)
        screen_manager.add_widget(analogclock_screen)
        screen_manager.add_widget(bgimage_screen)



        return screen_manager


if __name__ == "__main__":
    MainApp().run()
