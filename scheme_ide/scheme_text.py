import tkinter as tk

class SchemeText(tk.Text):
    '''
    Scheme Text
    
<<<<<<< HEAD
=======
    
>>>>>>> noah
    Text widget that does (basic) keyword coloring for Scheme text.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets the values of the tags and key press handler.'''
<<<<<<< HEAD
        super(SchemeEditor, self).__init__(*args, **kwargs)
=======
        tk.Text.__init__(self, *args, **kwargs)
>>>>>>> noah
        self.tag_configure("red", foreground="#ff0000")
        self.tag_configure("blue", foreground="#0000ff")
        self.tag_configure("green", foreground="#00ff00")
        self.bind("<KeyRelease>", self.key)
<<<<<<< HEAD
        self.key(EventStub('a'))
        
=======

>>>>>>> noah
    def highlight_pattern(self, pattern, tag):
        '''Colors pattern with the color from tag.'''
        self.mark_set("matchStart", '1.0')
        self.mark_set("matchEnd", '1.0')
        self.mark_set("searchLimit", self.index("end"))

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
<<<<<<< HEAD
                                count=count)
=======
                                count=count).strip()
>>>>>>> noah
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def key(self, event):
        '''Updates the text color on key presses.'''
<<<<<<< HEAD
=======
        #print(self.index(tk.INSERT))
>>>>>>> noah

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
<<<<<<< HEAD

class EventStub: 
    '''Pretend event stub for methods that take an event argument.'''
    def __init__(self, c):        
        self.char = c


=======
>>>>>>> noah
