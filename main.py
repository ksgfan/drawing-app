# -*- coding: utf-8 -*-
from math import log1p
from kivy.app import App
# kivy.require("1.8.0")
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.metrics import dp
from os.path import join

import os
import time
import platform
import sys

# changing color to white
from kivy.core.window import Window
from kivy.graphics import Color, Fbo, ClearColor, ClearBuffers, Scale, Translate, Rectangle, Line

from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton


##### This Version of the application works only with Apple Pencil. If pressure is not greater than 0, nothing will be drawn.
##### It prevents accidental drawing by wrist etc. In 'old_main.py' it is also possible to draw with a finger or with a stylus 
##### without pressure information. 


# setting empty lists for callback
flag = True
with_pressure = []    
without_pressure = []
test_type = 'Practise'

# setting time for callback
seconds = time.time()
t = time.localtime(seconds)
local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

class MainScreen(Screen):

    def __init__(self, **kwargs): 
        super(MainScreen, self).__init__(**kwargs)
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size,
                                    pos=self.pos)
        
    username = ObjectProperty(None)
    age = ObjectProperty(None)
      
    def reset(self):
        self.username.text = ""
        self.age.text = ""

    def check_inputs(self):
        '''
        check, if demographics make sense
        '''

        self.manager.current = "drawing"

"""         gender = ApplePenApp.get_running_app().gender
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
            self.gender_label.color = [1, 1, 1, 1] """
            
class HandScreen(Screen):
    def __init__(self,**kwargs):
        super(HandScreen, self).__init__(**kwargs)

class EduScreen(Screen):
    def __init__(self,**kwargs):
        super(EduScreen, self).__init__(**kwargs)

class TrustScreen(Screen):
    def __init__(self,**kwargs):
        super(TrustScreen, self).__init__(**kwargs)

class DrugScreen(Screen):
    def __init__(self,**kwargs):
        super(DrugScreen, self).__init__(**kwargs)

class TestFamScreen(Screen):
    def __init__(self,**kwargs):
        super(TestFamScreen, self).__init__(**kwargs)

class RavenScreen(Screen):
    def __init__(self,**kwargs):
        super(RavenScreen, self).__init__(**kwargs)
        self.raven_figures = 0
        self.raven_respons = StringProperty("")
        self.all_responses = []
        
    def change_items(self):
        #print(self.raven_figures)
        if self.raven_figures == 0:
            screen = self.manager.get_screen("ravenscreen")
            txt1 = """Hier unten ist ein Muster mit einer Lücke. 
                  \nJedes der Teilstücke hier unten passt der 
                  \nGrösse nach in die Lücke des Musters  
                  \naber nur ein einziges Teilstück ergänzt das  
                  \nMuster richtig. Alle Teilstücke müssen 
                  \ngenau angeschaut werden
                  """
            txt2 = "Welches ist das Teilstück das genau richtig ist?"
            txt3 = """Nummer 8 ist richtig.
                   \nMarkieren Sie 8 und
                   \ndrücken Sie 'Weiter'
                   \num mit der richtigen
                   \nAufgabe anzufangen.
                   """

            self.l1 = Label(text=txt1, pos = (-700, 340), font_size = 30, color = (0, 0, 0, 1))
            self.l2 = Label(text=txt2, pos = (0, -50), font_size = 30, color = (0, 0, 0, 1))
            self.l3 = Label(text=txt3, pos = (750, -450), font_size = 30, color = (0, 0, 0, 1))
            screen.add_widget(self.l1)
            screen.add_widget(self.l2)
            screen.add_widget(self.l3)
            self.ids.instructions_label.text = "Raven Matrizen-Test. Beispiel-Aufgabe."
            self.ids.raven_fig.source = "images/Raven0.png"

            # update index
            self.raven_figures = self.raven_figures + 1
        elif self.raven_figures > 0 and self.raven_figures < 13:
            screen = self.manager.get_screen("ravenscreen")
            # remove instruction labels
            if self.raven_figures == 1: 
                screen.remove_widget(self.l1)
                screen.remove_widget(self.l2)
                screen.remove_widget(self.l3)

            # change instrution and update figure
            self.ids.instructions_label.text = "Raven Matrizen-Test (" + str(self.raven_figures) + " / 12)"
            self.ids.raven_fig.source = "images/Raven" + str(self.raven_figures) + ".png"
            self.raven_figures = self.raven_figures + 1
        else:
            # if task is finished, go to another screen
            self.manager.current = "handscreen"

    def save_raven_resp(self):
        self.all_responses.append(self.raven_respons)
        #print(self.all_responses)
        # remove check 
        for val in list(self.ids.values()):
            try:
                val.active = False
            except:
                print("Can't deactivate")



class DrawingScreen(Screen):
    ''' 
    canvas screen
    '''
    
    def __init__(self,**kwargs):
        super(DrawingScreen, self).__init__(**kwargs)
        self.drawinput = DrawInput()  

    # Replace the given image source value:
    def display_image(self):
        '''
        display images to copy and update instructions on the screen
        '''
        global test_type
        if test_type == "Practise":
            self.ids.viewImage.source = 'images/practiseImage.png'
            self.ids.instructions.text = "Warm up! Draw a copy of the image as accurately as possible. \nAfter completion press 'Finish' to proceed"
        elif test_type == "Copy":
            self.ids.viewImage.source = 'images/reyFigure.png'
            self.ids.instructions.text = "Draw a copy of the Rey Figure as accurately as possible. \nAfter completion press 'Finish' to proceed"
        else:
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Try to draw the Rey Figure again from your memory. \nAfter completion press 'Finish' to proceed"

            # test
            with self.canvas:
                # https://kivy.org/doc/stable/examples/gen__canvas__lines_extended__py.html
                print(self.center_x,self.center_y)
                Color(0, 0, 0, 1)
                s = (500, 500)
                rect = Line(rectangle = (self.center_x - s[0] / 2, self.center_y - s[1] / 2, s[0], s[1]), width = 2)



class BetweenTrialScreen(Screen):
    '''
    between trial screen with instructions
    '''

    def __init__(self,**kwargs):
        super(BetweenTrialScreen, self).__init__(**kwargs)

        with self.canvas:
            Color(0.5,0.5, 0.5, 0.5)
            self.rect = Rectangle(size=Window.size,
                                    pos=self.pos)
    def change_text(self):
        '''
        update instructions between trials on the screen
        '''
        if test_type == 'Copy':
            self.ids.between_trial_label.text = "Well done! \nPress 'Continue' to start the actual task!"
        elif test_type == 'Recall':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a new task!"
        elif test_type == 'Delayed':
            self.ids.between_trial_label.text = "Great! \n[color=#ff0000]Now please put the tablet aside [/color] and solve the RAVEN Matrices test! \nAFTER finishing the RAVEN test, press 'Continue'"
        elif test_type == 'Finished':
            self.ids.between_trial_label.text = "Finished! \nPress 'Continue' to complete the study!"

    def get_test_type(self):
        return test_type

    def close_application(self):
        '''
        close the application after delayed recall
        '''
        if self.get_test_type() == 'Finished':
            App.get_running_app().stop()
        else:
            pass


class AnotherScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass   

class DrawInput(Widget):
    '''
    canvas to draw. Its on top of 'DrawingScreen'
    '''

    def __init__(self,**kwargs):
        super(DrawInput, self).__init__(**kwargs)
       
        self.drawing_counter = []

    filename = StringProperty("")
    age = StringProperty("")

    # pen color default
    pencolor =  ListProperty([0, 0, 0, 1])
    # pen color
    def change_color(self, instance):
        self.pencolor = instance.color

    # setting time
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

    # screenshot        
    def save_image(self, instance):
        global test_type
        # self.test_type = ApplePenApp.get_running_app().t_type # self.a[-1]
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + str(test_type) + ".png")   
        instance.export_as_image().save(name)


    # setting line width       
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

    # drawing and saving text methods       
    def on_touch_down(self, touch):

        # get vars
        global flag
        global test_type
        flag = True
        timing_ms = ApplePenApp.get_running_app().sw_seconds       
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + test_type + ".txt")
        
        if 'pressure' in touch.profile: 
            # draw only, when pressure > 0 - otherwise accidental lines could be drawn by wrist etc.
            if touch.pressure > 0:
                touch.ud['pressure'] = touch.pressure

                to_save_down = (str(timing_ms) + "\t" + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" + 
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "touch" + "\t" + str(touch.pressure) 
                        + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")

                # save to a file     
                x = open(name, "a")
                x.write(to_save_down)

                # draw on canvas
                with self.canvas:
                    Color(rgba = self.pencolor)
                    touch.ud["line"] = Line(points = (touch.x, touch.y), width = self.change_width())

    def on_touch_move(self, touch):

        # get vars
        global flag
        flag = True
        global test_type
        global with_pressure
        global without_pressure
        timing_ms = ApplePenApp.get_running_app().sw_seconds
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, self.local_time + "_" + self.filename + "_" + test_type + ".txt")

        if 'pressure' in touch.profile:
            # draw only, when pressure > 0 - otherwise accidental lines could be drawn by wrist etc.
            if touch.pressure > 0:
                touch.ud['pressure'] = touch.pressure
                
                to_save_move = (str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")
            
                print(str(touch.pos[0]) + "\t" + str(touch.pos[1]))
                # to a list, the last 'move' will serve as 'up'
                with_pressure.append(str(touch.spos[0]))
                with_pressure.append(str(touch.spos[1]))
                with_pressure.append(str(touch.pos[0]))
                with_pressure.append(str(touch.pos[1]))
                with_pressure.append("up")
                with_pressure.append("0") # its for the "up", and "up" has pressure 0
                with_pressure.append(str(self.pencolor))
                with_pressure.append(str(self.line_width))
                with_pressure.append(str(Window.size))

                # save to a file
                x = open(name, "a")
                x.write(to_save_move)

                # draw
                touch.ud["line"].points += (touch.x, touch.y)

        return flag
            
    def on_touch_up(self, touch):
        '''
        without this method and without 'with_pressure' and 'without_pressure' lists, 
        nothing will be saved when the pen does not touch the screen
        '''
        global flag
        flag = False

        return flag
        
    def my_callback(self, dt):
        '''
        write data to a file, while 'touch_up'
        '''

        # get vars
        global flag
        global test_type
        global with_pressure
        global without_pressure
        global local_time
        user_data_dir = App.get_running_app().user_data_dir
        filename = ApplePenApp.get_running_app().filename
        name = join(user_data_dir, local_time + "_" + filename + "_" + test_type + ".txt")
        timing_ms = ApplePenApp.get_running_app().sw_seconds

        # if flag false, meaning on_touch_up is activated
        if flag is False:
            
            # one list list always empty!
            if not without_pressure and not with_pressure:
                pass

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
        '''
        start the callback, which will write data to a file, while 'touch_up'
        '''
        self.event = Clock.schedule_interval(self.my_callback, 0.001)

    def stop_callback(self):
        self.event.cancel()

    def save_data(self):
        '''
        save demographis to a file
        '''

        # get vars
        global test_type
        self.gender = ApplePenApp.get_running_app().gender
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, "InfoTable")
        
        # save to a file
        x = open(name, "a")
        x.write(str(self.filename) + "\t"+str(self.age)+"\t"+
                str(self.gender)+"\t"+ str(test_type) +
                "\t"+platform.platform()+"\t"+platform.mac_ver()[0]+
                "\t"+str(Window.size)+"\n") 


    def switch_test_type(self):
        '''
        count conditions and update test type accordingly
        '''
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

       
class ApplePenApp(MDApp):

    # color window to white
    Window.clearcolor = (1, 1, 1, 1)

    # get vars
    var_main = MainScreen()
    filename = StringProperty("") # ID
    gender = StringProperty("")
    line_width = StringProperty("")
 
    # clock
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
        presentation = Builder.load_file("applepen_kivy.kv")
        return presentation
       
if __name__=="__main__":
    ApplePenApp().run()


