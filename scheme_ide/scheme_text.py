import tkinter as tk

class SchemeText(tk.Text):
    '''
    Scheme Text
    
    Text widget that does (basic) keyword coloring for Scheme text.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets the values of the tags and key press handler.'''

        tk.Text.__init__(self, *args, **kwargs)
        self.tag_configure("paren", foreground="#ff0000")
        self.tag_configure("keyword", foreground="#0000ff")
        self.tag_configure("operator", foreground="#00ff00")
        self.bind("<KeyRelease>", self.key)

    def configure_colors(self, background=None, text=None, \
                        keyword=None, operator=None):
        if background != None: self.configure(background=background)
        if text != None: self.configure(foreground=text)
        if keyword != None: self.tag_configure("keyword", foreground=keyword)
        if operator != None: self.tag_configure("operator", foreground=operator)

    def highlight_pattern(self, pattern, tag):
        '''Colors pattern with the color from tag.'''
        self.mark_set("matchStart", '1.0')
        self.mark_set("matchEnd", '1.0')
        self.mark_set("searchLimit", self.index("end"))

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count).strip()
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def key(self, event):
        '''Updates the text color on key presses.'''
        #print(self.index(tk.INSERT))

        #Start with a blank slate.
        self.tag_remove("paren", '1.0', 'end')
        self.tag_remove("keyword", '1.0', 'end')
        self.tag_remove("operator", '1.0', 'end')    
        
        #Do keyword highlighting.
        self.highlight_pattern("(", "paren")
        self.highlight_pattern(")", "paren")
        self.highlight_pattern("define", "keyword")
        self.highlight_pattern("lambda", "keyword")
        self.highlight_pattern("+", "operator")
        self.highlight_pattern("-", "operator")  
        self.highlight_pattern("*", "operator")
        self.highlight_pattern("/", "operator")

    def set_all(self, string):
        # Sets the contents of the text box to this string.
        self.delete(1.0, tk.END)
        self.insert(1.0, string)

    def get_all(self):
        # Returns full contents of the text box.
        return self.get(1.0, tk.END)

