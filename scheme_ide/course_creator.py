import tkinter as tk

class CourseCreator(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(CourseCreator, self).__init__(*args, **kwargs)
        self.wm_title("Create Tutorial")

        frame = tk.Frame(self)
        frame.pack(side='top')
        course_name = tk.Label(frame, text="Course Name: ", width=15)
        course_name.pack(side="left")
        course_input = tk.Text(frame, height=1, width=30)
        course_input.pack(side="left")

        seperator = ''
        for x in range(80): seperator = seperator + '_'
        w = tk.Label(self, text=seperator)
        w.pack(side='top')

        frame = tk.Frame(self)
        frame.pack(side='top')
        lesson_name = tk.Label(frame, text="Lesson Name: ", width=15)
        lesson_name.pack(side="left")
        lesson_input = tk.Text(frame, height=1, width=30)
        lesson_input.pack(side="left")

        w = tk.Label(self, text=seperator)
        w.pack(side='top')

        self.section_frame = tk.Frame(self, height=10)
        self.section_frame.pack(side='top')

        frame = tk.Frame(self.section_frame)
        frame.pack(side='top')
        section_name = tk.Label(frame, text="Section Name: ", width=15)
        section_name.pack(side="left")
        section_input = tk.Text(frame, height=1, width=30)
        section_input.pack(side="left")

        frame = tk.Frame(self.section_frame)
        frame.pack(side='top')
        instr_name = tk.Label(frame, text="Instructions: ", width=15)
        instr_name.pack(side="left")
        instr_input = tk.Text(frame, height=5, width=30)
        instr_input.pack(side="left")
        
        frame = tk.Frame(self)
        frame.pack(side='top')
        add_section = tk.Button(frame, text='+ Add Section', command=self.add_section)
        add_section.pack(side='left')

        w = tk.Label(self, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(self)
        frame.pack(side='top')
        add_lesson = tk.Button(frame, text='+ Add Lesson')
        add_lesson.pack(side='left')
        
        w = tk.Label(self, text=seperator)
        w.pack(side='top')
    
        frame = tk.Frame(self)
        frame.pack(side='top')
        save = tk.Button(frame, text='Save Course')
        save.pack(side='left')

    def add_section(self):
        frame = tk.Frame(self.section_frame)
        frame.pack(side='top')
        section_name = tk.Label(frame, text="Section Name: ", width=15)
        section_name.pack(side="left")
        section_input = tk.Text(frame, height=1, width=30)
        section_input.pack(side="left")

        frame = tk.Frame(self.section_frame)
        frame.pack(side='top')
        instr_name = tk.Label(frame, text="Instructions: ", width=15)
        instr_name.pack(side="left")
        instr_input = tk.Text(frame, height=5, width=30)
        instr_input.pack(side="left")

if __name__ == '__main__':
    t = CourseCreator()
    t.mainloop()
