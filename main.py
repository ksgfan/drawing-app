# -*- coding: utf-8 -*-
from kivy.app import App
# kivy.require("1.8.0")
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock

import os
import time

from kivy.config import Config
#Config.set('graphics', 'width', '700')
#Config.set('graphics', 'height', '700')
#Config.write()

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from os.path import join

# changing color to white
from kivy.core.window import Window
from kivy.graphics import Color
Window.clearcolor = (1, 1, 1, 1)
# mode rgba

class MainScreen(Screen):  
        
    username = ObjectProperty(None)
    test_type = ObjectProperty(None)
    test_date = ObjectProperty(None)

    def reset(self):
        self.username.text = ""
        self.test_type.text = ""
        self.test_date.text = ""
        
class SecondScreen(Screen):
    pass     
class AnotherScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass
                                
class DrawInput(Widget):
        
    filename = StringProperty("")
    test_type = StringProperty("")

    pencolor =  ListProperty([0, 0, 0, 1])
    
    seconds = time.time()
    t = time.localtime(seconds)
    local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

    #pen color
    def change_color(self, instance):
        self.pencolor = instance.color
        
    #screenshot        
    def btn_save(self):
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".png")
        Window.dispatch("on_draw")
        Window.screenshot(name)
        #print(name)
        
    def on_touch_down(self, touch):
        
        timing_ms = ApplePenApp.get_running_app().sw_seconds
        
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".txt")

        if 'pressure' in touch.profile:
            ud['pressure'] = touch.pressure
            # print(touch.pressure)
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\n")
            else:

                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\n")


            with self.canvas:
                Color(rgba = self.pencolor)
                touch.ud["line"] = Line(points = (touch.x, touch.y))
        else:
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch" + "\t" + str(self.pencolor) +  "\n")
            else:

                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch" + "\t" + str(self.pencolor) + "\n")


            with self.canvas:
                Color(rgba = self.pencolor)
                touch.ud["line"] = Line(points = (touch.x, touch.y))


       
    def on_touch_move(self, touch):

        timing_ms = ApplePenApp.get_running_app().sw_seconds

        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".txt")

        if 'pressure' in touch.profile:
            ud['pressure'] = touch.pressure
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\n")
            else:
            
                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor)  + "\n")

            touch.ud["line"].points += (touch.x, touch.y)

        else:
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move" + "\t" + str(self.pencolor) + "\n")
            else:
            
                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move" + "\t" + str(self.pencolor) + "\n")

            touch.ud["line"].points += (touch.x, touch.y)
            

    def on_touch_up(self, touch):     

        timing_ms = ApplePenApp.get_running_app().sw_seconds

        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".txt")

        if 'pressure' in touch.profile:
            ud['pressure'] = touch.pressure
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "released" + "\t" + "0" + "\t" + str(self.pencolor) + "\n")
            else:
                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "released" + "\t" + "0" + "\t" + str(self.pencolor) + "\n")
        else:
            
            if os.path.isfile(name) is True:
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                         str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "released" + "\t" + str(self.pencolor) + "\n")
            else:
                x = open(name, "w")
                x.write(str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "released" + "\t" + str(self.pencolor) + "\n")

presentation = Builder.load_file("applepen_kivy.kv")

class ApplePenApp(App):

    sw_started = False
    sw_seconds = 0
    
    def update_clock(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        #print(self.sw_seconds)
            
    def start_clock(self):
        self.sw_started = True

    def reset(self):
        if self.sw_seconds:
            self.sw_seconds = 0
        else:
            pass

    def stop_clock(self):
        self.sw_started = False

    def on_start(self):
        Clock.schedule_interval(self.update_clock, 0)

    def build(self):
        return presentation
       
if __name__=="__main__":
    ApplePenApp().run()


