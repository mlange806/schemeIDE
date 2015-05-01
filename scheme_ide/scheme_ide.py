from subprocess import Popen, PIPE
from tkinter import filedialog
import math
import evaluator as ev
from colorprofile import Colorprofile
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

        self.colorprofile = Colorprofile(self)
        self.create_toolbar(master)
        self.create_editor(master)
        self.create_console(master)

        self.colorprofile_updated()

        self.root = master

    def colorprofile_updated(self):
        self.colorprofile.update_scheme_text(self.editor)
        self.colorprofile.update_scheme_text(self.console)
        if hasattr(self, 'tutorial'):
            self.colorprofile.update_tutorial(self.tutorial)

    def create_toolbar(self, r):
        '''Creates a toolbar with a pull down menu.'''
    
        self.menubar = tk.Menu(self.rightframe)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Open Tutorial", command=self.add_tutorial)
        self.filemenu.add_command(label="Create Tutorial", command=self.create_course)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        colormenu = tk.Menu(self.menubar, tearoff=0)
        colormenu.add_command(label="Load Profile", command=lambda: self.colorprofile.load_profile(self))
        colormenu.add_command(label="Save Profile", command=lambda: self.colorprofile.save_profile(self))
        colormenu.add_separator()
        colormenu.add_command(label="Text", command=lambda: self.colorprofile.pickcolor("text"))
        colormenu.add_command(label="Background", command=lambda: self.colorprofile.pickcolor("background"))
        colormenu.add_command(label="Keywords", command=lambda: self.colorprofile.pickcolor("keyword"))
        colormenu.add_command(label="Operators", command=lambda: self.colorprofile.pickcolor("operator"))
        colormenu.add_command(label="Parenthesis", command=lambda: self.colorprofile.pickcolor("paren_highlight"))
        colormenu.add_command(label="Selected Reference", command=lambda: self.colorprofile.pickcolor("ref_selected"))
        colormenu.add_command(label="Highlighted Reference", command=lambda: self.colorprofile.pickcolor("ref_highlight"))
        self.menubar.add_cascade(label="Colors", menu=colormenu)

        self.menubar.add_command(label="Run", command=self.run_code)

        r.config(menu=self.menubar)

    def create_editor(self, r):
        '''Creates a text box that a user can type code into.'''

        self.editor = SchemeTextLineNumbered(master=self.rightframe,
                reference_highlighting_callback = ev.reference_highlight, height=20, width=40)
        self.editor.pack(fill=tk.BOTH, expand=1)
        
    def create_console(self, r):
        '''Creates a console for program output.'''

        self.console = SchemeShell(master=self.rightframe,height=10,width=60)
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
            self.colorprofile_updated()
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

    def create_course(self):
        '''Form input that creates a course file.'''
    
        t = tk.Toplevel(self)
        t.wm_title("Create Tutorial")

        frame = tk.Frame(t)
        frame.pack(side='top')
        course_name = tk.Label(frame, text="Course Name: ", width=15)
        course_name.pack(side="left")
        course_input = tk.Text(frame, height=1, width=30)
        course_input.pack(side="left")

        seperator = ''
        for x in range(80): seperator = seperator + '_'
        w = tk.Label(t, text=seperator)
        w.pack(side='top')

        frame = tk.Frame(t)
        frame.pack(side='top')
        lesson_name = tk.Label(frame, text="Lesson Name: ", width=15)
        lesson_name.pack(side="left")
        lesson_input = tk.Text(frame, height=1, width=30)
        lesson_input.pack(side="left")

        w = tk.Label(t, text=seperator)
        w.pack(side='top')

        frame = tk.Frame(t)
        frame.pack(side='top')
        section_name = tk.Label(frame, text="Section Name: ", width=15)
        section_name.pack(side="left")
        section_input = tk.Text(frame, height=1, width=30)
        section_input.pack(side="left")

        frame = tk.Frame(t)
        frame.pack(side='top')
        instr_name = tk.Label(frame, text="Instructions: ", width=15)
        instr_name.pack(side="left")
        instr_input = tk.Text(frame, height=5, width=30)
        instr_input.pack(side="left")
        
        frame = tk.Frame(t)
        frame.pack(side='top')
        add_section = tk.Button(frame, text='+ Add Section')
        add_section.pack(side='left')

        w = tk.Label(t, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(t)
        frame.pack(side='top')
        add_lesson = tk.Button(frame, text='+ Add Lesson')
        add_lesson.pack(side='left')
        
        w = tk.Label(t, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(t)
        frame.pack(side='top')
        save = tk.Button(frame, text='Save Course')
        save.pack(side='left')
       
          
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    root.title('Scheme IDE')
    app = SchemeIDE(master=root)
    app.mainloop()


