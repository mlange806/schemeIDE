import tkinter as tk
import evaluator as ev
from tkinter import filedialog
import os
import importlib

class Tutorial(tk.Frame):
    '''
    Tutorial Widget
    
    Currently tests defined Scheme functions for correct functionality.
    '''

    def __init__(self, shell, master=None, *args, **kwargs):
        '''Constructor that loads the course and sets up everything.'''    

        tk.Frame.__init__(self, master, bg='black', *args, **kwargs)
        titleframe = tk.Frame(self, bg='black')
        bottomframe = tk.Frame(self, bg='black')
        titleframe.pack(side='top')
        bottomframe.pack(side='bottom')

        self.shell = shell
        self.section_no = 1
        self.lesson_no = 1
            
        #Create the title frame
        self.title = tk.Text(titleframe, height=1, bg='black', fg='white', width=30, borderwidth=0)       
        self.title.config(state='disabled')

        self.menu_option = tk.StringVar(self)
        self.menu_option.set('')
        self.menu_option.trace("w", self.set_lesson)
        self.ops = ['wow']
        
        self.lesson_sel = tk.OptionMenu(titleframe, self.menu_option, self.ops)
        self.lesson_sel.config(bg = "BLACK", fg = "WHITE", bd=0, highlightbackground='black')

        self.prev = tk.Button(titleframe, text='<-', bg='black', fg='white', width=4, height=1, command=self.next_section)
        self.next = tk.Button(titleframe, text='->', bg='black', fg='white', width=4, height=1, command=self.next_section)
 
        self.title.pack(side='left')
        self.lesson_sel.pack(side='left')
        self.prev.pack(side='left')
        self.next.pack(side='left')

        #Create instruction section
        self.instr = tk.Text(self, height=40, bg='black', fg='white', width=50)
        self.instr.config(state='disabled')
        self.instr.pack(side='top')        

        #Create the bottom frame
        self.check = tk.Button(bottomframe, text='Check Answer', bg='black', fg='white', width=10, height=3, command=self.check_result)    
        self.feedback = tk.Text(bottomframe, height=3, bg='black', fg='white', width=40, borderwidth=0)
        self.feedback.insert('end', 'You have not submitted an answer yet...')
        self.feedback.config(state='disabled')
            
        self.check.pack(side='left')
        self.feedback.pack(side='left')

        self.load_course()

    def load_course(self):
        #Get the course information here.          
        path = tk.filedialog.askopenfilename(parent=self, initialdir=os.path.realpath('scheme_ide/courses'))
        name = os.path.basename(path)
        name = os.path.splitext(name)[0]
        module = __import__('courses.'+name, fromlist=[''])

        self.course = module.course
        title = self.course[0]
        lesson = self.course[1][0]
        section = self.course[1][1][0]
        instr = self.course[1][1][1][0]
        
        self.title.config(state='normal')
        self.title.delete('1.0', 'end')
        self.title.insert('end', title)

        self.instr.config(state='normal')
        self.instr.delete('1.0', 'end')
        self.instr.insert('end', section+'\n\n'+instr)

        self.ops = self._get_lessons(self.course)
        self.menu_option.set(lesson)
        self.lesson_sel['menu'].delete(0, 'end')

        for choice in sorted(list(self.ops)):
            self.lesson_sel['menu'].add_command(label=choice, command=tk._setit(self.menu_option, choice))      

    def set_lesson(self, *args):
        '''Set the tutorial screen to the new lesson chosen in the menu.'''
       
        try:
            self.lesson_no = self.ops[self.menu_option.get()]
            # Get the course information here.
            section = self.course[self.lesson_no][self.section_no][0]
            instr = self.course[self.lesson_no][self.section_no][1][0]

            # Sets the contents of the instr box.
            self.instr.config(state='normal')
            self.instr.delete(1.0, tk.END)
            self.instr.insert(1.0, section+'\n\n'+instr)
            self.instr.config(state='disabled')

            # Reset the feedback box.
            self.set_all('You have not submitted an answer yet...')

        except:
            # If an exception occurs, it is because the course is first being loaded and menu option has no meaningful data yet.
            pass
        

    def check_result(self):        
        '''Loads the test function from the course data and tests the scheme function specified in instructions.'''

        if self.course[self.lesson_no][self.section_no][1][1] == '<value-test>':
            #Tests that the last value computed is equal to the epected value.
            value = self.course[self.lesson_no][self.section_no][1][2]

            if self.shell.get_result() == str(value): 
                self.set_all("Correct!")
            else:  
                self.set_all("Incorrect!")

        else:
            #Tests that a function returns the expected value for a set test inputs.
            tester = self.course[self.lesson_no][self.section_no][1][2]
            funct =  self.course[self.lesson_no][self.section_no][1][1]       

            def f(x):
                return ev.evaluate('('+funct+' '+str(x)+')')

            if tester(f):
                self.set_all("Correct!")
            else:  
                self.set_all("Incorrect!")

    def next_section(self):
        '''Goes to the next section in the current lesson. Once it reaches the last section, it resets back to the first.'''

        if self.section_no < (len(self.course[1]) - 1): 
            self.section_no =  self.section_no + 1
        else:
            self.section_no = 1

        # Get the course information here.
        section = self.course[self.lesson_no][self.section_no][0]
        instr = self.course[self.lesson_no][self.section_no][1][0]

        # Sets the contents of the instr box.
        self.instr.config(state='normal')
        self.instr.delete(1.0, tk.END)
        self.instr.insert(1.0, section+'\n\n'+instr)
        self.instr.config(state='disabled')

        # Reset the feedback box.
        self.set_all('You have not submitted an answer yet...')

    def prev_section(self):
        '''Goes to the previous section in the current lesson. Once it reaches the first section, it resets back to the last.'''

        if self.section_no >= (len(self.course[1]) - 1): 
            self.section_no =  self.section_no - 1
        else:
            self.section_no = len(self.course[1]) - 1

        # Get the course information here.
        section = self.course[self.lesson_no][self.section_no][0]
        instr = self.course[self.lesson_no][self.section_no][1][0]

        # Sets the contents of the instr box.
        self.instr.config(state='normal')
        self.instr.delete(1.0, tk.END)
        self.instr.insert(1.0, section+'\n\n'+instr)
        self.instr.config(state='disabled')

        # Reset the feedback box.
        self.set_all('You have not submitted an answer yet...')
             
    def set_all(self, string):
        '''Sets the feedback box to string.'''

        # Sets the contents of the text box to this string.
        self.feedback.config(state='normal')
        self.feedback.delete(1.0, tk.END)
        self.feedback.insert(1.0, string)
        self.feedback.config(state='disabled')

    def _get_lessons(self, data):
        '''Takes an array of course data and returns an dict of all lessons in the course with their index.'''
        
        lessons = {}

        for x in range(1, len(data)):
            lessons[data[x][0]] = x

        return lessons
            



