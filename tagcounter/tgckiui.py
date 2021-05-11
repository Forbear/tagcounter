from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from .tgc import TagCounter


SIZE = (1200, 600)


class TagCounterBox(FloatLayout):
    arguments = ObjectProperty(None)
    output = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = SIZE
        self.build_buttons()
        self.arguments.pos = (0, self.height - self.arguments.height)
        output_size_y = self.height - 30 - self.arguments.height
        self.output.size[1] = output_size_y

    def build_buttons(self):
        commands = TagCounter.get_commands()
        button_size = (self.width / len(commands), 30)
        button_pos_y = self.height - self.arguments.height - button_size[1]
        for i, c in enumerate(commands):
            btn = Button(text=f"{c}", size_hint=(None, None), size=button_size, pos=(button_size[0] * i, button_pos_y))
            btn.bind(on_press=self.btn_click)
            self.add_widget(btn)

    def btn_click(self, instance):
        args = [instance.text, *self.arguments.text.split(' ')]
        c = TagCounter(args)
        self.output.text = str(c.execute())


class TagCounterApp(App):
    def build(self):
        Window.size = SIZE
        return TagCounterBox()
