import sys, os
from decimal import *
#Needed so that Python knows where to find the files.
sys.path.append(os.path.join('..', 'scheme_ide'))
from scheme_ide import *
import evaluator as ev
import unittest
import tkinter as tk
import time
import random

class SchemeIDETest(unittest.TestCase):
    '''
    Scheme IDE Test

    Tests the front end of this application as well as some functionality of the evaluator.
	
    Todo: Check for the existence of test.txt. I can see someone running this in the wrong directory and deleting a pre-existing test.txt.
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
        result = self.app.console.get("4.0", "4.6")
        self.assertEqual(result, 'Error!', 'Console did not output None.')

        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', "(+ (* 6 6) 18)")
        self.app.run_code()
        result = self.app.console.get("6.0", "6.2")
        self.assertEqual(result, '54', 'Console did not output 54.')
    
    def test_run_code(self):
        '''Verifies console output after running code.'''
        
        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', "(+ 2 2)")
        self.app.run_code()
        result = self.app.console.get("2.0", "2.1")
        self.assertEqual(result, '4', 'Console did not output 4.')
               
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
        x, y = self.app.editor.tag_ranges('operator')
        tag_range = (str(x), str(y))    
        expected = ('1.0', '1.1')     

        self.assertEqual(expected, tag_range)

    def test_paren_matching(self):
        '''Verifies keyword highlighting for typed lambda in the editor.'''

        self.app.editor.delete('1.0', 'end')
        self.app.editor.insert('end', 'abc(def(s))')
        self.app.editor.key(None)
        ranges = self.app.editor.tag_ranges('paren_highlight')
        ranges_str = [str(x) for x in ranges]
        self.assertEqual(['1.3', '1.4', '1.10', '1.11'], ranges_str)

    def test_double_arrow(self): 
        '''Test for same line arrow output issue.'''  

        self.app.editor.delete('1.0', 'end')     
        self.app.editor.insert('end', "2+2")
        self.app.run_code()
        output = self.app.console.get("1.0", "end")
        self.assertNotEqual(output, ">> >> \n")

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
        out = self.app.console.get('4.0', '4.6')
        self.assertEqual(out, 'Error!')

        self.app.console.insert('5.3', '(* (+ 18 19) 200)')
        self.app.press_key('\r', 'console')
        out = self.app.console.get('6.0', '6.4')
        self.assertEqual(out, '7400')

    def test_tutorial_feedback_on_correct(self):
        '''Tests that tutorial can identify correct output (e.g. 4)'''
        
        self.app.create_tutorial()
        tutorial = self.app.tutorial()
        console = self.app.console()

        #Simulate a user typing in input.
        console.insert('1.3', '(+ 2 2)')
        self.app.press_key('\r', 'console')
        
        #Simulate a user checking his answer.
        tutorial.check()
        
        self.assertTrue(tutorial.feedback())

    def test_tutorial_feedback_on_incorrect(self):
        '''Tests that tutorial can identify incorrect output (e.g. 3)'''
        
        self.app.create_tutorial()
        tutorial = self.app.tutorial()
        console = self.app.console()

        #Simulate a user typing in input.
        console.insert('1.3', '(+ 1 2)')
        self.app.press_key('\r', 'console')
        
        #Simulate a user checking his answer.
        tutorial.check()
        
        self.assertTrue(not tutorial.feedback())

    def test_tutorial_creation(self):
        '''Unit test for Tutorial constructor method.'''

        tutorial = Tutorial(self.root)

        self.assertTrue('tutorial' in locals())
        self.assertTrue(hasattr(tutorial, 'title'))
        self.assertTrue(type(tutorial.title) is tk.Text)
 
        self.assertTrue(hasattr(tutorial, 'instr'))
        self.assertTrue(type(tutorial.instr) is tk.Text)

        self.assertTrue(hasattr(tutorial, 'check'))
        self.assertTrue(type(tutorial.check) is tk.Button)

        self.assertTrue(hasattr(tutorial, 'feedback'))
        self.assertTrue(type(tutorial.feedback) is tk.Text)

    def test_number_literal(self):
        out = ev.evaluate('486')
        self.assertEqual(out, 486)

    def test_no_operator(self):
        out = ev.evaluate('(2 2)')
        self.assertEqual(out, None)

    def test_addition(self):
        out = ev.evaluate('(+ 137 349)')
        self.assertEqual(out, 486)

    def test_subtraction(self):
        out = ev.evaluate('(- 1000 334)')
        self.assertEqual(out, 666)

    def test_multiplication(self):
        out = ev.evaluate('(* 5 99)')
        self.assertEqual(out, 495)

    def test_division(self):
        out = ev.evaluate('(/ 10 5)')
        self.assertEqual(out, 2)

    def test_negation(self):
        out = ev.evaluate('(- 5)')
        self.assertEqual(out, -5)

    def test_operator_presidence(self):
        out = ev.evaluate('(- 5 -3 (- 4))')
        self.assertEqual(out, 12)

    def test_decimal_addition(self):
        out = ev.evaluate('(+ 2.7 10)')
        self.assertEqual(out, Decimal('12.7'))

    def test_four_operator_addition(self):
        out = ev.evaluate('(+ 21 35 12 7)')
        self.assertEqual(out, 75)
    
    def test_evaluator_1(self):
        out = ev.evaluate('486')
        self.assertEqual(out, 486)

    def test_evaluator_2(self):
        out = ev.evaluate('(+ 137 349)')
        self.assertEqual(out, 486)

    def test_evaluator_3(self):
        out = ev.evaluate('(- 1000 334)')
        self.assertEqual(out, 666)

    def test_evaluator_4(self):
        out = ev.evaluate('(* 5 99)')
        self.assertEqual(out, 495)

    def test_evaluator_5(self):
        out = ev.evaluate('(/ 10 5)')
        self.assertEqual(out, 2)

    def test_evaluator_6(self):
        out = ev.evaluate('(- 5)')
        self.assertEqual(out, -5)

    def test_evaluator_7(self):
        out = ev.evaluate('(- 5 -3 (- 4))')
        self.assertEqual(out, 12)

    def test_evaluator_8(self):
        out = ev.evaluate('(+ 2.7 10)')
        self.assertEqual(out, 12.7)

    def test_evaluator_9(self):
        out = ev.evaluate('(+ 21 35 12 7)')
        self.assertEqual(out, 75)

    def test_evaluator_10(self):
        out = ev.evaluate('(* 25 4 12)')
        self.assertEqual(out, 1200)

    def test_evaluator_11(self):
        out = ev.evaluate('(+ (* 3 5) (- 10 6))')
        self.assertEqual(out, 19)

    def test_evaluator_12(self):
        out = ev.evaluate('(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))')
        self.assertEqual(out, 57)

    def test_evaluator_13(self):
        out = ev.evaluate('(* (+ 2 (* 4 6))  (+ 3 5 7))')
        self.assertEqual(out, 390)

    def test_evaluator_14(self):
        out = ev.evaluate('(define pi 3.14159)')
        self.assertEqual(out, None)

    def test_evaluator_15(self):
        out = ev.evaluate('(define radius 10)')
        self.assertEqual(out, None)

    def test_evaluator_16(self):
        out = ev.evaluate('(* pi (* radius radius))')
        self.assertEqual(out, 314.159)

    def test_evaluator_17(self):
        out = ev.evaluate('(define circumference (* 2 pi radius))')
        self.assertEqual(out, None)

    def test_evaluator_18(self):
        out = ev.evaluate('circumference')
        self.assertEqual(out, 62.8318)

    def test_evaluator_19(self):
        out = ev.evaluate('(define (square x) (* x x))')
        self.assertEqual(out, None)

    def test_evaluator_20(self):
        out = ev.evaluate('(define (sum-of-squares x y)(+ (square x) (square y)))')
        self.assertEqual(out, None)

    def test_evaluator_21(self):
        out = ev.evaluate('(square 5)')
        self.assertEqual(out, 25)

    def test_evaluator_22(self):
        out = ev.evaluate('(square (square 3))')
        self.assertEqual(out, 81)

    def test_evaluator_23(self):
        out = ev.evaluate('(sum-of-squares 3 4)')
        self.assertEqual(out, 25)

    def test_evaluator_24(self):
        out = ev.evaluate('(sum-of-squares (square 3) (square 4))')
        self.assertEqual(out, 337)

    def test_evaluator_25(self):
        out = ev.evaluate('(define (f a)(sum-of-squares (+ a 1) (* a 2)))')
        self.assertEqual(out, None)

    def test_evaluator_26(self):
        out = ev.evaluate('(f 5)')
        self.assertEqual(out, 136)

    def test_evaluator_27(self):
        out = ev.evaluate('(define a 3)')
        self.assertEqual(out, )

    def test_evaluator_28(self):
        out = ev.evaluate('(define b (+ a 1))')
        self.assertEqual(out, )

    def test_evaluator_29(self):
        out = ev.evaluate('(+ a b (* a b))')
        self.assertEqual(out, 19)

    def test_evaluator_30(self):
        out = ev.evaluate('(> a b)')
        self.assertEqual(out, False)

    def test_evaluator_31(self):
        out = ev.evaluate('(if (and (> b a) (< b (* a b))) b a)')
        self.assertEqual(out, 4)

    def test_evaluator_32(self):
        out = ev.evaluate('(cond ((= a 4) 6) ((= b 4) (+ 6 7 a)) (else 25))')
        self.assertEqual(out, 16)

    def test_evaluator_33(self):
        out = ev.evaluate('(+ 2 (if (> b a) b a))')
        self.assertEqual(out, 6)

    def test_evaluator_34(self):
        out = ev.evaluate('(* (cond ((> a b) a) ((< a b) b) (else -1)) (+ a 1))')
        self.assertEqual(out, 16)

    def test_evaluator_35(self):
        out = ev.evaluate('(define (abs x)(cond ((< x 0) (- x))(else x)))')
        self.assertEqual(out, None)

    def test_evaluator_36(self):
        out = ev.evaluate('(define (average x y)(/ (+ x y) 2))')
        self.assertEqual(out, None)

    def test_evaluator_37(self):
        out = ev.evaluate('(define (improve guess x)(average guess (/ x guess)))')
        self.assertEqual(out, None)

    def test_evaluator_38(self):
        out = ev.evaluate('(define (good-enough? guess x)(< (abs (-(square guess) x)) 0.001))')
        self.assertEqual(out, None)

    def test_evaluator_39(self):
        out = ev.evaluate('(define (sqrt-iter guess x)(if (good-enough? guess x) guess(sqrt-iter (improve guess x) x)))')
        self.assertEqual(out, None)

    def test_evaluator_40(self):
        out = ev.evaluate('(define (sqrt x) (sqrt-iter 1.0 x))')
        self.assertEqual(out, None)

    def test_evaluator_41(self):
        out = ev.evaluate('(sqrt 9)')
        self.assertEqual(out, 3.00009155413138)

    def test_evaluator_42(self):
        out = ev.evaluate('(define (^ base exp) (if (= exp 0) 1 (* base (^ base (- exp 1)))))')
        self.assertEqual(out, None)

    def test_evaluator_43(self):
        out = ev.evaluate('(^ 17 0)')
        self.assertEqual(out, 1)

    def test_evaluator_44(self):
        out = ev.evaluate('(^ -2 7)')
        self.assertEqual(out, -128)

    def test_evaluator_45(self):
        out = ev.evaluate('(^ 3 4)')
        self.assertEqual(out, 81)

    def test_evaluator_46(self):
        out = ev.evaluate('(define (cube x) (* x x x))')
        self.assertEqual(out, )

    def test_evaluator_47(self):
        out = ev.evaluate('(define (sum term a next b)(if (> a b) 0(+ (term a)(sum term (next a) next b))))')
        self.assertEqual(out, None)

    def test_evaluator_48(self):
        out = ev.evaluate('(define (inc n) (+ n 1))')
        self.assertEqual(out, None)

    def test_evaluator_49(self):
        out = ev.evaluate('(define (sum-cubes a b)(sum cube a inc b))')
        self.assertEqual(out, None)

    def test_evaluator_50(self):
        out = ev.evaluate('(sum-cubes 1 10)')
        self.assertEqual(out, 3025)

    def test_evaluator_51(self):
        out = ev.evaluate('(define (identity x) x)')
        self.assertEqual(out, None)

    def test_evaluator_52(self):
        out = ev.evaluate('(define (sum-integers a b)(sum identity a inc b))')
        self.assertEqual(out, None)

    def test_evaluator_53(self):
        out = ev.evaluate('(sum-integers 1 10)')
        self.assertEqual(out, 55)

    def test_evaluator_54(self):
        out = ev.evaluate('(define (pi-term x)(/ 1.0 (* x (+ x 2))))')
        self.assertEqual(out, None)

    def test_evaluator_55(self):
        out = ev.evaluate('(define (pi-next x)(+ x 4))')
        self.assertEqual(out, None)

    def test_evaluator_56(self):
        out = ev.evaluate('(define (pi-sum a b)(sum pi-term a pi-next b))')
        self.assertEqual(out, None)

    def test_evaluator_57(self):
        out = ev.evaluate('(* 8 (pi-sum 1 100))')
        self.assertEqual(out, 3.139592655589783)

    def test_evaluator_58(self):
        out = ev.evaluate('(define (list-ref items n) (if (= n 0) (car items) (list-ref (cdr items) (- n 1))))')
        self.assertEqual(out, None)

    def test_evaluator_59(self):
        out = ev.evaluate('(define squares (list 1 4 9 16 25))')
        self.assertEqual(out, None)

    def test_evaluator_60(self):
        out = ev.evaluate('(list-ref squares 3)')
        self.assertEqual(out, 16)

    def test_quotes(self):
        out = ev.evaluate("(car '(1 2 '3))")
        self.assertEqual(out, str(1))
    
    def test_blank_shell_input(self):
        '''Test for issue where inputing only non-alphanumberic characters broke the shell.'''
        
        self.app.press_key('\r', 'console')
        out = self.app.console.get('2.0', '2.2')
        self.assertEqual(out, '>>')

    def test_misplaced_error_message(self):
        '''Test for issue where an error message was misplaced after evaluating invalid code in the editor.'''

        self.app.editor.insert('end', 'gibberish')
        self.app.run_code()
        out = self.app.console.get('1.0', 'end')
        self.assertEqual(out, '>> run\nError!\n>> \n')

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
            
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SchemeIDETest)
    unittest.TextTestRunner(verbosity=2).run(suite)

