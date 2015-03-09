from tkinter import *
import tkinter as tk
import math

root = Tk()

class EditorClass(object):

    UPDATE_PERIOD = 100 #ms

    updateId = None

    def __init__(self, master):
        self.lineNumbers = ''
        self.lastViewCmd = None

        # A frame to hold the three components of the widget.
        self.frame = Frame(master, bd=2, relief=SUNKEN)

        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)

        # The Text widget holding the line numbers.
        self.lnText = Text(self.frame,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'lightgrey',
                foreground = 'magenta',
                state='disabled'
        )
        self.lnText.pack(side=LEFT, fill='y')

        # The Main Text Widget
        self.text = Text(self.frame,
                width=16,
                bd=0,
                padx = 4,
                undo=True,
                background = 'white'
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)

        def my_textviewchange(*args):
            self.vScrollbar.set(*args)

        def my_scrollviewchange(*args):
            self.lastViewCmd = args
            self.text.yview(*args)
            self.lnText.yview(*args)

        #self.text.config(yscrollcommand=self.vScrollbar.set)
        self.text.config(yscrollcommand=my_textviewchange)
        #self.vScrollbar.config(command=self.text.yview)
        self.vScrollbar.config(command=my_scrollviewchange)

        self.update_line_numbers()

    def get_full_line_numbers(self, text):
        # Get characters_per_line
        def get_characters_per_line(text):
            base_width = 8
            char_width = 8
            print(text.winfo_width())
            return int((text.winfo_width() - base_width) / char_width)
        characters_per_line = get_characters_per_line(text)
        if characters_per_line == 0: return ""

        # Generate the line numbers
        counter = 1
        output = ""

        for line_data in text.get(1.0, tk.END).split("\n")[:-1]:
            lines_needed = math.ceil(len(line_data) / characters_per_line)
            
            #print("line: " + line_data + "lines_needed: " + str(lines_needed))
            if(counter > 1): output += "\n"
            output += str(counter)
            for i in range(1, lines_needed):
                output += "\n"
            counter += 1
        
        return output

    def update_line_numbers(self):
        data = self.get_full_line_numbers(self.text)
        self.lnText.config(state='normal')
        self.lnText.delete('1.0', END)
        self.lnText.insert('1.0', data)
        self.lnText.config(state='disabled')

        if self.lastViewCmd != None:
            self.lnText.yview(*self.lastViewCmd)

        self.updateId = self.text.after(
            self.UPDATE_PERIOD,
            self.update_line_numbers)

def demo(noOfLines):

    pane = PanedWindow(root, orient=HORIZONTAL, opaqueresize=True)

    ed = EditorClass(root)
    pane.add(ed.frame)

    s = 'line ................................... %s'
    s = '\n'.join( s%i for i in range(1, noOfLines+1) )
    
    ed.text.insert(END, s)

    pane.pack(fill='both', expand=1)

    root.title("Example - Line Numbers For Text Widgets")


if __name__ == '__main__':

    demo(1000)
    mainloop()
