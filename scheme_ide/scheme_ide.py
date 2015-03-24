import tkinter as tk
from subprocess import Popen, PIPE
from tkinter import filedialog
import math
import evaluator as ev
from scheme_shell import *
from scheme_editor import *

class SchemeIDE(tk.Frame):
    '''
    Scheme IDE

    This is the main application window.   
    '''

    def __init__(self, master=None):
        '''Creates the application and its widgets.'''
        tk.Frame.__init__(self, master)
        master.minsize(width=300, height=300)
        self.create_toolbar(master)
        self.create_editor(master)
        self.create_console(master)

    def create_toolbar(self, r):
        menubar = tk.Menu(r)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=filemenu)

        menubar.add_command(label="Run", command=self.run_code)

        r.config(menu=menubar)

    def create_editor(self, r):
        '''Creates a text box that a user can type code into.'''
        self.editor = SchemeEditor(master=r, height=20, width=40, bg='black', \
                                 fg='white', insertbackground='blue')
        self.editor.pack(fill=tk.BOTH, expand=1)
        
    def create_console(self, r):
        '''Creates a console for program output.'''
        self.console = SchemeShell(master=r,height=10,width=60,bg='black',fg='white')
        self.console.pack(fill=tk.BOTH, expand=1)

    def run_code(self):
        '''Evaluates Scheme expression in editor and displays result in console.'''

        exp = self.editor.get("1.0", tk.END)
        self.console.run(exp)

    def open_file(self, testMode=False, path=None):
        
        if not testMode: path = tk.filedialog.askopenfilename(parent=self)
        if path == None: return
        file = open(path, "r")
        self.editor.set_all(file.read())
        file.close()

    def save_file(self, testMode=False, path=None):
        if not testMode: path = tk.filedialog.asksaveasfilename(parent=self)
        if path == None: return
        file = open(path, "w")
        file.write(self.editor.get_all())
        file.close()

class LineNumsText(tk.Text):
    def __init__(self, *args, **kwargs):
        # Make sure only keyword args are used here
        if len(args) > 0:
            raise Exception("lineNumsText: Only keyword arguments"
                            " should be used for initialization.")

        # Create a frame
        self.frame = tk.Frame(kwargs["master"], bd=2, relief=tk.SUNKEN)

        # Create the scrollbar component
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(fill='y', side=tk.RIGHT)

        # Create the line number text component
        self.linetext = tk.Text(self.frame,
                height = 1,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'grey',
                foreground = 'white',
                state='disabled')
        self.linetext.pack(side=tk.LEFT, fill='y')

        # Create the main text component
        kwargs["master"] = self.frame
        kwargs["padx"] = 4
        tk.Text.__init__(self, *args, **kwargs)
        tk.Text.pack(self, side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Set up the scrollbar
        self.lastPosition = 0
        self.dropupdate = False
        def updateposition(position):
            #print("updateposition: " + str(position))
            if self.dropupdate:
                self.dropupdate = False
                return
            self.yview("moveto", str(position))
            self.linetext.yview("moveto", str(position))
            self.lastPosition = position
        def textviewchange(*args):
            #print("textviewchange: " + str(args))
            updateposition(float(args[0]))
            self.scrollbar.set(*args)
        def scrollviewchange(*args):
            #print("scrollviewchange: " + str(args))
            self.yview(*args)
            self.linetext.yview(*args)
        self.config(yscrollcommand=textviewchange)
        self.linetext.config(yscrollcommand=textviewchange)
        self.scrollbar.config(command=scrollviewchange)

        # Kickstart the line number updates
        self.update_line_numbers()

    def update_line_numbers(self):
        def display_lines_for_actual_line(actual_line, available_pixels):
            def get_residual(string, available_pixels):
                whitespace_tally = 0

                for index, character in enumerate(string):
                    if character.isspace():
                        available_pixels -= whitespace_tally * 7
                        available_pixels -= 1
                        whitespace_tally = 1
                    else:
                        available_pixels -= whitespace_tally * 7
                        whitespace_tally = 0
                        available_pixels -= 8

                    if available_pixels < 0: return string[index:]

                return None

            line_count = 0
            residual = actual_line
            while True:
                residual = get_residual(residual, available_pixels)
                line_count += 1
                if residual == None: break
                
            return line_count
        
        def generate_line_numbers(tktext):
            available_pixels = tktext.winfo_width() - 10
            actual_lines = tktext.get(1.0, tk.END).split("\n")[:-1]

            output = ""
            counter = 1
            for actual_line in actual_lines:
                display_line_count = display_lines_for_actual_line(actual_line, available_pixels)
                
                if(counter > 1): output += "\n"
                output += str(counter)
                for i in range(1, display_line_count):
                    output += "\n"
                counter += 1
            
            return output

        data = generate_line_numbers(self)
        self.linetext.config(state='normal')
        self.linetext.delete('1.0', tk.END)
        self.linetext.insert('1.0', data)
        self.linetext.config(state='disabled')

        self.linetext.yview("moveto", str(self.lastPosition))
        self.dropupdate = True

        self.after(100, self.update_line_numbers)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

class Tutorial(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='black', *args, **kwargs)
        bottomframe = tk.Frame(self, bg='black')
        bottomframe.pack(side='bottom')

        self.title = tk.Text(self, height=1, bg='black', fg='white', width=50, borderwidth=0)
        self.title.insert('end', 'Lesson')
        self.title.config(state='disabled')

        self.instr = tk.Text(self, height=15, bg='black', fg='white', width=50)
        self.instr.insert('end', 'Here is sample instructions\n    1. Do this.\n    2. Then do this\n\nPress the Check Answer button when you are\nfinished.')
        self.instr.config(state='disabled')

        self.check = tk.Button(bottomframe, text='Check Answer', bg='black', fg='white', width=10, height=3)
        self.feedback = tk.Text(bottomframe, height=3, bg='black', fg='white', width=40, borderwidth=0)
        self.feedback.insert('end', 'You have not submitted an answer yet...')
        self.feedback.config(state='disabled')
        
        self.title.pack(side='top')
        self.instr.pack(side='top')
        self.check.pack(side='left')
        self.feedback.pack(side='left')
          
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    root.title('Scheme IDE')
    app = SchemeIDE(master=root)
    app.mainloop()

