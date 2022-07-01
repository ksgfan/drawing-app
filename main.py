# -*- coding: utf-8 -*-
from kivy.app import App
# kivy.require("1.8.0")
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.image import Image

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
from kivy.metrics import dp
from os.path import join

# changing color to white
from kivy.core.window import Window
from kivy.graphics import Color, Fbo, ClearColor, ClearBuffers, Scale, Translate, Rectangle



# mode rgba

#setting flag for callback (on_touch_up)
flag = True

#setting empty lists for callback
with_pressure = []    
without_pressure = []
test_type = 'Practise'

#setting time for callback
seconds = time.time()
t = time.localtime(seconds)
local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

class MainScreen(Screen):

    def __init__(self, **kwargs): 
        super(MainScreen, self).__init__(**kwargs)
        
        with self.canvas:
            Color(0.5,0.5, 0.5, 0.5)
            self.rect = Rectangle(size=Window.size,
                                    pos=self.pos)
        
    username = ObjectProperty(None)
    age = ObjectProperty(None)
      
    def reset(self):
        self.username.text = ""
        self.age.text = ""

    def check_inputs(self):
        gender = ApplePenApp.get_running_app().gender
        # check, if the inputs are not empty and are valid
        if self.username.text == "" and self.age.text == "":
            self.username.hint_text = "Enter valid ID!"
            self.age.hint_text = "Enter valid Age!"
        elif self.username.text == "":
            self.username.hint_text = "Enter valid ID!"
        elif self.age.text == "":
            self.age.hint_text = "Enter valid Age!"
        elif not(self.age.text.isnumeric()):
            self.age.text = ""
            self.age.hint_text = "Enter valid Age!"
        elif gender == "":
            self.gender_label.text = "Select Gender!"
            self.gender_label.color = [1, 0, 0, 1]
        else:
            # if inputs are valid, go to the next screen
            self.manager.current = "drawing"
            self.gender_label.text = "Gender:"
            self.gender_label.color = [1, 1, 1, 1]
            
                                      
class SecondScreen(Screen):
    
    def __init__(self,**kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.drawinput = DrawInput()  

    # Replace the given image source value:
    def display_image(self):
        global test_type
        if test_type == "Practise":
            self.ids.viewImage.source = 'practiseImage.png'
            self.ids.instructions.text = "Warm up! Draw a copy of the image as accurately as possible. \nAfter completion press 'Finish' to proceed"
        elif test_type == "Copy":
            self.ids.viewImage.source = 'reyFigure.png'
            self.ids.instructions.text = "Draw a copy of the Rey Figure as accurately as possible. \nAfter completion press 'Finish' to proceed"
        else:
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Try to draw the Rey Figure again from your memory. \nAfter completion press 'Finish' to proceed"

class BetweenTrialScreen(Screen):

    def __init__(self,**kwargs):
        super(BetweenTrialScreen, self).__init__(**kwargs)

        with self.canvas:
            Color(0.5,0.5, 0.5, 0.5)
            self.rect = Rectangle(size=Window.size,
                                    pos=self.pos)
    def change_text(self):
        if test_type == 'Copy':
            self.ids.between_trial_label.text = "Well done! \nPress 'Continue' to start the actual task!"
        elif test_type == 'Recall':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a new task!"
        elif test_type == 'Delayed':
            self.ids.between_trial_label.text = "Great! \nNow please solve the RAVEN Matrices test! \nAFTER finishing the RAVEN test, press 'Continue'"
        elif test_type == 'Finished':
            self.ids.between_trial_label.text = "Finished!"

    def get_test_type(self):
        return test_type

class AnotherScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass   
class DrawInput(Widget):


    def __init__(self,**kwargs):
        super(DrawInput, self).__init__(**kwargs)
       
        self.drawing_counter = []

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
        global test_type
        # self.test_type = ApplePenApp.get_running_app().t_type # self.a[-1]
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + str(test_type) + ".png")   
        instance.export_as_image().save(name)


    #setting line width       
    line_width = NumericProperty(3)
    def change_width(self):
        if ApplePenApp.get_running_app().line_width == "Line Width: 2 mm":
            self.line_width = 2
        elif ApplePenApp.get_running_app().line_width == "Line Width: 3 mm":
            self.line_width = 3
        return self.line_width
    
    def reset_line_width(self):
        self.line_width = 3
        

    def normalize_pressure(self, pressure):
        print(pressure)
        # this might mean we are on a device whose pressure value is
        # incorrectly reported by SDL2, like recent iOS devices.
        if pressure == 0.0:
            return 1
        return dp(pressure * 10)

    #drawing and saving text methods       
    def on_touch_down(self, touch):

        global flag
        global test_type
        flag = True
        
        # self.test_type = ApplePenApp.get_running_app().t_type 
        timing_ms = ApplePenApp.get_running_app().sw_seconds       
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + test_type + ".txt")
        
        if 'pressure' in touch.profile: 
            touch.ud['pressure'] = touch.pressure

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
        global test_type
        global with_pressure
        global without_pressure
        
        # self.test_type = ApplePenApp.get_running_app().t_type
        timing_ms = ApplePenApp.get_running_app().sw_seconds
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + test_type + ".txt")

        if 'pressure' in touch.profile:
            touch.ud['pressure'] = touch.pressure
            
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
        
    def my_callback(self, dt):
        global flag
        global test_type
        global with_pressure
        global without_pressure
        global local_time

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
    
    def start_callback(self):
        self.event = Clock.schedule_interval(self.my_callback, 0.001)

    def stop_callback(self):
        self.event.cancel()

    def save_data(self):

        global test_type
        self.gender = ApplePenApp.get_running_app().gender
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, "InfoTable")
        
        x = open(name, "a")
        x.write(str(self.filename) + "\t"+str(self.age)+"\t"+
                str(self.gender)+"\t"+ str(test_type) +
                "\t"+platform.platform()+"\t"+platform.mac_ver()[0]+
                "\t"+str(Window.size)+"\n") 


    def switch_test_type(self):
        global test_type

        if len(self.drawing_counter) == 0:
            test_type = "Practise"
        if len(self.drawing_counter) == 1:
            test_type = "Copy"
        elif len(self.drawing_counter) == 2:
            test_type = "Recall"
        elif len(self.drawing_counter) == 3:
            test_type = "Delayed"
        elif len(self.drawing_counter) > 3:
            test_type = "Finished"

        return test_type


    def count_figures(self):
        self.drawing_counter.append(1)

       
presentation = Builder.load_file("applepen_kivy.kv")

class ApplePenApp(App):

    Window.clearcolor = (1, 1, 1, 1)

    #var = DrawInput()
    var_main = MainScreen()

    filename = StringProperty("") # ID
    # t_type = StringProperty("Copy")
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

    def on_pause(self):
        return True

    def build(self):
        return presentation
       
if __name__=="__main__":
    ApplePenApp().run()


