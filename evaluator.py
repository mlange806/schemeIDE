from decimal import *
debug = False #Controls whether or not the debug statements are printed
function_definitions = dict()
variable_definitions = dict()
reserved_words = ["+", "-", "*", "/", "define", "if", "and", "or", "not", "cond", ">", "<", "=", ">=", "<=", "quote", "car", "cdr", "cons", "list"]
#@TODO:
#Next up: lists, quotes
#
#Math:
#Arbitrary precision arithmetic
#Rationals
#Unary division? (/ x) = 1/x
#
#
#Other features:
#List manipulation: car, cdr, cons, (list)?
#Lambda functions
#Let function
#Returning functions from functions (functional replacement)
#Passing functions? this might work already
#Inline definitions (define (define))
#Variadic functions (define (f . args))
#Nil/empty list constant
#pair?, null?, append function
#
#General:
#Error messages
#Arity checking
#Scoping, environments
#Clean up debug statements to actually be useful
#Stack limits: (* 8 (pi-sum 1 100-1000)) stops working eventually

def run():
#The main method that only gets invoked if evaluator.py is the calling program, for quick testing mostly
	while(True):
		exp = input()
		if(exp == ""):
			break
		else:
			print(parse(exp))
			print(evaluate(exp))
		
def evaluate(expression):
#Reads a string expression which is then parsed into a list 'tree' and evaluated
	debug_print("expression: " + str(expression))
	expr = parse(expression)
	debug_print("parsed: <" + str(expr)+">")
	return eval(expr[0])

def eval(expression):
#Reads an expression in list 'tree' form and evaluates the result
	if(is_list(expression)): #Anything that's not an atom
		return eval_function(expression)
	elif(is_int(expression)):
		return int(expression)
	elif(is_float(expression)): #Floats are implemented as Decimals
		return Decimal(expression)
	elif(is_rational(expression)): #Not implemented
		return expression
	elif(is_variable(expression)): #Technically, this checks if the expression represents a previously assigned variable
		return variable_definitions[expression]
	else:
		wrong("Unknown form: <{0}>".format(expression))

def eval_function(expression): #Handles anything that isn't an atom - applies the function to all the arguments
	#Arity checking coming soon
	function = expression[0]
	if(function in function_definitions.keys()): #User-defined functions take precedence over everything
		return(apply_function(function, expression[1:]))
	elif(function == "+"):
		sum = 0
		for summand in expression[1:]:
			try:
				sum += eval(summand)
			except Exception as e:
				wrong("Invalid operand for +: {0} in expression <{1}>: {2}".format(summand, expression, str(e)))
		return sum
	elif(function == "-"):
		if(len(expression[1:]) == 1): #Unary minus
			return eval(expression[1]) * -1
		difference = eval(expression[1])
		for subtrahend in expression[2:]:
			try:
				difference -= eval(subtrahend)
			except Exception as e:
				wrong("Invalid operand for -: {0} in expression <{1}>: {2}".format(summand, expression, str(e)))
		return difference
	elif(function == "*"):
		product = 1
		for multiplicand in expression[1:]:
			try:
				product *= eval(multiplicand)
			except Exception as e:
				wrong("Invalid operand for *: {0} in expression <{1}>: {2}".format(summand, expression, str(e)))
		return product
	elif(function == "/"):
		#Unary divide here, once rationals are implemented
		quotient = eval(expression[1])
		for divisor in expression[2:]:
			try:
				quotient /= eval(divisor)
			except Exception as e:
				wrong("Invalid operand for /: {0} in expression <{1}>: {2}".format(summand, expression, str(e)))
		return quotient
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
			debug_print("<{0}: {1}>".format(signature, variable_definitions[signature]))
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
	elif(function == "quote"):
		return expression[1]
	elif(function == "car"):
		return car(expression[1])
	elif(function == "cdr"):
		return cdr(expression[1])
	elif(function == "cons"):
		pair = [eval(expression[1])]
		pair.append(eval(expression[2]))
		return pair
	elif(function == "list"):
		return expression[1:]
	#elif(function == "null?"):
		#return (len(expression[1] == 0))
	else:
		debug_print("<{0}> is not a valid operator in expression <{1}>.".format(expression[0], expression))
		return None


def apply_function(name, args): #Applies the function to the arguments
	debug_print("Applying <{0}> to <{1}>".format(name, args))
	body = function_definitions[name]
	num_args = body[0]
	body = unescape_args(args, body[1])
	debug_print(body)
	#Here, we substitute (expand) the body of the function with the given arguments, instead of evaluating them as they come up
	#Remains to be seen if this is going to cause some performance problem or bugs, so watch this
	return(eval(body))

def escape_args(args, body):
	#Replace the temporary variables with index variables: For instance, (define (square x) (* x x)) is mapped to [*, {0}, {0}]
	#And (define (sum-of_squares x y) (+ (square x) (square y))) becomes [+ [square, {0}] [square, {1}]]
	#The order of the variables is kept, but the names are anonymized
	if(not is_list(body)):
		for args_index in range(len(args)):
				if(body == args[args_index]):
					body = "{" + str(args_index) + "}"
		return body
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
	if(not is_list(fun_body)):
		if(fun_body[0] == '{' and fun_body[-1] == '}'):
				arg_index = int(fun_body[1:-1])
				body = args[arg_index]
		return body
	body = list(fun_body)
	for body_index in range(len(body)):
		if(is_list(body[body_index])):
			body[body_index] = unescape_args(args, body[body_index])
		else:
			if(body[body_index][0] == '{' and body[body_index][-1] == '}'):
				arg_index = int(body[body_index][1:-1])
				body[body_index] = args[arg_index]
	return body

def unquote(expression):
	quote_index = expression.find("'")
	if(quote_index < 0):
		return expression
	new_expression = expression[:quote_index]
	rest = expression[quote_index+1:]
	new_expression += "(quote "
	if(rest[0] == '('):
		num_parens = 0
		index = 0
		while(index < len(rest)):
			char = rest[index]
			new_expression += char
			if(char == '('):
				num_parens += 1
			elif(char == ')'):
				num_parens -= 1
				if(num_parens == 0):
					new_expression += ")" + rest[index+1:]
					if(new_expression.find("'") < 0):
						return new_expression
					else:
						return unquote(new_expression)
			index += 1
	else:
		index = 0
		while(index < len(rest)):
			char = rest[index]
			if(char not in ['(', ' ', ')']):
				new_expression += char
			else:
				new_expression += ")" + rest[index:]
				if(new_expression.find("'") < 0):
					return new_expression
				else:
					return unquote(new_expression)
			index += 1
	debug_print("Something went wrong")
	return expression

def parse(expression):
	expression = unquote(expression)
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
	if(numParens != 0):
		wrong("Mismatched parentheses in {0}".format(expression))
	return expr

#list: (a b c...)
def car(list): #Non-functional until quoting is implemented
	list = eval(list)
	if(is_list(list)):
		return list[0]
	debug_print("car: " + str(list) + ", " + str(list[0]))
	return []

#list: (a b c...)
def cdr(list): #Non-functional until quoting is implemented
	list = eval(list)
	if(is_list(list)):
		if(len(list) > 0):
			return list[1:]
		else:
			return []
	else:
		debug_print("Error: <{0}> is not a list.".format(list))
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
	return(expression in variable_definitions.keys())

def is_quoted(expression): #Non-functional
	try:
		return (expression[0] == "'" or expression.find("quote") == 0)
	except:
		return False
		
def debug_print(str):
	if(debug):
		print(str)

def wrong(str):
	raise Exception(str)

def display_variables():
	print(str(variable_definitions))

def display_functions():
	print(str(function_definitions))

if(__name__ == "__main__"):
	run()