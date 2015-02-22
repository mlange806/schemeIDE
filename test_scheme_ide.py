import unittest
import tkinter as tk
import tkinter.messagebox as MBox
from scheme_ide import *
import time
import random
import os

class TestSchemeIDE(unittest.TestCase):
	
    def setUp(self):
        self.root = tk.Tk()
        self.app = SchemeIDE(master=self.root)

    def tearDown(self):
        try: self.root.destroy()
        except: pass
        os.remove("test.txt")

    def _verify(self, name, question):
        '''
        Asks the user to verify editor GUI functionality. Sets switch if a failure occurs.
        At the end, destroys the editor stub which is in the mainloop by the time this 
        method is called.
        '''
        self.gui_test_result = True
        result = MBox.askquestion(name, question)
        if result == 'no': self.gui_test_result = False
        self.root.destroy()

    def _key(self, event, title, msg):   
        if event.char == '\r':
            self._verify(title, msg)
    
    def _kill(self):
        self.root.destroy()
    
    def test_run_code(self):
        #Currently fails because evaluator is not implemented.
        self.app.editor.insert('end', "(+ 2 2)")
        self.app.run_code()
        result = self.app.console.get("2.3", "end")
        self.app.after(1, self._kill)
        self.app.mainloop()
        self.assertEqual(result, '4', 'Console did not output 4.')
		
    def test_highlight_lambda(self):
        self.app.editor.insert('end', 'Look at this code: (+ (lambda other stuff)')
        self.app.editor.highlight_pattern('lambda', 'red')
        self.app.after(1000, self._verify, "Test Lambda Highlight", "Is lambda highlighted?")
        self.app.mainloop()
        self.assertTrue(self.gui_test_result, 'Lambda is not highlighted.')

    def test_delayed_highlight(self):
        self.app.editor.insert('end', "Type '+' and 'return': ")
        self.app.editor.bind("<Key>", lambda event: self._key(event, "Test Delayed Highlight", "Is '+' highlighted?"))
        self.app.mainloop()
        self.assertTrue(self.gui_test_result, 'Highlight does not occur on completion.')

    def test_double_arrow(self):       
        self.app.editor.insert('end', "2+2")
        self.app.run_code()
        output = self.app.console.get("1.0", "end")
        self.app.after(1, self._kill)
        self.app.mainloop()
        self.assertNotEqual(output, "-> -> \n", 'Invalid code breaks console format.')

    def test_shell_evaluation(self):
        self.app.console.insert('1.3', '(+ 2 2)')
        output = self.app.console.get('2.0' '3.0')
        self.app.after(1, self._kill)
        self.app.mainloop()
        self.assertEqual(output, '4\n')
        
    def test_save(self):
        test_message = "test message (" + str(random.random()) + ")"
        self.app.editor.insert('end', test_message)
        self.app.run_code()
        MBox.showinfo("Message", "When the save box appears, attempt to save the file as 'test.txt'"
                      " in the current directory.")
        self.app.save_file()

        with open("test.txt") as test_file: test_data = test_file.read().strip()
        self.assertTrue(test_data == test_message, 'Discrepancy when saving text file.')       

    def test_open(self):
        test_message = "test message (" + str(random.random()) + ")"
        with open("test.txt", "w") as test_file: test_file.write(test_message)
        
        #self.app.editor.insert('end', test_message)
        self.app.run_code()
        MBox.showinfo("Message", "When the open box appears, attempt to open the file 'test.txt'"
                      " in the current directory.")
        self.app.open_file()

        self.assertTrue(self.app.editor.get_all().strip() == test_message, 'Discrepancy when opening text file.')

    def test_text_entry(self):
        self.charcount = 0
        def handler(event):
            self.charcount += 1
            if self.charcount == 20:
                self._verify("Test Text Entry", "Did text show up correctly?")

        self.app.run_code()
        self.app.editor.bind("<Key>", handler)

        self.app.after(1000, MBox.showinfo, "Message", "Try typing 20 characters into the text box.")
        self.app.mainloop()
        self.assertTrue(self.gui_test_result, 'User reported problem entering text.')
		
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSchemeIDE)
    unittest.TextTestRunner(verbosity=2).run(suite)

