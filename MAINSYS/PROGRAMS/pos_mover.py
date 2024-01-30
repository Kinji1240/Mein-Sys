from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import csv
import os
import subprocess
import time
import japanize_kivy
from kivy.core.window import Window

## インチあたりのピクセル数
pixels_per_inch = 96

# 縦8cm、横15cmのサイズをピクセルに変換
width_cm = 15
height_cm = 8
width_pixels = int(width_cm * pixels_per_inch / 2.54)
height_pixels = int(height_cm * pixels_per_inch / 2.54)

# ウィンドウサイズの指定
Window.size = (width_pixels, height_pixels)

class RunningTask:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            print("タスクが実行中...")
            time.sleep(1)

    def stop(self):
        self.running = False

class ButtonMoverApp(App):
    def build(self):
        # ウィンドウを作成
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

        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.on_size)

        return self.layout

    def on_button_move(self, instance, touch):
        # ボタンがタッチされ、移動したときに呼ばれるメソッド
        if instance.collide_point(*touch.pos):
            instance.pos = (touch.x - instance.width / 2, touch.y - instance.height / 2)

    def on_stop(self):
        # アプリケーションが終了するときに呼ばれるメソッド
        self.save_button_positions()

    def get_background_settings(self,bgopt):
        # selected_backgrounds.csvから背景画像のパスを取得
        if bgopt == 1:
            background_image_path = self.get_background_image_path("MAINSYS/CSV/selected_backgrounds.csv")
            return (1, 1, 1, 1), background_image_path
                
        else:
        # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
            background_color = self.get_background_color("MAINSYS\CSV\color_settings.csv")
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

    def save_button_positions(self):
        # 各ボタンの座標をCSVファイルに保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            i = 1
            for button in self.buttons:
                button_pos = button.pos
                x = button_pos[0]
                y = button_pos[1]

                data[16 + i][1] = x
                data[16 + i][2] = y
                i +=  1
        # 新しいCSVファイルに書き出す
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押下されたときの処理
        syokiflg,setflg = self.optflg()
        if syokiflg == '0' and setflg == '0':
            self.save_button_positions()
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\main_facter.py"])
        elif syokiflg == '1' and setflg == '1':
            pass
        else :
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
        App.get_running_app().stop()

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


if __name__ == '__main__':
    # アプリケーションを起動
    ButtonMoverApp().run()
