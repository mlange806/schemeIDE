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

        frame = tk.Frame(root)
        frame.pack(side='top')
        lesson_name = tk.Label(frame, text="Lesson Name: ", width=15)
        lesson_name.pack(side="left")
        lesson_input = tk.Text(frame, height=1, width=30)
        lesson_input.pack(side="left")

        w = tk.Label(root, text=seperator)
        w.pack(side='top')

        # Here is where the scroll maddness begins
        frame = tk.Frame(root)
        frame.pack(side='top')
    
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
        
        section_name = tk.Label(self.section_frame, text="Section Name: ", width=15).grid(row=self.x, column=0)
        section_input = tk.Text(self.section_frame, height=1, width=30).grid(row=self.x, column=1)

        instr_name = tk.Label(self.section_frame, text="Instructions: ", width=15).grid(row=self.x+1, column=0)
        instr_input = tk.Text(self.section_frame, height=5, width=30).grid(row=self.x+1, column=1)
        # Here it where it ends

        
        frame = tk.Frame(root)
        frame.pack(side='top')
        add_section = tk.Button(frame, text='+ Add Section', command=self.add_section)
        add_section.pack(side='left')

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
        section_name = tk.Label(self.section_frame, text="Section Name: ", width=15).grid(row=self.x, column=0)
        section_input = tk.Text(self.section_frame, height=1, width=30).grid(row=self.x, column=1)

        instr_name = tk.Label(self.section_frame, text="Instructions: ", width=15).grid(row=self.x+1, column=0)
        instr_input = tk.Text(self.section_frame, height=5, width=30).grid(row=self.x+1, column=1)

    def OnFrameConfigure(self, event):
        self.section_canvas.configure(scrollregion=self.section_canvas.bbox("all"))

if __name__ == '__main__':
    root=tk.Tk()
    t = CourseCreator(root)
    root.mainloop()
