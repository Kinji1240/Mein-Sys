from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
import japanize_kivy
import os
import csv
import subprocess

class ColorPickerApp(App):
    def build(self):
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

        return layout

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
        
            
        subprocess.Popen(["python", "MAINSYS\PROGRAMS\pos_mover.py"])
        App.get_running_app().stop()

    def on_back_button_press(self, instance):
        # 戻るボタンが押されたときの処理
        self.color_display.canvas.before.clear()  # 色の表示もクリア
        App.get_running_app().stop()

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

if __name__ == '__main__':
    ColorPickerApp().run()
