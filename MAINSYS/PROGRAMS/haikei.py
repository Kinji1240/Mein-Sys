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
        file_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)


        data[8][1] = background_red
        data[8][2] = background_green
        data[8][3] = background_blue
        data[8][4] = background_alpha
        data[4][1] = 2
       # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # 保存後に別のPythonスクリプトを実行
        script_path = os.path.join(os.path.dirname(__file__), "pos_mover.py")
            
        if os.path.exists(script_path):
            setflg_row = 10  # 設定画面遷移時に使用するフラグの保存行番号
            syokiflg_row = 11 # 初期設定時に使用するフラグの保存行番号

            setflg = self.optflg(setflg_row)
            syokiflg = self.optflg(syokiflg_row)
            if syokiflg == '0' and setflg == '0':
                subprocess.Popen(["python", "MAINSYS\PROGRAMS\pos_mover.py"])
            elif syokiflg == '1' and setflg == '1':
                pass
            else :
                subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
            App.get_running_app().stop()
        else:
            print(f"スクリプト '{script_path}' は存在しません。")
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])


    def optflg(self,val):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[val][1]
        return optdata
    
    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
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

        return 


if __name__ == '__main__':
    BackgroundChangerApp().run()
