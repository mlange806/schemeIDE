import tkinter as tk
import re

class SchemeText(tk.Text):
    '''
    Scheme Text
    
    Text widget that does (basic) keyword coloring for Scheme text.
    '''

    def __init__(self, reference_highlighting_callback=None, *args, **kwargs):
        '''Sets the values of the tags and key press handler.'''

        tk.Text.__init__(self, *args, **kwargs)
        self.reference_highlighting_callback = reference_highlighting_callback
        self.bind("<KeyRelease>", self.key)
        self.bind("<ButtonRelease>", self.key)

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

    def reference_highlight(self, event): 
        def get_selected_string():
            current_position = self.index(tk.INSERT)
            current_line, current_col = [int(x) for x in current_position.split('.')]

            def make_index(column):
                return str(current_line) + "." + str(column)

            start_col = current_col
            while start_col > 0:
                start_col -= 1
                char = self.get(make_index(start_col))
                if not (char.isalpha() or char.isdigit()):
                    start_col += 1
                    break

            end_col = current_col
            while True:
                char = self.get(make_index(end_col))
                if not (char.isalpha() or char.isdigit()):
                    break
                end_col += 1

            return make_index(start_col), make_index(end_col)

        def get_tk_instances(text):
            results = list()
            self.mark_set("scanStart", "1.0")
            self.mark_set("scanEnd", self.index("end"))
             
            count = tk.IntVar()
            while True:
                index = self.search(text, "scanStart", "scanEnd",
                                    count=count).strip()
                if index == "": break
                self.mark_set("scanStart", "%s+%sc" % (index, count.get()))
                results.append(index)

            return results

        def get_instances(text):
            tk_instances = get_tk_instances(text)
            source = self.get_all()
            source_len = len(source)
            results = list()

            for index, match in enumerate(re.finditer(text, source)):
                start = match.start()
                end = match.end()

                if start > 0:
                    if source[start-1].isalpha() or source[start-1].isdigit():
                        continue
                if end < source_len:
                    if source[end].isalpha() or source[end].isdigit():
                        continue

                results.append((start, tk_instances[index], 0))

            return results

        tk_start_index, tk_end_index = get_selected_string()
        if tk_start_index == tk_end_index: return
        text = self.get(tk_start_index, tk_end_index)

        instances = get_instances(text)
        for instance in instances:
            if tk_start_index == instance[1]:
                text_start_index = instance[0]

        final = (text, text_start_index, tk_start_index, instances)
        print(final)

        #print(self.get())
        #print(text)
        #print(get_instances(text))

    def paren_match(self, event):
        profiles = (("(", ")", "[(]|[)]"),)
        
        def offset_index(index, roworcolumn, shift):
            integers = [int(x) for x in index.split(".")]
            integers[roworcolumn] += shift
            if integers[roworcolumn] < 0: integers[roworcolumn] = 0
            return str(integers[0]) + "." + str(integers[1])

        def paren_scan(pattern, start, end=None):
            # Returns list of parens matching regex pattern within range
            result = list()
            
            self.mark_set("scanStart", start)
            if end == None: self.mark_set("scanEnd", self.index("end"))
            else: self.mark_set("scanEnd", end)

            count = tk.IntVar()
            while True:
                index = self.search(pattern, "scanStart", "scanEnd",
                                    count=count, regexp=True).strip()
                if index == "": break
                self.mark_set("scanStart", "%s+%sc" % (index, count.get()))
                result.append((self.get(index), index))

            return result

        def locate_match(index):
            # Locates the counterpart, if it exists, to paren located at index
            char = self.get(index)
            scanresults = None
            for profile in profiles:
                if char == profile[0]:
                    scanresults = paren_scan(profile[2], index+"+1c")
                    direction = 1
                    break
                elif char == profile[1]:
                    scanresults = reversed(paren_scan(profile[2], "1.0", index))
                    direction = -1
                    break
            if scanresults == None: return None

            tally = 1
            for scanresult in scanresults:
                if scanresult[0] == profile[0]: tally += direction
                elif scanresult[0] == profile[1]: tally -= direction
                if tally == 0: return scanresult[1]

            return None

        def color_paren(index):
            # Applies color to paren located at index
            self.tag_add("paren_highlight", index)

        # Clear existing tags
        self.tag_remove("paren_highlight", '1.0', 'end')

        # Get current cursor position
        current_position = self.index(tk.INSERT)

        # Look for paren at beginning of selection area
        try: match = locate_match("sel.first")
        except: match = None
        if match != None:
            color_paren("sel.first")
            color_paren(match)
            return

        # Look for paren left of cursor
        current_position_one_left = offset_index(current_position, 1, -1)
        match = locate_match(current_position_one_left)
        if match != None:
            color_paren(current_position_one_left)
            color_paren(match)
            return

        # Look for paren right of cursor
        match = locate_match(current_position)
        if match != None:
            color_paren(current_position)
            color_paren(match)

    def key(self, event):
        '''Updates the text color on key presses.'''
        #Start with a blank slate.
        self.tag_remove("keyword", '1.0', 'end')
        self.tag_remove("operator", '1.0', 'end')    
        
        #Do keyword highlighting.
        self.highlight_pattern("define", "keyword")
        self.highlight_pattern("lambda", "keyword")
        self.highlight_pattern("+", "operator")
        self.highlight_pattern("-", "operator")  
        self.highlight_pattern("*", "operator")
        self.highlight_pattern("/", "operator")

        #Invoke parenthesis matching
        self.paren_match(event)

        # Invoke reference highlighting
        self.reference_highlight(event)

    def set_all(self, string):
        # Sets the contents of the text box to this string.
        self.delete(1.0, tk.END)
        self.insert(1.0, string)

    def get_all(self):
        # Returns full contents of the text box.
        return self.get(1.0, tk.END)

