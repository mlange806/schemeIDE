import tkinter as tk
from subprocess import Popen, PIPE
from tkinter import filedialog
import evaluator as ev

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
        self.editor = SchemeEditor(r, height=20, width=60, bg='black', \
                                 fg='white', insertbackground='blue')
        self.editor.pack()
        
    def create_console(self, r):
        '''Creates a console for program output.'''
        self.console = SchemeShell(r,height=10,width=60,bg='black',fg='white')
        self.console.pack()

    def run_code(self):
        '''Evaluates Scheme expression in editor and displays result in console.'''

        exp = self.editor.get("1.0", 'end')
        print(repr(exp))
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

class SchemeShell(tk.Text):
    '''
    Scheme Shell

    Shell widget that allows a user to type a line of Scheme and evaluate it.
    '''

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.line = 1

        self.insert('end', '-> ')
        self.bind("<KeyRelease>", self._key)
        self.bind("<BackSpace>", self._backspace)

    def _backspace(self, event):
        '''Prevents the user from deleting previous information.'''
        pos = str(self.line) + '.3'

        if self.index('insert') == pos:
            return 'break'
        

    def _key(self, event):
        if event.char == '\r':
            pos = str(self.line)+'.3'
            out = self.get(pos, 'end')
            out = ev.evaluate(out)
            self.insert('end', str(out)+'\n')
            self.new_line()
    
    def run(self, exp):
        '''Runs the expression in the console and shows the result.'''
        try:
            output = ev.evaluate(exp)  
            self.insert('end', 'run\n')  
            self.insert('end', str(output))
            self.insert('end', '\n')
        except:
            self.insert('end', 'Error!')
            self.insert('end', '\n')
        self.new_line()
    
    def new_line(self):
        self.insert('end', '-> ')
        self.line = self.line + 2

class SchemeEditor(tk.Text):
    '''
    Scheme Text
    
    Text widget that does (basic) keyword coloring for Scheme text.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets the values of the tags and key press handler.'''
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_configure("red", foreground="#ff0000")
        self.tag_configure("blue", foreground="#0000ff")
        self.tag_configure("green", foreground="#00ff00")
        self.bind("<KeyRelease>", self.key)
        
    def highlight_pattern(self, pattern, tag):
        '''Colors pattern with the color from tag.'''
        self.mark_set("matchStart", '1.0')
        self.mark_set("matchEnd", '1.0')
        self.mark_set("searchLimit", self.index("end"))

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def key(self, event):
        '''Updates the text color on key presses.'''

        #Start with a blank slate.
        self.tag_remove("red", '1.0', 'end')
        self.tag_remove("blue", '1.0', 'end')
        self.tag_remove("green", '1.0', 'end')    
        
        #Do keyword highlighting.
        self.highlight_pattern("(", "red")
        self.highlight_pattern(")", "red")
        self.highlight_pattern("define", "blue")
        self.highlight_pattern("lambda", "blue")
        self.highlight_pattern("+", "green")
        self.highlight_pattern("-", "green")  
        self.highlight_pattern("*", "green")
        self.highlight_pattern("/", "green")

    def set_all(self, string):
        # Sets the contents of the text box to this string.
        self.delete(1.0, tk.END)
        self.insert(1.0, string)

    def get_all(self):
        # Returns full contents of the text box.
        return self.get(1.0, tk.END)

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

