import tkinter as tk

class LineNumsText(tk.Text):
    def __init__(self, *args, **kwargs):
        # Make sure only keyword args are used here
        if len(args) > 0:
            raise Exception("lineNumsText: Only keyword arguments"
                            " should be used for initialization.")

        # Create a frame
        self.frame = tk.Frame(kwargs["master"], bd=2, relief=tk.SUNKEN)

        # Create the scrollbar component
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(fill='y', side=tk.RIGHT)

        # Create the line number text component
        self.linetext = tk.Text(self.frame,
                height = 1,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'grey',
                foreground = 'white',
                state='disabled')
        self.linetext.pack(side=tk.LEFT, fill='y')

        # Create the main text component
        kwargs["master"] = self.frame
        kwargs["padx"] = 4
        tk.Text.__init__(self, *args, **kwargs)
        tk.Text.pack(self, side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Set up the scrollbar
        self.lastPosition = 0
        self.dropupdate = False
        def updateposition(position):
            #print("updateposition: " + str(position))
            if self.dropupdate:
                self.dropupdate = False
                return
            self.yview("moveto", str(position))
            self.linetext.yview("moveto", str(position))
            self.lastPosition = position
        def textviewchange(*args):
            #print("textviewchange: " + str(args))
            updateposition(float(args[0]))
            self.scrollbar.set(*args)
        def scrollviewchange(*args):
            #print("scrollviewchange: " + str(args))
            self.yview(*args)
            self.linetext.yview(*args)
        self.config(yscrollcommand=textviewchange)
        self.linetext.config(yscrollcommand=textviewchange)
        self.scrollbar.config(command=scrollviewchange)

        # Kickstart the line number updates
        self.update_line_numbers()

    def update_line_numbers(self):
        def display_lines_for_actual_line(actual_line, available_pixels):
            def get_residual(string, available_pixels):
                whitespace_tally = 0

                for index, character in enumerate(string):
                    if character.isspace():
                        available_pixels -= whitespace_tally * 7
                        available_pixels -= 1
                        whitespace_tally = 1
                    else:
                        available_pixels -= whitespace_tally * 7
                        whitespace_tally = 0
                        available_pixels -= 8

                    if available_pixels < 0: return string[index:]

                return None

            line_count = 0
            residual = actual_line
            while True:
                residual = get_residual(residual, available_pixels)
                line_count += 1
                if residual == None: break
                
            return line_count
        
        def generate_line_numbers(tktext):
            available_pixels = tktext.winfo_width() - 10
            actual_lines = tktext.get(1.0, tk.END).split("\n")[:-1]

            output = ""
            counter = 1
            for actual_line in actual_lines:
                display_line_count = display_lines_for_actual_line(actual_line, available_pixels)
                
                if(counter > 1): output += "\n"
                output += str(counter)
                for i in range(1, display_line_count):
                    output += "\n"
                counter += 1
            
            return output

        data = generate_line_numbers(self)
        self.linetext.config(state='normal')
        self.linetext.delete('1.0', tk.END)
        self.linetext.insert('1.0', data)
        self.linetext.config(state='disabled')

        self.linetext.yview("moveto", str(self.lastPosition))
        self.dropupdate = True

        self.after(100, self.update_line_numbers)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

class SchemeEditor(LineNumsText):
    '''
    Scheme Text
    
    Text widget that does (basic) keyword coloring for Scheme text.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets the values of the tags and key press handler.'''
        LineNumsText.__init__(self, *args, **kwargs)
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
                                count=count).strip()
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


