import subprocess

import time
import shlex
import pty
import os, socket, re
import random
import json
from urllib import request
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen , ScreenManager
from threading import Thread
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from datetime import datetime, date, timedelta
from collections import namedtuple
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.core.window import Window
from kivy.factory import Factory

from remoteCtrlServer.httpserver import start_server_in_thread
from remoteCtrlServer.udpService import UdpAsyncClient

from backgroundServices.backgroundProcessor import BackgroundWorker


remCtrlPort = 8080

Builder.load_file('kv/bottomBar.kv')

Builder.load_file('kv/popUp.kv')

class udpReportService():
    ip = '192.168.1.255'
    rx_port = 5006
    tx_port = 55006

class BottomBar(BoxLayout):
    def show_menu(self):
        menu = PopupMenu()
        popup = Popup(content=menu, size_hint=(None, None), size=(430, 400))
        popup.open()

class PopupMenu(BoxLayout):
    def save_parameters(self):
        # Додайте логіку для збереження параметрів
        print("Parameters saved")
        self.dismiss()

    def dismiss(self):
        self.parent.parent.dismiss()

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.backProc = BackgroundWorker()
        self.backProc.startProc()
        
        
        self.background_image = Image(source='images/bg_d.jpg', size=self.size)
        self.add_widget(self.background_image)
        
        self.bottom_bar = BottomBar()
        self.add_widget(self.bottom_bar)

        

        ## Server start
        #self.server, self.server_thread = start_server_in_thread(remCtrlPort, self.remCtrlCB, self)
        #self.udpClient = UdpAsyncClient(self)
        #self.udpClient.startListener(udpReportService.rx_port, self.serverUdpIncomingData)
        
        Clock.schedule_interval(lambda dt: self.update_time(), 1)

    
        self.clock = Label(text='[color=ffffff]22:30:38[/color]', markup = True, font_size=100, pos=(700, 500) , font_name='fonts/hemi_head_bd_it.ttf')
        self.add_widget(self.clock)

        


        

    def on_button_release(self, message):
        self.udpClient.send_data(message, udpReportService.ip, udpReportService.tx_port)



    def update_time(self):
        #print(self.gpio.pinRead(self.jigSw))
        

        self.clock.text='[color=0099ff]'+datetime.now().strftime('%H:%M:%S')+'[/color]'
        #self.udpClient.send_text("Hello", udpReportService.ip, udpReportService.port)
        #print(self.backProc.getStatus())

    def serverUdpIncomingData(self, data):
        try:
            #gtaData = data.split(":")
            #gtaSpd = gtaData[2].split(";")
            json_data = json.loads(data)
            gtaSpd = data
            self.servReport.text = f"[color=00ffcc]{json_data['socStatusLoad'][0]} %, {json_data['socVoltage']/100} V, {json_data['socTemperature']/10} °C[/color]"
            print(json_data)
            pass
        except:
            print("Error in udp data")
    ##server handler CB function
    def remCtrlCB(self, arg):
        #['', 'slot', '0', 'status']
        request = arg.lower().split("/")
        print("CB arg-", request )
        if(request[0] == "run"):
            ##self.backProc.setCmd("run")
            self.backProc.startProc()
            return self.backProc.getStatus()
        elif(request[0] == "stop"):
             self.backProc.stopProc()
             #self.backProc.setCmd("stop")
             return self.backProc.getStatus()  
        return "ok" 
    
    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server_thread.join()

class BoxApp(App):
    def build(self):
        self.screen = MainScreen()
        return self.screen
    
    def on_stop(self):
        self.screen.stop_server()
        pass


if __name__ == '__main__':
    BoxApp().run()
