import os
import cv2
import numpy as np
import csv
import subprocess
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import japanize_kivy



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
            im = cv2.rectangle(im, (2, 2), (im.shape[1]-2, im.shape[0]-2), (255, 255, 0), 10)

        buf = cv2.flip(im, 0)
        image_texture = Texture.create(size=(im.shape[1], im.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        return image_texture

    def square_image(self, img):
        h, w = img.shape[:2]
        if h > w:
            x = int((h-w)/2)
            img = img[x:x + w, :, :]
        elif h < w:
            x = int((w - h) / 2)
            img = img[:, x:x + h, :]

        return img

    def adjust(self, img, alpha=1.0, beta=0.0):
        dst = alpha * img + beta
        return np.clip(dst, 0, 255).astype(np.uint8)

class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        image_dir = "MAINSYS\IMAGE"
        self.orientation = 'vertical'
        self.image_name = ""
        self.current_image_index = 0

        self.image = Image(size_hint=(1, 0.5))
        self.add_widget(self.image)

        sc_view = ScrollView(size_hint=(1, None), size=(self.width, self.height*4))
        box = GridLayout(cols=5, spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box = self.image_load(image_dir, box)
        sc_view.add_widget(box)
        self.add_widget(sc_view)

        # ボタンを横に並べるBoxLayoutを作成
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # 確定ボタンに変更
        self.confirm_button = Button(text="確定", size_hint=(0.5, None), height=50)
        self.confirm_button.bind(on_press=self.confirm_action)

        self.prev_button = Button(text="戻る", size_hint=(0.5, None), height=50)
        self.prev_button.bind(on_press=self.prev_image)

        button_layout.add_widget(self.prev_button)
        button_layout.add_widget(self.confirm_button)

        self.add_widget(button_layout)

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
            if syokiflg == '0' and setflg == '0':
                print(f"Image confirmed: {self.image_name}")
                #csvに保存
                data[14][1]= self.image_name
                data[4][1] = 1
                with open(filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
                    print("保存されました！")

                # "haikeigazou.py" を実行
                subprocess.Popen(["python", "MAINSYS\PROGRAMS\pos_mover.py"])
                App.get_running_app().stop()
            elif syokiflg == '1' and setflg == '1':
                print(f"Image confirmed: {self.image_name}")
                # 何らかの処理を追加する場合はここに記述
                #csvに保存
                data[14][1]= self.image_name
                data[4][1] = 1
                with open(filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
                    print("保存されました！")
                App.get_running_app().stop()
                pass
            else:
                subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
                App.get_running_app().stop()

    def prev_image(self, instance):
        # 戻るボタンが押下されたときの処理
        syokiflg, setflg = self.optflg()
        if syokiflg == '0' and setflg == '0':
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\syoki.py"])
        elif syokiflg == '1' and setflg == '1':
            pass
        else:
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
            App.get_running_app().stop()

    def optflg(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            syokiopt = data[11][1]
            setopt = data[10][1]

        return syokiopt, setopt

    def setflg(self, flgval):   # CSVファイルに設定用フラグを保存するメソッド
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

class SampleApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    SampleApp().run()
