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
import platform
import sys

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
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from os.path import join

# changing color to white
from kivy.core.window import Window
from kivy.graphics import Color, Fbo, ClearColor, ClearBuffers, Scale, Translate

# mode rgba

#setting flag for callback (on_touch_up)
flag = True

#setting empty lists for callback
with_pressure = []    
without_pressure = []

#setting time for callback
seconds = time.time()
t = time.localtime(seconds)
local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

class MainScreen(Screen):
        
    username = ObjectProperty(None)
    age = ObjectProperty(None)
            
    def reset(self):
        self.username.text = ""
        self.age.text = ""
                                      
class SecondScreen(Screen):
    pass      
class AnotherScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass   
class DrawInput(Widget):


##    def __init__(self,**kwargs):
##        super(DrawInput, self).__init__(**kwargs)
##        Clock.schedule_interval(self.on_touch_up, 0.1)

        
    filename = StringProperty("")
    age = StringProperty("")

    #pen color default
    pencolor =  ListProperty([0, 0, 0, 1])
    #pen color
    def change_color(self, instance):
        self.pencolor = instance.color

    #setting time
    seconds = time.time()
    t = time.localtime(seconds)
    local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

    def export_as_image(self, *args, **kwargs):
        
        # overwrite the function, because ClearColor is set to black per default
        from kivy.core.image import Image
        scale = kwargs.get('scale', 1)

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=(self.width * scale, self.height * scale),
                  with_stencilbuffer=True)

        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Scale(scale, scale, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        img = Image(fbo.texture)
        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        return img

    #screenshot        
    def save_image(self, instance):
        self.test_type = ApplePenApp.get_running_app().t_type # self.a[-1]
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + str(self.test_type) + ".png")   
        instance.export_as_image().save(name)


    #setting line width       
    line_width = NumericProperty(1)
    def change_width(self):
        if ApplePenApp.get_running_app().line_width == "1 mm":
            self.line_width = 1
        elif ApplePenApp.get_running_app().line_width == "2 mm":
            self.line_width = 2
        elif ApplePenApp.get_running_app().line_width == "3 mm":
            self.line_width = 3
        return self.line_width
    
    def reset_line_width(self):
        self.line_width = 1
        

    #drawing and saving text methods       
    def on_touch_down(self, touch):

        global flag
        flag = True
        
        self.test_type = ApplePenApp.get_running_app().t_type 
        timing_ms = ApplePenApp.get_running_app().sw_seconds       
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".txt")
        
        if 'pressure' in touch.profile: 
            ud['pressure'] = touch.pressure

            to_save = (str(timing_ms) + "\t" + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" + 
                     str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch" + "\t" + str(touch.pressure) 
                     + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")
        else:
            to_save = (str(timing_ms) + "\t" + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                     str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch" + "\t" + str(self.pencolor) + "\t" 
                     + str(self.line_width) +"\t"+str(Window.size)+"\n")

                      
        x = open(name, "a")
        x.write(to_save)
    
        with self.canvas:
            Color(rgba = self.pencolor)
            touch.ud["line"] = Line(points = (touch.x, touch.y), width = self.change_width())

    def on_touch_move(self, touch):

        global flag
        flag = True

        global with_pressure
        global without_pressure
        
        self.test_type = ApplePenApp.get_running_app().t_type
        timing_ms = ApplePenApp.get_running_app().sw_seconds
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + self.test_type + ".txt")

        if 'pressure' in touch.profile:
            ud['pressure'] = touch.pressure
            
            to_save2 = (str(timing_ms) + "\t"
                    + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                     str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move"
                    + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")
        

            #to a list
            with_pressure.append(str(touch.spos[0]))
            with_pressure.append(str(touch.spos[1]))
            with_pressure.append(str(touch.pos[0]))
            with_pressure.append(str(touch.pos[1]))
            with_pressure.append("up")
            with_pressure.append("0") ### change to pressure 
            with_pressure.append(str(self.pencolor))
            with_pressure.append(str(self.line_width))
            with_pressure.append(str(Window.size))

        else:
            to_save2 = (str(timing_ms) + "\t"
                    + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" + str(touch.pos[0]) + "\t" 
                    + str(touch.pos[1]) + "\t" + "move" + "\t" + str(self.pencolor) + "\t" + str(self.line_width) 
                    + "\t"+str(Window.size)+"\n")

            #to a list
            without_pressure.append(str(touch.spos[0]))
            without_pressure.append(str(touch.spos[1]))
            without_pressure.append(str(touch.pos[0]))
            without_pressure.append(str(touch.pos[1]))
            without_pressure.append("up")
            without_pressure.append(str(self.pencolor))
            without_pressure.append(str(self.line_width))
            without_pressure.append(str(Window.size))

        x = open(name, "a")
        x.write(to_save2)
        touch.ud["line"].points += (touch.x, touch.y)

        return flag
            
    def on_touch_up(self, touch):
        
        global flag
        flag = False

        return flag
        
    def my_callback(dt):
        global flag
        global with_pressure
        global without_pressure
        global local_time

        test_type = ApplePenApp.get_running_app().t_type
        user_data_dir = App.get_running_app().user_data_dir
        filename = ApplePenApp.get_running_app().filename
 
        name = join(user_data_dir, local_time + "_" + filename + "_" + test_type + ".txt")
        
        timing_ms = ApplePenApp.get_running_app().sw_seconds

        if flag is False:
            # one list list always empty!
            if not without_pressure and not with_pressure:
                pass
            
            elif len(without_pressure) > len(with_pressure):
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"+ without_pressure[-8] +"\t"+ without_pressure[-7] +"\t"+ without_pressure[-6]+"\t"+
                        without_pressure[-5]+"\t"+without_pressure[-4]+"\t"+without_pressure[-3]+"\t"+
                        without_pressure[-2]+"\t"+without_pressure[-1]+"\n")
                if len(without_pressure) > 8:
                    del without_pressure[0:-8]

            elif len(without_pressure) < len(with_pressure):
                x = open(name, "a")
                x.write(str(timing_ms) + "\t"+ with_pressure[-9]+ "\t"+ with_pressure[-8] +"\t"+ with_pressure[-7] +"\t"+
                        with_pressure[-6]+"\t"+ with_pressure[-5]+"\t"+with_pressure[-4]+"\t"+
                        with_pressure[-3]+"\t"+ with_pressure[-2]+"\t"+ with_pressure[-1]+"\n")
                if len(with_pressure) > 8:
                    del with_pressure[0:-9]
        else:
            pass
            
    Clock.schedule_interval(my_callback, 0.001)
        
    def save_data(self):

        self.test_type = ApplePenApp.get_running_app().t_type
        self.gender = ApplePenApp.get_running_app().gender
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, "InfoTable")
        
        x = open(name, "a")
        x.write(str(self.filename) +"\t"+str(self.age)+"\t"+
                str(self.gender)+"\t"+ str(self.test_type) +
                "\t"+platform.platform()+"\t"+platform.mac_ver()[0]+
                "\t"+str(Window.size)+"\n") 
                
       
presentation = Builder.load_file("applepen_kivy.kv")

class ApplePenApp(App):

    Window.clearcolor = (1, 1, 1, 1)

    #var = DrawInput()
    var_main = MainScreen()

    filename = StringProperty("")
    t_type = StringProperty("")
    gender = StringProperty("")
    line_width = StringProperty("")
 
    #clock
    sw_started = False
    sw_seconds = 0
    def update_clock(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
            
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


