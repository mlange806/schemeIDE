import tkinter as tk

class Tutorial(tk.Frame):
    def __init__(self, shell, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='black', *args, **kwargs)
        bottomframe = tk.Frame(self, bg='black')
        bottomframe.pack(side='bottom')

        self.shell = shell

        self.title = tk.Text(self, height=1, bg='black', fg='white', width=50, borderwidth=0)
        self.title.insert('end', 'Lesson 0')
        self.title.config(state='disabled')

        self.instr = tk.Text(self, height=40, bg='black', fg='white', width=50)
        self.instr.insert('end', 'Type 4 in the shell an press enter.\n')
        self.instr.config(state='disabled')

        self.check = tk.Button(bottomframe, text='Check Answer', bg='black', fg='white', width=10, height=3, command=self.check_result)
        self.feedback = tk.Text(bottomframe, height=3, bg='black', fg='white', width=40, borderwidth=0)
        self.feedback.insert('end', 'You have not submitted an answer yet...')
        self.feedback.config(state='disabled')
        
        self.title.pack(side='top')
        self.instr.pack(side='top')
        self.check.pack(side='left')
        self.feedback.pack(side='left')

    def check_result(self):
        shell = self.shell
        result = int(shell.get_result())
        if result == 4:
            self.set_all("Correct!")
        else:  
            self.set_all("Incorrect!")
       
    def set_all(self, string):
        # Sets the contents of the text box to this string.
        self.feedback.config(state='normal')
        self.feedback.delete(1.0, tk.END)
        self.feedback.insert(1.0, string)
        self.feedback.config(state='disabled')
