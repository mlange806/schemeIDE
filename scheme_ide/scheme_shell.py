from scheme_text import SchemeText
import evaluator as ev
import re
import string
import tkinter as tk

class SchemeShell(SchemeText):
    '''
    Scheme Shell

    Shell widget that allows a user to type a line of Scheme and evaluate it.
    '''

    def __init__(self, *args, **kwargs):
        '''Constructor for Shell object initialization.'''

        scrollbar = tk.Scrollbar(kwargs['master'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        super(SchemeShell, self).__init__(yscrollcommand=scrollbar.set, *args, **kwargs)
        
        self.line = 1

        self.insert('end', '>> ')
        self.bind("<KeyRelease>", self._key)
        self.bind("<Key>", self._onKey)
        self.bind("<BackSpace>", self._backspace)
        self.bind("<Delete>", self._backspace)

    def _backspace(self, event):
        '''Prevents the user from deleting previous information.'''

        pos = str(self.line) + '.3'
        insert_collumn = int(self.index('insert').split('.')[1])

        #Handled selection issue.
        if self.tag_ranges("sel"):
            print('here')
            sel_collumn = int(self.index('sel.first').split('.')[1])
            if sel_collumn < 3:
                self.delete(pos, 'sel.last')
                return 'break'

        #Prevents user from deleting text they shouldn't delete.
        if insert_collumn < 3:
            return 'break'

        if self.index('insert') == pos:
            return 'break'
        self.key(event)
        
    def _key(self, event):
        '''Handles event on key release.'''

        pos = str(self.line) + '.3'     

        if event.char == '\r':
            pos = str(self.line)+'.3'
            out = self.get(pos, 'end')

            #Handles special case of no alphanum input.
            if re.search('[a-zA-Z0-9'+str(string.punctuation)+']', out): 
                try: out = ev.evaluate(out)
                except: out = 'Error!'
                self.insert('end', str(out)+'\n')
                self.new_line()
                self.see(tk.END)
            else: self.new_line(output=False)

        #Text highlighting.
        self.key(event)

    def _onKey(self, event):
        '''Handles event of key press.'''

        pos = str(self.line) + '.3'       
        insert_collumn = int(self.index('insert').split('.')[1])
        
        #Prevents user from inserting text where they shouldn't.
        if insert_collumn < 3:
            return 'break'

    def run(self, exp):
        '''Runs the expression in the editor and shows the result.'''

        self.insert('end', 'run\n') 
        try:
            output = ev.evaluate(exp)   
            self.insert('end', str(output))
            self.insert('end', '\n')
        except:
            self.insert('end', 'Error!')
            self.insert('end', '\n')
        self.new_line()
        self.see(tk.END)
    
    def new_line(self, output=True):
        '''Creates new prompt arrows in the correct place.'''        

        if output:        
            self.insert('end', '>> ')
            self.line = self.line + 2
        else:  
            self.insert('end', '>> ')
            self.line = self.line + 1
    
    def get_result(self):
        '''Will return the value of the last evaluated result.'''

        return self.get(str(self.line - 1)+'.0', str(self.line)+'.0').rstrip('\n')      



