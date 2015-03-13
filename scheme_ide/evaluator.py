from decimal import *
debug = False #Controls whether or not the debug statements are printed
function_definitions = dict()
variable_definitions = dict()
#@TODO:
#Next up: conditionals: if, and, or, not, cond, (case)?, >, <, =, <=, >=
#
#Math:
#Arbitrary precision arithmetic
#Rationals
#Unary division? (/ x) = 1/x
#
#
#Other features:
#Quotes and quoting
#List manipulation: car, cdr, cons, (list)?
#Lambda functions
#
#
#General:
#Error messages
#Arity checking
#Scoping, environments
#
#

def run():
#The main method that only gets invoked if evaluator.py is the calling program, for quick testing mostly
        exp = ""
        while(True):
                exp = input()
                if(exp == ""):
                        break
                else:
                        print(evaluate(exp))
                
def evaluate(expression):
#Reads a string expression which is then parsed into a list 'tree' and evaluated
        debug_print("expression: " + str(expression))
        expr = parse(expression)
        debug_print("expression: <" + str(expr)+">")
        debug_print("start: <" + str(expr[0])+">")
        return eval(expr[0])

def eval(expression):
#Reads an expression in list 'tree' form and evaluates the result
        if(is_quoted(expression)): #This doesn't work
                debug_print("quote")
                return unquote(expression)
        elif(is_list(expression)): #Anything that's not an atom
                debug_print("list")
                return eval_function(expression)
        elif(is_int(expression)):
                debug_print("int")
                return int(expression)
        elif(is_float(expression)): #Floats are implemented as Decimals
                debug_print("float")
                return Decimal(expression)
        elif(is_rational(expression)): #Not implemented
                debug_print("rational")
                return expression
        elif(is_variable(expression)): #Technically, this checks if the expression represents a previously assigned variable
                debug_print("variable: " + expression)
                return variable_definitions[expression]
        else:
                debug_print("unknown")

def eval_function(expression): #Handles anything that isn't an atom - applies the function to all the arguments
        #Arity checking coming soon
        function = expression[0]
        if(function == "+"):
                sum = 0
                for summand in expression[1:]:
                        debug_print(summand)
                        sum += eval(summand)
                return sum
        elif(function == "-"):
                if(len(expression[1:]) == 1): #Unary minus
                        return eval(expression[1]) * -1
                difference = eval(expression[1])
                for subtrahend in expression[2:]:
                        debug_print(subtrahend)
                        difference -= eval(subtrahend)
                return difference
        elif(function == "*"):
                product = 1
                for multiplicand in expression[1:]:
                        debug_print(multiplicand)
                        product *= eval(multiplicand)
                return product
        elif(function == "/"):
                #Unary divide here, once rationals are implemented
                quotient = eval(expression[1])
                for divisor in expression[2:]:
                        debug_print(divisor)
                        quotient /= eval(divisor)
                return quotient
        elif(function == "car"): #Not implemented yet
                return car(eval(expression[1:][0]))
        elif(function == "define"): #Function and variable definition here
                signature = expression[1] #Signature: [name, arg1, arg2, ...]
                body = expression[2] #Actual definition
                if(is_list(signature)): #If signature has 2+ arguments, this is defining a function
                        args = len(signature) - 1 #Number of arguments, is stored for later arity checking
                        function_definitions[signature[0]] = (args, escape_args(signature[1:], body))
                        #Define the function to be the body, with the variables replaced by generics: see escape_args()
                        debug_print(function_definitions[signature[0]])
                else: #This is defining a variable, so just set the value of that variable 
                        variable_definitions[signature] = eval(body)
                        debug_print(str(variable_definitions))
                debug_print("<{0}: {1}>".format(signature, body))
        elif(function == "if"):
                predicate = expression[1]
                consequent = expression[2]
                alternative = expression[3]
                if(eval(predicate)):
                        return eval(consequent)
                else:
                        return eval(alternative)
        elif(function == "and"):
                for predicate in expression[1:]:
                        if(not eval(predicate)):
                                return False
                return True
        elif(function == "or"):
                for predicate in expression[1:]:
                        if(eval(predicate)):
                                return True
                return False
        elif(function == "not"):
                return(not eval(expression[1]))
        elif(function == "cond"):
                for pair in expression[1:]:
                        predicate = pair[0]
                        consequent = pair[1]
                        if(predicate == "else"):
                                return eval(consequent)
                        if(eval(predicate)):
                                return eval(consequent)
                return None
        elif(function == ">"):
                return(eval(expression[1]) > eval(expression[2]))
        elif(function == "<"):
                return(eval(expression[1]) < eval(expression[2]))
        elif(function == "="):
                return(eval(expression[1]) == eval(expression[2]))
        elif(function == "<="):
                return(eval(expression[1]) <= eval(expression[2]))
        elif(function == ">="):
                return(eval(expression[1]) >= eval(expression[2]))
        else: #If none of the other conditions are met, this is a user-defined function
                if(function in function_definitions.keys()): #Check for existence
                        return(apply_function(function, expression[1:]))
                else:
                        debug_print("<{0}> is not a valid operator.".format(expression[0]))
                        return None

                        
def apply_function(name, args): #Applies the function to the arguments
        debug_print(str(function_definitions))
        body = function_definitions[name]
        num_args = body[0]
        body = unescape_args(args, body[1])
        #Here, we substitute (expand) the body of the function with the given arguments, instead of evaluating them as they come up
        #Remains to be seen if this is going to cause some performance problem or bugs, so watch this
        return(eval(body))
        
def escape_args(args, body):
        #Replace the temporary variables with index variables: For instance, (define (square x) (* x x)) is mapped to [*, {0}, {0}]
        #And (define (sum-of_squares x y) (+ (square x) (square y))) becomes [+ [square, {0}] [square, {1}]]
        #The order of the variables is kept, but the names are anonymized
        for body_index in range(len(body)):
                if(is_list(body[body_index])):
                        body[body_index] = escape_args(args, body[body_index])
                else:
                        for args_index in range(len(args)):
                                if(body[body_index] == args[args_index]):
                                        body[body_index] = "{" + str(args_index) + "}"
        return body
        
def unescape_args(args, fun_body):
        #This is the opposite of escape_args - actual arguments are substituted into the body to replace the anonymous ones 
        body = list(fun_body)
        for body_index in range(len(body)):
                if(is_list(body[body_index])):
                        body[body_index] = unescape_args(args, body[body_index])
                else:
                        if(body[body_index][0] == '{' and body[body_index][-1] == '}'):
                                arg_index = int(body[body_index][1:-1])
                                body[body_index] = args[arg_index]
        return body
        
def parse(expression):
        #Converts a string expression to a list 'expression tree'
        expr = []
        buffer = ""
        char = ''
        index = 0
        numParens = 0
        while(index < len(expression)):
                char = expression[index]
                buffer += char
                if((char == ' ' or char == '\t' or char == '\n' or char == '\r') and numParens == 0):
                        #Whitespace\newline\tab is a delimiter, but only one counts
                        if(len(buffer) > 1):
                                expr.append(buffer[:-1])
                        buffer = ""
                elif(char == '('):
                        if(len(buffer) > 1 and numParens == 0):
                                expr.append(buffer[:-1])
                                buffer = ""
                        numParens += 1
                elif(char == ')'):
                        #Each parentheses block is a subexpression, so create a new list for it
                        numParens -= 1
                        if(numParens == 0):
                                if(buffer[0] == '('):
                                        expr.append(parse(buffer[1:-1]))
                                else:
                                        expr.append(parse(buffer[:-1]))
                                buffer= ""
                index += 1
        if(len(buffer) > 0):
                expr.append(buffer)
                #Add any trailing items
        return expr
        
#list: (a b c...)
def car(list): #Non-functional until quoting is implemented
        if(is_list(list)):
                return list[0]
        debug_print("car: " + str(list) + ", " + str(list[0]))
        return []

#list: (a b c...)
def cdr(list): #Non-functional until quoting is implemented
        if(is_list(list)):
                if(len(list) > 0):
                        return list[1:]
                else:
                        return []
        else:
                print("Error: <{0}> is not a list.".format(list))
                return []
                
def is_list(expression):
        try:
                if(not isinstance(expression, str)):
                        return(len(expression) > 1)
                return False
        except:
                return False
        
def is_number(value):
        return is_int(value) or is_float(value) or is_rational(value)

def is_float(value):
        try:
                float(value)
                return True
        except:
                return False                

def is_int(value):
        try:
                int(value)
                return True
        except:
                return False

def is_rational(value): #Non-functional
        try:
                num_den = value.split("/")
                if(len(num_den) != 2):
                        return False
                return(is_int(num_den[0]) and is_int(num_den[1]))
        except:
                return False

def is_variable(expression):
        debug_print("is_variable: " + expression)
        return(expression in variable_definitions.keys())
        
def is_quoted(expression): #Non-functional
        try:
                return (expression[0] == "'" or expression.find("quote") == 0)
        except:
                return False

def unquote(expression): #Non-functional
        if(expression[0] == "'"):
                return expression[1:]
        else:
                return expression[5:]

def debug_print(str):

        if(debug):
                print(str)

if(__name__ == "__main__"):
        run()

