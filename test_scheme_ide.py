import unittest
import tkinter as tk
import tkinter.messagebox as MBox
from scheme_ide import *
import time
import random
import os

class SchemeIDETest(unittest.TestCase):
    '''
    Scheme IDE Test

    Tests the front end of this application as well as some functionality of the evaluator.
    '''
	
    def setUp(self):
        '''This is called every time a test method is run.'''
        self.root = tk.Tk()
        self.app = AppStub(master=self.root)
        #Todo: Check for the existence of test.txt.
        open("test.txt", 'a')

    def tearDown(self):
        try: self.root.destroy()
        except: pass
        os.remove("test.txt")

    def shortDescription(self):
        '''Prevents unittest from displaying docstrings on every run.'''
        return None
    
    def test_basic_run(self):
        '''Verifies console output after running code.'''
        
        self.app.editor.insert('end', "(+ 2 2)")
        self.app.run_code()
        result = self.app.console.get("2.0", "2.1")
        self.assertEqual(result, '4', 'Console did not output 4.')

    def test_multiple_runs(self):
        '''Test console output after three runs.'''

        self.app.editor.insert('end', "(* 131 18 7)")
        self.app.run_code()
        result = self.app.console.get("2.0", "2.5")
        self.assertEqual(result, '16506', 'Console did not output 16506.')
        
        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', "!!!")
        self.app.run_code()
        result = self.app.console.get("4.0", "4.4")
        self.assertEqual(result, 'None', 'Console did not output None.')

        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', "(+ (* 6 6) 18)")
        self.app.run_code()
        result = self.app.console.get("6.0", "6.2")
        self.assertEqual(result, '54', 'Console did not output 54.')
        
		
    def test_highlight_lambda(self):
        '''Verifies keyword highlighting for typed lambda in the editor.'''

        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', '(lambda other stuff)')
        self.app.editor.highlight_pattern('lambda', 'red')

        x, y = self.app.editor.tag_ranges('red')
        tag_range = (str(x), str(y))
        expected = ('1.1', '1.7')
        
        self.assertEqual(expected, tag_range)

    def test_delayed_highlight(self):
        '''Test for delayed keyword highlighting issue.'''

        self.app.editor.delete('1.0', 'end')        
        self.app.press_key('+', 'editor')
        
        x, y = self.app.editor.tag_ranges('green')
        tag_range = (str(x), str(y))    
        expected = ('1.0', '1.1')     

        self.assertEqual(expected, tag_range)

    def test_double_arrow(self): 
        '''Test for same line arrow output issue.'''  

        self.app.editor.delete('1.0', 'end')     
        self.app.editor.insert('end', "2+2")
        self.app.run_code()
        output = self.app.console.get("1.0", "end")
        self.assertNotEqual(output, "-> -> \n")

    def test_save(self):
        '''Verifies saving a file with minimal mocking.'''
        
        self.app.editor.delete('1.0', 'end') 
        test_message = "test message (" + str(random.random()) + ")"
        self.app.editor.insert('end', test_message)
        self.app.save_file(testMode=True, path='test.txt')
        with open("test.txt") as test_file: test_data = test_file.read().strip()
        self.assertTrue(test_data == test_message, 'Discrepancy when saving text file.')       

    def test_open(self, testMode=False):
        '''Verfies opening a file with minimal mocking.'''

        self.app.editor.delete('1.0', 'end') 
        test_message = "test message (" + str(random.random()) + ")"
        with open("test.txt", "w") as test_file: test_file.write(test_message)
        self.app.editor.insert('end', test_message)
        self.app.open_file(testMode=True, path='test.txt')
        self.assertTrue(self.app.editor.get_all().strip() == test_message, 'Discrepancy when opening text file.')

    def test_text_entry(self):
        '''Verifies that a user can type text into the editor.'''        

        self.app.editor.delete('1.0', 'end') 
        for x in range(20):
            self.app.press_key(str(x),'editor')
    
    def test_shell_evaluation(self):
        '''Verifies that the shell can take expressions and evaluate them.'''

        self.app.console.insert('1.3', '(* 6 6)')
        self.app.press_key('\r', 'console')
        out = self.app.console.get('2.0', '2.2')
        self.assertEqual(out, '36')

    def test_multiple_shell_evaluations(self):
        '''Tests shell evaluations when given multiple expressions.'''

        self.app.console.insert('1.3', '(* 6 6)')
        self.app.press_key('\r', 'console')
        out = self.app.console.get('2.0', '2.2')
        self.assertEqual(out, '36')

        self.app.console.insert('3.3', '!!!')
        self.app.press_key('\r', 'console')
        out = self.app.console.get('4.0', '4.4')
        self.assertEqual(out, 'None')

        self.app.console.insert('5.3', '(* (+ 18 19) 200)')
        self.app.press_key('\r', 'console')
        out = self.app.console.get('6.0', '6.4')
        self.assertEqual(out, '7400')

class EventStub: 
    '''Pretend event stub for methods that take an event argument.'''
    def __init__(self, c):        
        self.char = c

class AppStub(SchemeIDE):
    '''Application stub that simulates user interaction.'''

    def __init__(self, *args, **kwargs):
        SchemeIDE.__init__(self, *args, **kwargs)    

    def press_key(self, c, widget):
        '''Simulates a keypress where handler is called on release.'''

        if widget == 'editor':
            self.editor.insert('end', c)
            self.editor.key(EventStub(c))
        if widget == 'console':
            if c == '\r':
                self.console.insert('end', '\n')
                self.console._key(EventStub(c))

def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(SchemeIDETest('test_basic_run'))
    suite.addTest(SchemeIDETest('test_multiple_runs'))
    suite.addTest(SchemeIDETest('test_highlight_lambda'))
    suite.addTest(SchemeIDETest('test_delayed_highlight'))
    suite.addTest(SchemeIDETest('test_double_arrow'))
    suite.addTest(SchemeIDETest('test_save'))
    suite.addTest(SchemeIDETest('test_open'))
    suite.addTest(SchemeIDETest('test_text_entry'))
    suite.addTest(SchemeIDETest('test_shell_evaluation'))
    suite.addTest(SchemeIDETest('test_multiple_shell_evaluations'))
    return suite
    	
if __name__ == '__main__':
    suite = create_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

