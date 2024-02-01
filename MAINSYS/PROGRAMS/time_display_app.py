# time_display_app.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.colorpicker import ColorPicker
from kivy.clock import Clock
import time
import csv
import os
import japanize_kivy
import subprocess

class MovableBoxLayout(BoxLayout):
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)

class TimeDisplayApp(App):
    def build(self):
        self.layout = MovableBoxLayout(orientation='vertical', size_hint=(1, 1))

        # 時刻表示用のラベル
        self.time_label = Label(text=self.get_japanese_time(), font_size='40sp', size_hint=(1, 0.6))
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
        self.load_settings_from_csv()

        # 確定ボタン
        next_button = Button(text='確定', on_press=self.next_page, size_hint=(1, 0.1))
        self.layout.add_widget(next_button)

        # 戻るボタン
        prev_button = Button(text='戻る', on_press=self.prev_page, size_hint=(1, 0.1))
        self.layout.add_widget(prev_button)

        return self.layout

    def update_time(self, dt):
        # 時間を更新する
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        # 現在時刻を取得する
        return time.strftime("%H:%M:%S", time.localtime())

    def save_to_csv(self, data, csv_filename):
        # ファイルが存在しなければ新規作成、存在すれば上書き
        csv_directory = 'MAINSYS/CSV'
        os.makedirs(csv_directory, exist_ok=True)
        csv_path = os.path.join(csv_directory, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(data)

    def load_settings_from_csv(self):
        # settings.csvから色とフォント情報を読み取り、ラベルに設定
        csv_path = os.path.join('MAINSYS', 'CSV', 'settings.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                row = next(csv_reader, None)  # Read the first row
                if row:
                    color_values = [float(value) for value in row]
                    # 色情報を4つの要素に固定
                    while len(color_values) < 4:
                        color_values.append(1.0)  # 不足している場合は1.0で埋める
                    self.time_label.color = color_values

                    row = next(csv_reader, None)  # Read the second row
                    if row:
                        self.time_label.font_name = row[0]

    def save_settings_to_csv(self):
        # settings.csvに色とフォント情報を保存
        color_values, font_name = self.get_settings_data()

        csv_path = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        # 絶対パスを相対パスに変換
        font_path_relative = os.path.relpath(font_name, start=os.getcwd())

        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            data[23][1] = color_values
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
        file_chooser = FileChooserListView(path='MAINSYS/FONT', filters=['*.ttf'])
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
        popup = Popup(title='色を選択', size_hint=(0.9, 0.9))

        color_picker = ColorPicker()
        content = BoxLayout(orientation='vertical')
        content.add_widget(color_picker)

        def set_color(selected_color):
            self.time_label.color = selected_color
            popup.dismiss()



        button_layout = BoxLayout(size_hint_y=None, height=40)
        button_layout.add_widget(Button(text='キャンセル', on_press=popup.dismiss))
        button_layout.add_widget(Button(text='選択', on_press=lambda instance: set_color(color_picker.color)))

        content.add_widget(button_layout)
        popup.content = content
        popup.open()

    def next_page(self, instance):
        self.setflg(2)
        # ここに確定ボタンが押されたときの処理を書く
        # subprocessを使用してsettings.pyを実行する
        # 色とフォント情報をCSVに保存（上書き）
        self.save_settings_to_csv()


        # オプションで、新しいスクリプトを開始した後に現在のKivyアプリを終了することができます
        App.get_running_app().stop()
        pass
        
    def prev_page(self, instance):
        # ここに戻るボタンが押されたときの処理を書く
        # subprocessを使用してsettings.pyを実行する
        

        # オプションで、新しいスクリプトを開始した後に現在のKivyアプリを終了することができます
        App.get_running_app().stop()
        pass

    def setflg(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = 'MAINSYS\CSV\onoD_opt.csv'
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
    


if __name__ == '__main__':
    TimeDisplayApp().run()
