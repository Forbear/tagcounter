from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from .tgc import TagCounter


SIZE = (1200, 600)


class TagCounterBox(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = SIZE
        self.arguments = TextInput(text='Paste arguments here', size_hint=(1, None), font_size=15, height=35)
        self.arguments.pos = (0, self.size[1] - self.arguments.height)
        self.add_widget(self.arguments)
        self.output = TextInput(text='Output field.', size_hint=(1, None), font_size=15)
        output_size_y = self.height - 30 - self.arguments.height
        self.output.size = (SIZE[0], output_size_y)
        self.add_widget(self.output)
        self.build_buttons()

    def build_buttons(self):
        commands = TagCounter.get_commands()
        button_size = (self.width / len(commands), 30)
        button_pos_y = self.size[1] - self.arguments.height - button_size[1]
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
