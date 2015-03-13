from scheme_editor import SchemeEditor
import evaluator as ev

class SchemeShell(SchemeEditor):
    '''
    Scheme Shell

    Shell widget that allows a user to type a line of Scheme and evaluate it.
    '''

    def __init__(self, *args, **kwargs):
        super(SchemeShell, self).__init__(*args, **kwargs)
        
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
        pos = str(self.line) + '.3'     

        if event.char == '\r':
            pos = str(self.line)+'.3'
            out = self.get(pos, 'end')
            out = ev.evaluate(out)

            self.insert('end', str(out)+'\n')
            self.new_line()

        #Text highlighting.
        self.key(event)

    def _onKey(self, event):
        pos = str(self.line) + '.3'       
        insert_collumn = int(self.index('insert').split('.')[1])
        
        #Prevents user from inserting text where they shouldn't.
        if insert_collumn < 3:
            return 'break'        

    
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
        self.insert('end', '>> ')
        self.line = self.line + 2
          



