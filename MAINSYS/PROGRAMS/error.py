from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader
import japanize_kivy
import csv
import os

class ErrorApp(App):
    def build(self):
        # エラーの条件を設定
        error_condition = True

        if error_condition:
            # エラーメッセージを生成
            text = self.load_error()
            error_message = f"{text}エラーが発生しました。"

            # エラー画面を表示するレイアウト
            layout = BoxLayout(orientation='vertical')

            # キャンバスを更新するコールバックを設定
            layout.bind(size=self.update_canvas)

            error_label = Label(text=f'エラーメッセージ: {error_message}', font_size='32sp', color=(1, 0, 0, 1), bold=True)

            # レイアウトにウィジェットを追加
            layout.add_widget(error_label)

            # 初回描画
            self.update_canvas(layout, layout.size)

            self.sound = SoundLoader.load('MAINSYS\AUDIO\六甲おろし.mp3')  # ここに音楽ファイルのパスを指定
            self.play_music()  # アプリ起動時に自動で音楽を再生

            return layout
        else:
            # エラーが発生しなかった場合の処理
            return Label(text='正常な画面です。', font_size='20sp', color=(1, 0, 0, 1), bold=True)

    def update_canvas(self, layout, size):
        # 画面全体を縦向きのトラ柄に描画
        with layout.canvas.before:
            layout.canvas.before.clear()
            stripe_width = 100
            for i in range(0, int(size[0]), stripe_width):
                Color(1, 1, 0, 1)  # 黄色の背景
                Rectangle(pos=(layout.x + i, layout.y), size=(stripe_width, size[1]))

                Color(0, 0, 0, 1)  # 黒い縞模様
                Rectangle(pos=(layout.x + i, layout.y), size=(stripe_width / 2, size[1]))

    def play_music(self, *args):
        if self.sound:
            self.sound.play()
            self.sound.bind(on_stop=self.play_music)  # 音楽が停止したら再度再生
    
    def load_error(self):
        filename = os.path.join(os.path.dirname(__file__),"onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            self.clock_states = data[12][1]
            
if __name__ == '__main__':
    ErrorApp().run()