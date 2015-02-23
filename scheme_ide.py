import tkinter as tk
from subprocess import Popen, PIPE
from tkinter import filedialog
import evaluator as ev

class SchemeIDE(tk.Frame):
    '''
    Scheme IDE

    This is the main application window.   
    IMPORTANT: Currently only runs Python code for demo purposes.
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
        self.editor = SchemeText(r, height=20, width=60, bg='black', \
                                 fg='white', insertbackground='blue')
        self.editor.pack()
        
    def create_console(self, r):
        '''Creates a console for program output.'''
        self.console = tk.Text(r,height=10,width=60,bg='black',fg='white')
        self.console.insert(tk.END, '-> ');
        self.console.config(state=tk.DISABLED)
        self.console.pack()

    def run_code(self):
        '''Runs (python) code in editor and displays stdout in console.'''

        exp = self.editor.get("1.0", tk.END)

        try:
            output = ev.evaluate(exp)    
            self.console.config(state=tk.NORMAL)
            self.console.insert('end', output)
            self.console.insert('end', '\n')
        except:
            self.console.insert('end', 'Error!')
            self.console.insert('end', '\n')

        self.console.insert(tk.END, '-> ')
        self.console.config(state=tk.DISABLED)

    def open_file(self):
        path = tk.filedialog.askopenfilename(parent=self)
        if path == None: return
        file = open(path, "r")
        self.editor.set_all(file.read())
        file.close()

    def save_file(self):
        path = tk.filedialog.asksaveasfilename(parent=self)
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
        self.line = 1
        tk.Text.__init__(self, *args, **kwargs)
        self.insert('end', '-> ')
        self.bind("<Key>", self._key)

    def _key(self, event):
        if event.char == '\r':
            print(self.get(str(self.line)+'.3', 'end'))
            self.line = self.line + 1
            self.insert('end', '\n')
            self.insert('end', '-> ')
            self.mark_set('insert', '1.3')

class SchemeText(tk.Text):
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

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    root.title('Scheme IDE Beta Version')
    app = SchemeIDE(master=root)
    app.mainloop()

