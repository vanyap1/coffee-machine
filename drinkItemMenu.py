from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class DrinkItemMenu(Popup):
    def __init__(self, image_source, **kwargs):
        super(DrinkItemMenu, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (800, 800)
        self.title = 'Якийсь кавіль'

        layout = BoxLayout(orientation='vertical')
        self.image = Image(source=image_source, size_hint=(1, 0.8))
        layout.add_widget(self.image)

        button_layout = BoxLayout(size_hint=(1, 0.2))
        sugarIncr = Button(text='цукор +',size_hint=(None, None), size=(104, 100), background_normal='images/empty_btn.png')
        sugarDecr = Button(text='цукор +',size_hint=(None, None), size=(104, 100), background_normal='images/empty_btn.png')
        info = Button(text='' ,size_hint=(None, None), size=(104, 100), background_normal='images/info.png')
        run = Button(text='',size_hint=(None, None), size=(230, 100), background_normal='images/main_runbutton.png')
        close_button = Button(text='', size_hint=(None, None), size=(190, 100), background_normal='images/cancel.png', on_release=self.dismiss)
        
        button_layout.add_widget(sugarDecr)
        button_layout.add_widget(sugarIncr)
        button_layout.add_widget(info)
        button_layout.add_widget(run)
        button_layout.add_widget(close_button)
        
        
        
        layout.add_widget(button_layout)

        self.content = layout

    def update_image(self, image_source):
        self.image.source = image_source