import tkinter as tk
from subprocess import Popen, PIPE
from scheme_shell import SchemeShell
from scheme_editor import SchemeEditor

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
        self.console = SchemeShell(r,height=10,width=60,bg='black',fg='white', insertbackground='blue', borderwidth=0)
        self.console.pack()

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


