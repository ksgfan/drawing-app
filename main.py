# -*- coding: utf-8 -*-
from glob import glob
from math import log1p
import webbrowser
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
import numpy as np
# changing color to white
from kivy.core.window import Window
from kivy.graphics import Color, Fbo, ClearColor, ClearBuffers, Scale, Translate, Rectangle, Line, Ellipse, Bezier

from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton


##### This Version of the application works only with Apple Pencil. If pressure is not greater than 0, nothing will be drawn.
##### It prevents accidental drawing by wrist etc. In 'old_main.py' it is also possible to draw with a finger or with a stylus 
##### without pressure information. 


# setting empty lists for callback
flag = True
with_pressure = []    
without_pressure = []
test_counter = 0
raven_counter = 0
test_type = ''
presentation_sequence = ['bPractise', 'Practise', 'bNachzeichnen', 'CopySq', 'CopyCircle', 'CopySpiral', 
                         'bReyCopy', 'CopyRey', 'bRecall', 'RecallRey', 'bQuest', 'Education', 'Handedness', 'TabletTrust', 'Drugs', 
                         'bMaze', 'Maze', 'bRaven', 'Raven', 'bDelayed', 'DelayedRey',
                         'bcogTests', 'bTaylor', 'bTestFam', 'TestFam', 'bFinished']
"""
presentation_sequence = ['bPractise', 'bcogTests', 'bNachzeichnen', 'CopySq', 'CopyCircle', 'CopySpiral', 
                         'bReyCopy', 'CopyRey', 'bRecall', 'RecallRey', 'bQuest', 'Education', 'Handedness', 'TabletTrust', 'Drugs', 
                         'bMaze', 'Maze', 'bRaven', 'Raven', 'bDelayed', 'DelayedRey',
                         'bcogTests', 'bTaylor', 'bTestFam', 'TestFam', 'bFinished']
"""
# when using a new link: remove everything that is after '=..' (i.e., remove everything between % % signs (% inlcuding) ) you need paste there unique subject ID
link_cog_tests = 'https://eu.cognitionlab.com/ertslab-0.1/sona/5T0DhbQnDm2hXH9yU2RCVMJG3QBHJPcj?c='

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
            # if inputs are valid, save them
            self.gender_label.text = "Gender:"
            self.gender_label.color = [1, 1, 1, 1] 
            App.get_running_app().switch_test_type()
        
            
class HandScreen(Screen):
    pass

class EduScreen(Screen):
    pass

class TrustScreen(Screen):
    pass

class DrugScreen(Screen):
    pass

class TestFamScreen(Screen):
    pass

class RavenScreen(Screen):
    def __init__(self,**kwargs):
        super(RavenScreen, self).__init__(**kwargs)
        self.raven_figures = 0
        self.raven_respons = StringProperty("")
        self.all_responses = []
        
    def change_items(self):
        global test_type
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
            App.get_running_app().switch_test_type()

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
        elif test_type == "CopyRey":
            self.ids.viewImage.source = 'images/reyFigure.png'
            self.ids.instructions.text = "Draw a copy of the Rey Figure as accurately as possible. \nAfter completion press 'Finish' to proceed"
            self.canvas.remove_group(u"rect")
        elif test_type in ['RecallRey', 'DelayedRey']:
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Try to draw the Rey Figure again from your memory. \nAfter completion press 'Finish' to proceed"
        elif test_type == "CopySq":
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Zeichnen Sie die Figure nach. \nAfter completion press 'Finish' to proceed"
            # draw a square
            with self.canvas:
                # https://kivy.org/doc/stable/examples/gen__canvas__lines_extended__py.html
                Color(0, 0, 0, 1)
                s = (500, 500)
                Line(rectangle = (self.center_x - s[0] / 2, self.center_y - s[1] / 2, s[0], s[1]), width = 2, group = u"rect")
        elif test_type == "CopyCircle":
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Zeichnen Sie die Figure nach. \nAfter completion press 'Finish' to proceed"
            # first, remove rect
            self.canvas.remove_group(u"rect")
            # draw a circle
            with self.canvas:
                Color(0, 0, 0, 1)
                r = 250
                Line(circle = (self.center_x, self.center_y, r), width = 2, group = u"rect")
        elif test_type == "CopySpiral":
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Zeichnen Sie die Figure nach. \nAfter completion press 'Finish' to proceed"
            # first, remove rect
            self.canvas.remove_group(u"rect")
            # draw a circle
            with self.canvas:
                Color(0, 0, 0, 1)
                theta = np.linspace(0, 10 * np.pi, 1000)
                r = theta ** 1.7 # adjust to change the size
                x = r * np.cos(theta) + self.center_x
                y = r * np.sin(theta) + self.center_y
                spirale = []
                for i in range(0, len(x)):
                    spirale.append(x[i])
                    spirale.append(y[i])

                Line(points = (spirale), width = 2, group = u"rect")
                
        else:
            self.canvas.remove_group(u"rect")
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Here. \nAfter completion press 'Finish' to proceed"


class DrawInput(Widget):
    '''
    canvas to draw. Its on top of 'DrawingScreen'
    '''
    def __init__(self,**kwargs):
        super(DrawInput, self).__init__(**kwargs)

    username = StringProperty('')
    age = StringProperty('')

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
        user_data_dir = App.get_running_app().user_data_dir
        self.username = ApplePenApp.get_running_app().username
        name = join(user_data_dir, self.local_time + "_" + self.username + "_" + str(test_type) + ".png")   
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
        self.username = ApplePenApp.get_running_app().username
        name = join(user_data_dir, self.local_time + "_" + self.username + "_" + test_type + ".txt")
        
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
        self.username = ApplePenApp.get_running_app().username
        name = join(user_data_dir, self.local_time + "_" + self.username + "_" + test_type + ".txt")

        if 'pressure' in touch.profile:
            # draw only, when pressure > 0 - otherwise accidental lines could be drawn by wrist etc.
            if touch.pressure > 0:
                touch.ud['pressure'] = touch.pressure
                
                to_save_move = (str(timing_ms) + "\t"
                        + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" +
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "move"
                        + "\t" + str(touch.pressure) + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")
            
                # print(str(touch.pos[0]) + "\t" + str(touch.pos[1]))
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
        self.username = ApplePenApp.get_running_app().username
        name = join(user_data_dir, local_time + "_" + self.username + "_" + test_type + ".txt")
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
        self.username = ApplePenApp.get_running_app().username
        self.age = ApplePenApp.get_running_app().age
        user_data_dir = App.get_running_app().user_data_dir
        name = join(user_data_dir, "InfoTable")
        
        # save to a file
        x = open(name, "a")
        x.write(str(self.username) + "\t"+str(self.age)+"\t"+
                str(self.gender)+"\t"+ str(test_type) +
                "\t"+platform.platform()+"\t"+platform.mac_ver()[0]+
                "\t"+str(Window.size)+"\n") 

class BetweenTrialScreen(Screen):
    '''
    between trial screen with instructions
    '''
    def change_text(self):
        '''
        update instructions between trials on the screen
        '''
        global test_type
        if test_type == 'bPractise':
            self.ids.between_trial_label.text = "Herzlich Wilkommen zu unserer Studie! \nPress 'Continue' to start the actual task!"
        elif test_type == 'bNachzeichnen':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a new task!"
        elif test_type == 'bReyCopy':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a new task!"
        elif test_type == 'bQuest':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start questionnaires!"
        elif test_type == 'bMaze':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a maze!"
        elif test_type == 'bRaven':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start raven!!"
        elif test_type == 'bDelayed':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start a delayed recall!"
        elif test_type == 'bcogTests':
            self.ids.between_trial_label.text = "Great! \nPress 'Continue' to start cognitve tests!"
        elif test_type == 'bTaylor':
            self.ids.between_trial_label.text = "Good job! You finished the cognitive tests! \nPress 'Continue' to start a taylor figure!"
        elif test_type == 'bTestFam':
            self.ids.between_trial_label.text = "Good job! \nPress 'Continue' to start the final questionnaire!"
        elif test_type == 'bFinished':
            self.ids.between_trial_label.text = "Finished! \nPress 'Continue' to complete the study!"

    def start_cog_tests(self):
        global test_type
        global link_cog_tests
        if test_type == 'bcogTests':
            username = ApplePenApp.get_running_app().username
            link = link_cog_tests + username
            webbrowser.open(link)

class ScreenManagement(ScreenManager):
    pass   

class ApplePenApp(MDApp):

    # color window to white
    Window.clearcolor = (1, 1, 1, 1)

    # get vars
    #var_main = MainScreen()
    username = StringProperty("") # ID
    age = StringProperty("")
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

    def switch_test_type(self):
        '''
        count conditions/tests/quests and update test type accordingly
        '''
        global test_type
        global test_counter
        global raven_counter
        global presentation_sequence
        # remove first element of the list and save it in the test_type variable 
        test_type = presentation_sequence.pop(0)
        test_counter = test_counter + 1
        print(test_counter)

        # now switch the screen according to test type
        if test_type in ['Practise', 'CopySq', 'CopyCircle', 'CopySpiral', 'CopyRey', 'RecallRey', 'DelayedRey', 'Maze']:
            App.get_running_app().root.current = 'drawing'
            # call the display_image method to change instructions and figures accordingly
            screen = App.get_running_app().root.get_screen("drawing")
            # display figure/test
            screen.display_image()
            # start clocks
            self.reset()
            self.start_clock()
            
        elif test_type in ['bPractise', 'bNachzeichnen', 'bReyCopy',  'bRecall',  
                'bQuest', 'bMaze',  'bRaven', 'bDelayed',
                'bcogTests', 'bTestFam', 'bTaylor']:
            App.get_running_app().root.current = 'between_trial'
            # call the change_text method to change instructions and figures accordingly
            between_screen = App.get_running_app().root.get_screen("between_trial")
            between_screen.change_text()

        elif test_type == 'Handedness':
            App.get_running_app().root.current = 'handscreen'
            
        elif test_type == 'Education':
            App.get_running_app().root.current = 'eduscreen'

        elif test_type == 'TabletTrust':
            App.get_running_app().root.current = 'trustscreen'

        elif test_type == 'Drugs':
            App.get_running_app().root.current = 'drugscreen'

        elif test_type == 'Raven':
            App.get_running_app().root.current = 'ravenscreen'
            # raven consists of 13 sub-screens (12 + 1 example)
            #raven_counter = raven_counter + 1
            #print(raven_counter)
            #if raven_counter > 12:
            #    between_screen = App.get_running_app().root.get_screen("between_trial")
            #    between_screen.change_text()

        elif test_type == 'TestFam':
            App.get_running_app().root.current = 'testfamscreen'

        else:
            print('nothing happened')



    def build(self):
        presentation = Builder.load_file("applepen_kivy.kv")
        return presentation
       
if __name__=="__main__":
    ApplePenApp().run()


