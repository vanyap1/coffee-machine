from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class DrinkItemMenu(Popup):
    def __init__(self, image_source, **kwargs):
        super(DrinkItemMenu, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (800, 800)
        self.title = 'Image Popup'

        layout = BoxLayout(orientation='vertical')
        self.image = Image(source=image_source, size_hint=(1, 0.8))
        layout.add_widget(self.image)

        button_layout = BoxLayout(size_hint=(1, 0.2))
        close_button = Button(text='Close', on_release=self.dismiss)
        button_layout.add_widget(close_button)
        layout.add_widget(button_layout)

        self.content = layout

    def update_image(self, image_source):
        self.image.source = image_source