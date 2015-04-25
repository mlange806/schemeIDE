import tkinter as tk

class CourseCreator(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super(CourseCreator, self).__init__(*args, **kwargs)

        frame = tk.Frame(root)
        frame.pack(side='top')
        course_name = tk.Label(frame, text="Course Name: ", width=15)
        course_name.pack(side="left")
        course_input = tk.Text(frame, height=1, width=30)
        course_input.pack(side="left")

        seperator = ''
        for x in range(80): seperator = seperator + '_'
        w = tk.Label(root, text=seperator)
        w.pack(side='top')
 
        # Add a scroll here too
        frame = tk.Frame(root)
        frame.pack(side='top')

        self.lesson_canvas = tk.Canvas(frame)
        self.lesson_frame = tk.Frame(self.lesson_canvas)
        self.lesson_scroll = tk.Scrollbar(frame, orient="vertical", command=self.lesson_canvas.yview)
        self.lesson_canvas.configure(yscrollcommand=self.lesson_scroll.set)

        

        lesson_name = tk.Label(self.lesson_frame, text="Lesson Name: ", width=15)
        lesson_name.grid(row=0, column=0)
        lesson_input = tk.Text(self.lesson_frame, height=1, width=30)
        lesson_input.grid(row=0, column=1)
        # End Lesson Scroll

        # Here is where the scroll maddness begins
        frame = tk.Frame(self.lesson_canvas)
        frame.grid(row=1, column=0)
    
        self.section_canvas = tk.Canvas(frame)
        self.section_frame = tk.Frame(self.section_canvas, height=10)
        self.scroll = tk.Scrollbar(frame, orient="vertical", command=self.section_canvas.yview)
        self.section_canvas.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side="right", fill='y')
        self.section_canvas.pack(side="right", fill="both", expand=True)
        self.section_canvas.create_window((2,2), window=self.section_frame, anchor="nw", 
                                  tags="self.section_frame")
        self.section_frame.bind("<Configure>", self.OnFrameConfigure)

        self.x = 0

        self.section_list = []
        
        section_name = tk.Label(self.section_frame, text="Section Name: ", width=15)
        section_name.grid(row=self.x, column=0)
        section_input = tk.Text(self.section_frame, height=1, width=30)
        section_input.grid(row=self.x, column=1)

        instr_name = tk.Label(self.section_frame, text="Instructions: ", width=15)
        instr_name.grid(row=self.x+1, column=0)
        instr_input = tk.Text(self.section_frame, height=5, width=30)
        instr_input.grid(row=self.x+1, column=1)

        self.section_list.append((section_name, section_input, instr_name, instr_input))

        self.lesson_scroll.pack(side='right', fill='y')
        self.lesson_canvas.pack(side='right', fill="both", expand=True)
        self.lesson_canvas.create_window((2,2), window=self.lesson_frame, anchor="nw", 
                                  tags="self.lesson_frame")
        self.lesson_frame.bind("<Configure>", self.OnFrameConfigure)
        # Here is where it ends

        
        frame = tk.Frame(root)
        frame.pack(side='top')
        add_section = tk.Button(frame, text='+ Add Section', command=self.add_section)
        add_section.pack(side='left')
        rm_section = tk.Button(frame, text='- Remove Section', command=self.rm_section)
        rm_section.pack(side='left')

        w = tk.Label(root, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(root)
        frame.pack(side='top')
        add_lesson = tk.Button(frame, text='+ Add Lesson')
        add_lesson.pack(side='left')
        
        w = tk.Label(root, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(root)
        frame.pack(side='top')
        save = tk.Button(frame, text='Save Course')
        save.pack(side='left')

    def add_section(self):
        self.x = self.x + 1
        section_name = tk.Label(self.section_frame, text="Section Name: ", width=15)
        section_name.grid(row=self.x, column=0)
        section_input = tk.Text(self.section_frame, height=1, width=30)
        section_input.grid(row=self.x, column=1)

        instr_name = tk.Label(self.section_frame, text="Instructions: ", width=15)
        instr_name.grid(row=self.x+1, column=0)
        instr_input = tk.Text(self.section_frame, height=5, width=30)
        instr_input.grid(row=self.x+1, column=1)

        self.section_list.append((section_name, section_input, instr_name, instr_input))

    def rm_section(self):
        if self.x == 0:
            return
        else:
            for i in range(4):
                self.section_list[self.x][i].grid_forget()
            del self.section_list[self.x]
            self.x = self.x - 1

    def OnFrameConfigure(self, event):
        self.section_canvas.configure(scrollregion=self.section_canvas.bbox("all"))

if __name__ == '__main__':
    root=tk.Tk()
    t = CourseCreator(root)
    root.mainloop()
