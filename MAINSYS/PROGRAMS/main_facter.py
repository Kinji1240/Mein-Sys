import csv
import os
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from onoD_wth_test import WeatherApp
from onoD_calendar import CalendarApp
from onoD_clock import ClockApp
from kivy.core.window import Window
import subprocess

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

class MainDisplayApp(App):
    
    

    def build(self):
        # レイアウトのインスタンスを作成
        self.layout = FloatLayout()
        
        self.background_color = [0, 0, 0, 0]  # デフォルトは黒い背景

        bgopt = self.loadhaikei()
        print("bgopt:", bgopt)
        if bgopt == "2":
            print("color_settings.csv を使用します")
            background_color = self.get_background_color("MAINSYS\CSV\color_settings.csv")
            background_image_path = None

        else:
            print("selected_backgrounds.csv を使用します")
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
        weather_app = WeatherApp()
        calender_app = CalendarApp()
        clock_app = ClockApp()

        # 各アプリのレイアウトを作成
        weather_layout = weather_app.build()
        calendar_layout = calender_app.build()
        clock_layout = clock_app.build()

        # 時間アプリの座標を読み込み
        posrow = 0
        x, y = self.load_button_position(posrow)
        clock_layout.pos = (x, y)

        # 天気アプリの座標を読み込み
        posrow = 1 
        x, y = self.load_button_position(posrow)
        weather_layout.pos = (x, y)

        # 予定アプリの座標を読み込み
        posrow = 2
        x, y = self.load_button_position(posrow)
        calendar_layout.pos = (x, y)


        # 設定ボタンの生成
        button = Button(text="設定", size_hint=(0.1, 0.15), pos_hint={'top': 1})
        button.bind(on_press=self.on_settings_button_press)
        
        self.layout.add_widget(button)
        self.layout.add_widget(weather_layout)
        self.layout.add_widget(calendar_layout)
        self.layout.add_widget(clock_layout)

        return self.layout
    

    # 設定ボタンが押されたときの処理
    def on_settings_button_press(self, instance):
        subprocess.Popen(["python", "MAINSYS\PROGRAMS\settings.py"])#subprocessじゃないと画面が消えなかったんだ...
        App.get_running_app().stop()

    def get_background_settings(self):
         # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
        background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
        
        return (1,1,1,1), background_image_path


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
                next(reader)  # ヘッダー行をスキップ
                row = next(reader, None)
                if row:
                    background_color = (float(row[0]), float(row[1]), float(row[2]), float(row[3]))
                else:
                    background_color = (1, 1, 1, 1)  # デフォルト値
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color
    
    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)


        

    def update_background_size(self,v,a):
        print("on_sizeメソッドが呼ばれました。")
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size

        # 背景画像のサイズも更新
        if hasattr(self, 'background_image'):
            self.background_image.size = self.layout.size
    
    # CSVファイルからアプリの座標を取得するメソッド
    def load_button_position(self,row):
        filename = 'MAINSYS\CSV\move.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            button_pos_x = data[row][0]
            button_pos_x = float(button_pos_x)
            button_pos_x = button_pos_x - 223.0

            button_pos_y = data[row][1]
            button_pos_y = float(button_pos_y)
            button_pos_y = button_pos_y - 132.0

        return button_pos_x,button_pos_y
    
    def loadhaikei(self):
        filename = 'MAINSYS\CSV\onoD_opt.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata

if __name__ == '__main__':
    MainDisplayApp().run() 
