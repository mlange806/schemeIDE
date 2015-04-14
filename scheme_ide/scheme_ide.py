from subprocess import Popen, PIPE
from tkinter import filedialog
import math
import evaluator as ev
from scheme_shell import *
from scheme_text_line_numbered import *
from tutorial import *

class SchemeIDE(tk.Frame):
    '''
    Scheme IDE

    This is the main application window.   
    '''

    def __init__(self, master=None):
        '''Creates the application and its widgets.'''

        tk.Frame.__init__(self, master)
        self.master = master
        master.maxsize(width=450, height=450)
        master.resizable(width='false', height='false')

        self.state = 0
        
        self.rightframe = tk.Frame(master)
        self.leftframe = tk.Frame(master)
        self.rightframe.pack(side='right')
        self.leftframe.pack(side='left')

        self.create_toolbar(master)
        self.create_editor(master)
        self.create_console(master)
        self.root = master
  
    def create_toolbar(self, r):
        '''Creates a toolbar with a pull down menu.'''
    
        self.menubar = tk.Menu(self.rightframe)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Open Tutorial", command=self.add_tutorial)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.menubar.add_command(label="Run", command=self.run_code)

        r.config(menu=self.menubar)

    def create_editor(self, r):
        '''Creates a text box that a user can type code into.'''

        self.editor = SchemeTextLineNumbered(master=self.rightframe, height=20, width=40, bg='black', \
                                 fg='white', insertbackground='blue')
        self.editor.pack(fill=tk.BOTH, expand=1)
        
    def create_console(self, r):
        '''Creates a console for program output.'''

        self.console = SchemeShell(master=self.rightframe,height=10,width=60,bg='black',fg='white',insertbackground='blue')
        self.console.pack(fill=tk.BOTH, expand=1)

    def run_code(self):
        '''Evaluates Scheme expression in editor and displays result in console.'''

        exp = self.editor.get("1.0", tk.END)
        self.console.run(exp)

    def open_file(self, testMode=False, path=None):
        '''Creates an open file window and sets the contents of the editor to the file.'''
        
        if not testMode: path = tk.filedialog.askopenfilename(parent=self)
        if path == None: return
        file = open(path, "r")
        self.editor.set_all(file.read())
        file.close()

    def save_file(self, testMode=False, path=None):
        '''Creates a save fie window and saves the contents of the editor to the path specified.'''

        if not testMode: path = tk.filedialog.asksaveasfilename(parent=self)
        if path == None: return
        file = open(path, "w")
        file.write(self.editor.get_all())
        file.close()

    def add_tutorial(self):
        '''Creates the tutorial widget if not created and closes it if it is visible.'''

        if self.state == 0:
            self.master.maxsize(width=1000, height=400)           
            self.tutorial = Tutorial(self.console, master=self.leftframe)
            self.tutorial.pack()
            self.filemenu.entryconfigure(2, label="Close Tutorial")
            self.state = 1 

        elif self.state == 1:
            self.tutorial.pack_forget()
            self.master.maxsize(width=450, height=400)
            self.filemenu.entryconfigure(2, label="Open Tutorial")
            self.state = 2

        elif self.state == 2:
            self.tutorial.load_course()
            self.master.maxsize(width=1000, height=400)   
            self.tutorial.pack()    
            self.filemenu.entryconfigure(2, label="Close Tutorial")
            self.state = 1
       
          
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    root.title('Scheme IDE')
    app = SchemeIDE(master=root)
    app.mainloop()


