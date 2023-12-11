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
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
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
from kivymd.toast import toast

##### This Version of the application works only with Apple Pencil. If pressure is not greater than 0, nothing will be drawn.
##### It prevents accidental drawing by wrist etc. In 'old_main.py' it is also possible to draw with a finger or with a stylus 
##### without pressure information. 

# For completion code - set up the URL in Xcode (Targer, URL, add URL) 

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
                         'bcogTests', 'bTaylorCopy', 'bTaylorRecall', 'bTestFam', 'TestFam', 'bFinished']


# when using a new link: remove everything that is after '=..' (i.e., remove everything between % % signs (% inlcuding) ) you need paste there unique subject ID
link_cog_tests = 'https://eu.cognitionlab.com/ertslab-0.1/sona/5T0DhbQnDm2hXH9yU2RCVMJG3QBHJPcj?c='

# setting time for callback
seconds = time.time()
t = time.localtime(seconds)
local_time = str(t.tm_mday) + "_" + str(t.tm_mon) + "_" + str(t.tm_year) + "_" + str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)

# move text input up by writing
#Window.softinput_mode = "below_target"

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
        # for testing
        #App.get_running_app().switch_test_type()

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

class QuestScreens(Screen):
    def __init__(self,**kwargs):
        super(QuestScreens, self).__init__(**kwargs)   

    def check_quest_inputs(self):
        all_checkboxes = []
        all_active = []
        # go trough all children and their children
        for c in self.walk():
            if isinstance(c, CheckBox):
                # append active checkboxes
                if c.active is True:
                    all_active.append(c.active)
                if c.group not in all_checkboxes:
                    all_checkboxes.append(c.group)
        # check, if all questions were answered
        if len(all_active) < len(all_checkboxes):
            toast('Antworte bitte alle Fragen')
            return
        else:
            App.get_running_app().switch_test_type()   

class HandScreen(QuestScreens):
    pass

class EduScreen(QuestScreens):
    pass

class TrustScreen(QuestScreens):
    pass

class DrugScreen(QuestScreens):
    pass
       
class TestFamScreen(QuestScreens):
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
                  \ngenau angeschaut werden"""
            txt2 = "Welches ist das Teilstück das genau richtig ist?"
            txt3 = """Nummer 8 ist richtig.
                   \nSiehst du warum?
                   \nMarkiere 8 und
                   \ndrücke „Weiter“
                   \num mit der richtigen
                   \nAufgabe anzufangen."""

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

            # get screen
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
            App.get_running_app().stop_clock()
            App.get_running_app().reset()
            App.get_running_app().raven_time.cancel()
            App.get_running_app().switch_test_type()

    def save_raven_resp(self):
        self.all_responses.append(self.raven_respons)
        #print(self.all_responses)
        # remove checks for the next trial
        for val in list(self.ids.values()):
            try:
                val.active = False
            except:
                print("Can't deactivate")

    def check_raven_inputs(self):
        state = False
        for val in list(self.ids.values()):
            try:
                if val.active is True:
                    state = True
            except:
                pass
        # if all values are False (not checked), don't continue and show warning
        if state is False:
            toast('Wähle eine Antwortsalternative')
            return
        # else, save data and go to next trial
        else:
            self.change_items()
            self.save_raven_resp()

    def get_raven_score(self):
        return self.all_responses


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
            self.ids.viewImage.allow_stretch = False
            self.ids.viewImage.size_hint = (0.4, 0.5)
            self.ids.viewImage.pos_hint = {'x': 0.01, 'y': 0.28}
            self.ids.viewImage.source = 'images/practiseImage.png'
            self.ids.instructions.markup = True
            self.ids.instructions.text = """Warm up! Zeichne das Haus [b]rechts neben[/b] die Abbildung, um dich an den Umgang mit dem Tablet und dem Stift zu gewöhnen. Zeichne dazu noch eine Sonne und ein paar Bäume. Sei dabei so präzise wie möglich. 
                                            \nDu kannst deine Zeichnung korrigieren, indem du oben links auf „Löschen“ drückst. 
                                            \nSobald du dich mit dem Stift vertraut gemacht hast, drücke oben rechts auf „Fertig“."""
            # make "Löschen" button visible
            self.ids.clear_button.opacity = 1
            self.ids.clear_button.disable = False
        elif test_type == "CopyRey":
            self.ids.viewImage.allow_stretch = True
            self.ids.viewImage.size_hint = (0.45, 0.45)
            self.ids.viewImage.pos_hint = {'x': 0, 'y': 0.35}
            self.ids.viewImage.source = 'images/reyFigure.jpeg'
            self.ids.instructions.markup = True
            self.ids.instructions.text = """Zeichne die hier auf der linken Seite abgebildete Rey Figur so präzise wie möglich ab. Bitte zeichne dabei [b]nicht direkt[/b] auf die Abbildung, sondern [b]rechts neben[/b] Abbildung.
                                            \nDu kannst deine Zeichnung korrigieren, indem du oben links auf „Löschen“ drückst. 
                                            \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""
            self.canvas.remove_group(u"rect")
            # make "Löschen" button visible
            self.ids.clear_button.opacity = 1
            self.ids.clear_button.disable = False

            ## draw a rectangle where the figure should be drawn
            #with self.canvas:
            #    Color(0, 0, 0, 1)
            #    s = (1000, 800)
            #    Line(rectangle = (self.center_x - 100, self.center_y - s[1] / 2, s[0], s[1]), width = 2, group = u"rect")

        elif test_type in ['RecallRey', 'DelayedRey']:
            self.ids.viewImage.source = ''
            # make "Löschen" button visible
            self.ids.clear_button.opacity = 1
            self.ids.clear_button.disable = False
            if test_type == 'RecallRey':
                self.ids.instructions.markup = True
                self.ids.instructions.text = """Erinnere Dich an die Rey Figur, die du in der vorherigen Aufgabe abgezeichnet hast. Zeichne die Figur so präzise wie möglich aus deiner Erinnerung. 
                                                \nDu kannst deine Zeichnung korrigieren, indem du oben links auf „Löschen“ drückst. 
                                                \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""
            else:
                self.ids.instructions.markup = True
                self.ids.instructions.text = """Erinnere Dich an die Rey Figur, die du zu Beginn abgezeichnet hast. Zeichne die Figur so präzise wie möglich aus deiner Erinnerung. 
                                                \nDu kannst deine Zeichnung korrigieren, indem du oben links auf „Löschen“ drückst. 
                                                \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""

        elif test_type == "CopySq":
            self.ids.viewImage.source = ''
            self.ids.instructions.markup = True
            self.ids.instructions.text = """Zeichne das Quadrat so präzise wie möglich ab. Bitte zeichne dabei [b]direkt[/b] auf die Abbildung.
                                            \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""            
            # make "Löschen" button not visible
            self.ids.clear_button.opacity = 0
            self.ids.clear_button.disable = True
            # draw a square
            with self.canvas:
                # https://kivy.org/doc/stable/examples/gen__canvas__lines_extended__py.html
                Color(0, 0, 0, 1)
                s = (500, 500)
                Line(rectangle = (self.center_x - s[0] / 2, self.center_y - s[1] / 2, s[0], s[1]), width = 2, group = u"rect")
                self.center_square = (self.center_x, self.center_y)
        elif test_type == "CopyCircle":
            self.ids.viewImage.source = ''
            self.ids.instructions.markup = True
            self.ids.instructions.text = """Zeichne den Kreis so präzise wie möglich ab. Bitte zeichne dabei [b]direkt[/b] auf die Abbildung. 
                                         \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""
            # first, remove rect
            self.canvas.remove_group(u"rect")
            # make "Löschen" button not visible
            self.ids.clear_button.opacity = 0
            self.ids.clear_button.disable = True
            # draw a circle
            with self.canvas:
                Color(0, 0, 0, 1)
                r = 250
                Line(circle = (self.center_x, self.center_y, r), width = 2, group = u"rect")
                self.center_circle = (self.center_x, self.center_y)
        elif test_type == "CopySpiral":
            self.ids.viewImage.source = ''
            self.ids.instructions.markup = True
            self.ids.instructions.text = """Zeichne die Spirale so präzise wie möglich ab. Bitte zeichne dabei [b]direkt[/b] auf die Abbildung. 
                                            \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""            
            # first, remove rect
            self.canvas.remove_group(u"rect")
            # make "Löschen" button not visible
            self.ids.clear_button.opacity = 0
            self.ids.clear_button.disable = True
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
                self.center_spiral = (self.center_x, self.center_y)

        elif test_type == "Maze":
            self.ids.viewImage.source = 'images/maze1.png'
            self.ids.instructions.text = """Löse das Labyrinth. 
                                         \nSobald du die Aufgabe beendet hast, drücke oben rechts auf „Fertig“."""
            # first, remove rect
            self.canvas.remove_group(u"rect")
            # make "Löschen" button not visible
            self.ids.clear_button.opacity = 0
            self.ids.clear_button.disable = True
            with self.canvas:
                self.ids.viewImage.allow_stretch = True
                self.ids.viewImage.size_hint = (None, None)
                self.ids.viewImage.size = (int(968*1.3), int(664*1.3))
                px = (self.center_x - (self.ids.viewImage.size[0] / 2)) / self.size[0]
                py = (self.center_y - (self.ids.viewImage.size[1] / 2)) / self.size[1]
                self.ids.viewImage.pos_hint = {'x': px, 'y': py}
                self.center_maze = (self.center_x, self.center_y)
        else:
            self.canvas.remove_group(u"rect")
            self.ids.viewImage.source = ''
            self.ids.instructions.text = "Empty. \nAfter completion press 'Finish' to proceed"

    def get_screen_centers(self):
        center_dict = {}
        center_dict["center_square"] = self.center_square
        center_dict["center_circle"] = self.center_circle
        center_dict["center_spiral"] = self.center_spiral
        center_dict["center_maze"] = self.center_maze
        return center_dict

class DrawInput(Widget):
    '''
    canvas to draw. Its on top of 'DrawingScreen'
    '''
    def __init__(self,**kwargs):
        super(DrawInput, self).__init__(**kwargs)
        self.flag_clear = False

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

                # first check, if the "Löschen" button was pressed.
                if self.flag_clear is True:
                    to_save_down = (str(timing_ms) + "\t" + str(touch.spos[0]) + "\t" + str(touch.spos[1]) + "\t" + 
                        str(touch.pos[0]) + "\t" + str(touch.pos[1]) + "\t" + "cleared" + "\t" + str(touch.pressure) 
                        + "\t" + str(self.pencolor) + "\t" + str(self.line_width) +"\t"+str(Window.size)+ "\n")
                    # save to a file     
                    x = open(name, "a")
                    x.write(to_save_down)
                    self.flag_clear = False

                # then proceed with saving the data and drawing new figure
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

    def check_correction(self):
        self.flag_clear = True

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
            self.ids.between_trial_label.markup = True
            self.ids.between_trial_label.text = """Herzlich Willkommen zu unserer Studie. 
                                                \nIm folgenden Experiment wirst du einige kognitive Aufgaben am Tablet bearbeiten. Dabei ist es wichtig, dass du die Aufgaben so gut wie möglich bearbeitest. Lass Dir Zeit und lasse dich nicht von den anderen Teilnehmer*innen im Raum ablenken oder stressen. 
                                                \nDie Aufgaben, bei denen du [b]zeichnen[/b] musst, [b]müssen unbedingt[/b] mit dem Apple Pencil gelöst werden.
                                                \nDie Fragebogen und andere kognitive Tests sollten mit dem Finger gelöst werden.
                                                \nWenn du bereit bist drücke auf „Weiter“, um mit dem Experiment zu beginnen."""
        elif test_type == 'bNachzeichnen':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nDrücke auf „Weiter“, um die nächste Aufgabe zu starten."""
        elif test_type == 'bReyCopy':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nDrücke auf „Weiter“, um die nächste Aufgabe zu starten."""
        elif test_type == 'bQuest':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nJetzt werden Dir einige Fragebögen zu den Themen Ausbildung, Händigkeit, Erfahrungen mit Tablet und Stift, sowie Konsum von Alkohol, Nikotin, Kaffee und Medikamenten gezeigt. Bitte beantworte die Fragen wahrheitsgemäss. Wenn du einen Fragebogen bearbeitet hast, kannst du mit dem „Fertig“ Button oben rechts zum nächsten Fragebogen gehen.
                                                \nDrücke auf „Weiter“, um die Fragebogen zu starten."""
        elif test_type == 'bMaze':
            self.ids.between_trial_label.markup = True
            self.ids.between_trial_label.text = """Die Fragebogen sind nun fertig! 
                                                \nIn der nächsten Aufgabe muss Du ein Labyrinth mit dem [b]Apple Pencil[/b] lösen. Wichtig dabei ist so schnell und genau wie möglich zu sein.
                                                \nFange unten an und drücke „Fertig“ sobald Du das Labyrinth gelöst hast.
                                                \nBist Du bereit? Drücke auf „Weiter“, um das Labyrinth zu starten."""
        elif test_type == 'bRaven':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nJetzt folgt der Raven-Matrizen-Test um die logische Denkfähigkeiten zu messen.
                                                \nDer Test besteht aus einer Reihe von Aufgaben, bei denen es darum geht, fehlende Teile in Mustern zu identifizieren und zu ergänzen.
                                                \nEs stehen maximal 20 min. Zeit zur Verfügung. Es kommt nicht in erster Linie darauf an, schnell zu sein, sondern möglichst viele von den Aufgaben richtig zu lösen.  
                                                \nWir fangen an mit einer Übungsaufgabe.
                                                \nDrücke auf „Weiter“, um die Übungsaufgabe zu starten."""
        elif test_type == 'bDelayed':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nDrücke auf „Weiter“, um die nächste Aufgabe zu starten."""
        elif test_type == 'bcogTests':
            self.ids.between_trial_label.markup = True
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nNun folgen weitere kognitive Tests. Die Tests werden im Webbrowser durchgeführt.
                                                \nBenutze deinen [b]Finger[/b], um die Tests zu lösen!
                                                \nAm Ende des Tests wirst Du gebeten auf „Completion Code“ zu drücken, um zurück zur „drawing-app“ zu kommen.
                                                \nDrücke auf „Weiter“, um mit den kognitiven Tests zu starten."""
        elif test_type == 'bTaylorCopy':
            self.ids.between_trial_label.markup = True
            self.ids.between_trial_label.text = """Gut gemacht!
                                                \n[b]Die nächste Aufgabe muss auf dem Blatt Papier ausgeführt werden.[/b]
                                                \nNimm jetzt das [b]obere[/b] Blatt Papier und den Stift und zeichne die auf der linken Seite abgebildete [b]Taylor Figur[/b] so präzise wie möglich ab. 
                                                \nWenn du fertig bist, drehe die [b]Taylor Figur[/b] um und lege sie auf die Seite.
                                                \nSobald du die Aufgabe beendet hast, drücke „Weiter“."""
        elif test_type == 'bTaylorRecall':
            self.ids.between_trial_label.markup = True
            self.ids.between_trial_label.text = """Nimm jetzt das [b]zweite[/b] Blatt Papier und den Stift und zeichne die [b]Taylor Figur[/b] so präzise wie möglich [b]aus dem Gedächtnis[/b]. 
                                                \nSobald du die Aufgabe beendet hast, drücke „Weiter“."""
        elif test_type == 'bTestFam':
            self.ids.between_trial_label.text = """Gut gemacht! 
                                                \nNun folgt der letze Fragebogen. Bitte beantworte die Fragen wahrheitsgemäss.
                                                \nDrücke auf „Weiter“, um die nächste Aufgabe zu starten."""
        elif test_type == 'bFinished':
            self.ids.between_trial_label.text = """Die Studie ist nun zu Ende! 
                                                \nVielen Dank für die Teilnahme.
                                                \nDrücke auf „Weiter“, um die Studie zu beenden und wende dich an die Studienleitung."""

    def start_cog_tests(self):
        global test_type
        global link_cog_tests
        if test_type == 'bcogTests':
            username = ApplePenApp.get_running_app().username
            link = link_cog_tests + username
            webbrowser.open(link)

    def save_quest_data(self):
        '''
        save demographics/questionaires to a file
        /Users/dawidstrzelczyk/Library/Application Support/applepen/InfoTable
        '''
        global test_type
        # save data at the end of the study
        if test_type == 'bFinished':
            user_data_dir = App.get_running_app().user_data_dir
            
            # get dict with all scores
            app_instance = ApplePenApp.get_running_app()
            self.quest_dict = ApplePenApp.get_running_app().quest_dict

            # get raven scores
            ravscreen = self.manager.get_screen("ravenscreen")
            # append to dict
            self.quest_dict["raven_scores"] = ravscreen.get_raven_score()
            # get screen centers from each nachzeichnen test
            drscreen = self.manager.get_screen("drawing")
            center_dict = drscreen.get_screen_centers()
            # concat dicts
            self.quest_dict.update(center_dict)
        
            # save to a file
            name = join(user_data_dir, "demographics.txt")
            file_exist = os.path.isfile(name)
            
            x = open(name, "a", newline = '\n')
            # if file does not exisit yet, write a header first
            if not file_exist:
                for key, val in self.quest_dict.items():
                    x.write(str(key) + "\t")
                x.write("\n")
                for key, val in self.quest_dict.items():
                    # retrieve the responses
                    if isinstance(val, StringProperty):
                        response = getattr(app_instance, key, None)
                    else:
                        response = val
                    x.write(str(response) + "\t")
                x.write("\n")
            else:
                for key, val in self.quest_dict.items():
                    # retrieve the responses
                    if isinstance(val, StringProperty):
                        response = getattr(app_instance, key, None)
                    else:
                        response = val
                    x.write(str(response) + "\t")
                x.write("\n")
        else:
            pass


class ScreenManagement(ScreenManager):
    pass   

class ApplePenApp(MDApp):

    # color window to white
    Window.clearcolor = (1, 1, 1, 1)

    # get vars
    username = StringProperty("") # ID
    age = StringProperty("")
    gender = StringProperty("")
    line_width = StringProperty("")

    # handedness
    hand_schreiben = StringProperty("")
    hand_malen = StringProperty("")
    hand_werfen = StringProperty("")
    hand_tischtennis = StringProperty("")
    hand_tennisschlager = StringProperty("")
    hand_hammer = StringProperty("")
    hand_messergabel = StringProperty("")
    hand_messer = StringProperty("")
    hand_gabel = StringProperty("")
    hand_spaghetti = StringProperty("")
    hand_loeffel = StringProperty("")
    hand_handgeben = StringProperty("")

    # education
    edu_ausbildung = StringProperty("")
    edu_jahren = StringProperty("")

    # trust
    trust_tab = StringProperty("")
    trust_tab_freq = StringProperty("")
    trust_pen = StringProperty("")
    trust_pen_freq = StringProperty("")
    trust_tab_faehigkeit = StringProperty("")
    trust_pen_faehigkeit = StringProperty("")

    # drugs
    drugs_alko = StringProperty("")
    drugs_smoke = StringProperty("")
    drugs_coffe = StringProperty("")
    drugs_medis = StringProperty("")
    drugs_medis_list = StringProperty("")

    # test familiarity
    test_rey = StringProperty("")
    test_taylor = StringProperty("")
    test_tmt = StringProperty("")
    test_tower = StringProperty("")
    test_raven = StringProperty("")
    test_spatial = StringProperty("")
    test_adaptive = StringProperty("")
    test_road = StringProperty("")
    test_finger = StringProperty("")

    quest_dict = {
        "username":username,
        "age":age,
        "gender":gender,
        "hand_schreiben":hand_schreiben,
        "hand_malen":hand_malen,
        "hand_werfen":hand_werfen,
        "hand_tischtennis":hand_tischtennis,
        "hand_tennisschlager":hand_tennisschlager,
        "hand_hammer":hand_hammer,
        "hand_messergabel":hand_messergabel,
        "hand_messer":hand_messer,
        "hand_gabel":hand_gabel,
        "hand_spaghetti":hand_spaghetti,
        "hand_loeffel": hand_loeffel,
        "hand_handgeben":hand_handgeben,
        "edu_ausbildung":edu_ausbildung,
        "edu_jahren":edu_jahren,
        "trust_tab":trust_tab,
        "trust_tab_freq":trust_tab_freq,
        "trust_pen":trust_pen,
        "trust_pen_freq":trust_pen_freq,
        "trust_tab_faehigkeit":trust_tab_faehigkeit,
        "drugs_alko":drugs_alko,
        "drugs_smoke":drugs_smoke,
        "drugs_coffe":drugs_coffe,
        "drugs_medis":drugs_medis,
        "drugs_medis_list":drugs_medis_list,
        "test_rey":test_rey,
        "test_taylor":test_taylor,
        "test_tmt":test_tmt,
        "test_tower":test_tower,
        "test_raven":test_raven,
        "test_spatial":test_spatial,
        "test_adaptive":test_adaptive,
        "test_road":test_road,
        "test_finger":test_finger,
    }

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

    def close_app(self):
        global test_type
        if test_type == 'bFinished':   
            self.stop()

    def get_time(self, dt):
        # after 20 min of raven stop the test and switch screens
        # 20 min = 20 * 60 = 1200 s, but add 1 min for example task
        if self.sw_seconds > 1260:
            self.stop_clock()
            self.reset()
            self.raven_time.cancel()
            self.switch_test_type()

    def count_time_raven(self):
        self.raven_time = Clock.schedule_interval(self.get_time, 1) # every second is enough

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
        #print(test_counter)

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
                'bcogTests', 'bTestFam', 'bTaylorCopy', 'bTaylorRecall', 'bFinished']:
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

            # start clock (subjects have 20 min time to complete the task)
            self.reset()
            self.start_clock()
            self.count_time_raven()

        elif test_type == 'TestFam':
            App.get_running_app().root.current = 'testfamscreen'

        else:
            print('nothing happened')



    def build(self):
        presentation = Builder.load_file("applepen_kivy.kv")
        return presentation
       
if __name__=="__main__":
    ApplePenApp().run()


