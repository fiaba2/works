from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
import pyrebase
from firebase_config import firebaseConfig

# Размер окна (не нужен для Android)
Window.size = (400, 700)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class TaskScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.title_label = MDLabel(
            text="📋 ЗАДАЧИ",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 0, 1),
            font_style="H5"
        )

        self.task_input = MDTextField(
            hint_text="Введите новую задачу",
            mode="rectangle",
            line_color_normal=(1, 1, 0, 1),
            line_color_focus=(1, 1, 0, 1),
            text_color=(1, 1, 1, 1),
        )

        self.add_button = MDRaisedButton(
            text="Добавить задачу",
            md_bg_color=(1, 1, 0, 1),
            text_color=(0, 0, 0, 1),
            on_release=self.add_task,
        )

        self.task_list = MDList()
        self.scroll = MDScrollView()
        self.scroll.add_widget(self.task_list)

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.task_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

        Clock.schedule_once(lambda dt: self.load_tasks(), 1)

    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            data = {"text": task_text, "done": False}
            db.child("tasks").push(data)
            self.task_input.text = ""
            self.load_tasks()

    def load_tasks(self):
        self.task_list.clear_widgets()
        tasks = db.child("tasks").get()
        if tasks.each():
            for task in tasks.each():
                task_data = task.val()
                task_key = task.key()
                item_text = f"✅ {task_data['text']}" if task_data['done'] else task_data['text']
                item = OneLineListItem(
                    text=item_text,
                    on_release=lambda x, k=task_key, d=task_data: self.toggle_task(k, d),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    bg_color=(0.1, 0.1, 0.1, 1)
                )
                self.task_list.add_widget(item)

    def toggle_task(self, key, data):
        data['done'] = not data['done']
        db.child("tasks").child(key).update(data)
        self.load_tasks()

class TaskApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        sm = ScreenManager()
        sm.add_widget(TaskScreen(name='tasks'))
        return sm

if __name__ == '__main__':
    TaskApp().run()
