from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
import csv
import os
from kivy.core.window import Window
import subprocess
import japanize_kivy

class BackgroundChangerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ラベル（背景色変更用）
        label_background = Label(text="背景色変更")
        self.label_background = label_background

        # カラーピッカー（背景色用）
        self.background_color_picker = ColorPicker()
        self.background_color_picker.bind(color=self.on_background_color)

        # ボタン
        button = Button(text="背景色を変更", on_press=self.change_background_color)

        # レイアウトにウィジェットを追加
        layout.add_widget(label_background)
        layout.add_widget(self.background_color_picker)
        layout.add_widget(button)

        # ウィンドウサイズ変更時にオブジェクトを調整
        Window.bind(on_resize=self.on_window_resize)

        return layout

    def on_window_resize(self, instance, width, height):
        # ウィンドウサイズが変更されたときに呼ばれるメソッド
        # フォントサイズを調整
        font_size = int(0.04 * height)  # 画面高さの4%をフォントサイズとする
        self.label_background.font_size = font_size

    def on_background_color(self, instance, value):
        # ラベルの背景色を変更
        self.label_background.background_color = value

    def change_background_color(self, instance):
        # カラーピッカーの選択色をCSVファイルに保存
        background_color = self.background_color_picker.color

        # 背景色のRGBA値を取得
        background_red, background_green, background_blue, background_alpha = background_color



        print("確定ボタンが押されました。")
         # ファイルの読み込みと書き込みはここで行います
        file_path =  os.path.join(os.path.dirname(__file__),"onoD_opt.csv")
        

        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)


        data[7][1] = background_red
        data[7][2] = background_green
        data[7][3] = background_blue
        data[7][4] = background_alpha

       # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)



if __name__ == '__main__':
    BackgroundChangerApp().run()
