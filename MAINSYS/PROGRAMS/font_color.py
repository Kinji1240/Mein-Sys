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

        # ラベル（文字色変更用）
        label_text = Label(text="文字色変更")
        self.label_text = label_text

        # カラーピッカー（文字色用）
        self.text_color_picker = ColorPicker()
        self.text_color_picker.bind(color=self.on_text_color)

        # ボタン
        button = Button(text="文字色を変更", on_press=self.change_text_color)

        # レイアウトにウィジェットを追加
        layout.add_widget(label_text)
        layout.add_widget(self.text_color_picker)
        layout.add_widget(button)

        # ウィンドウサイズ変更時にオブジェクトを調整
        Window.bind(on_resize=self.on_window_resize)

        return layout

    def on_window_resize(self, instance, width, height):
        # ウィンドウサイズが変更されたときに呼ばれるメソッド
        # フォントサイズを調整
        font_size = int(0.04 * height)  # 画面高さの4%をフォントサイズとする
        self.label_text.font_size = font_size

    def on_text_color(self, instance, value):
        # ラベルの文字色を変更
        self.label_text.color = value

    def change_text_color(self, instance):
        # カラーピッカーの選択色をCSVファイルに保存
        text_color = self.text_color_picker.color

        # フォント色のRGBA値を取得
        text_red, text_green, text_blue, text_alpha = text_color


        print("確定ボタンが押されました。")
         # ファイルの読み込みと書き込みはここで行います
        file_path = os.path.join(os.path.dirname(__file__),"onoD_opt.csv")
        
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        
        # 必要な部分を変更
        data[8][1] = text_red # watchを文字列に変換して代入
        data[8][2] = text_green
        data[8][3] = text_blue
        data[8][4] = text_alpha
        

        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
        

 


if __name__ == '__main__':
    BackgroundChangerApp().run()
