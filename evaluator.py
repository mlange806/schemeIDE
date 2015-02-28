from decimal import *
debug = False
function_definitions = dict()
variable_definitions = dict()

def run():
	print(evaluate("(define radius 10)"))
	print(evaluate ("(2 2)"))
	#print(evaluate("(define circumference (* 2 pi radius))"))
	print(evaluate("(define (square x) (* x x))"))
	print(evaluate("(define (sum-of-squares x y)(+ (square x) (square y)))"))
	print(evaluate("(square 5)"))
	print(evaluate("(square (square 3))"))
	print(evaluate("(sum-of-squares 3 4)"))
	print(evaluate("(sum-of-squares (square 3) (square 4))"))
	exp = ""
	while(False):
		exp = input()
		if(exp == ""):
			break
		print(evaluate(exp))
		
def evaluate(expression):
	debug_print("expression: " + str(expression))
	expr = parse(expression)
	debug_print("expression: <" + str(expr)+">")
	debug_print("start: <" + str(expr[0])+">")
	return eval(expr[0])

def eval(expression):
	#@TODO: Quotes
	if(is_quoted(expression)):
		debug_print("quote")
		return unquote(expression)
	elif(is_list(expression)):
		debug_print("list")
		return eval_function(expression)
	elif(is_int(expression)):
		debug_print("int")
		return int(expression)
	elif(is_float(expression)):
		debug_print("float")
		return Decimal(expression)
	elif(is_rational(expression)):
		debug_print("rational")
		return expression
	else:
		debug_print("unknown")

def eval_function(expression):
	function = expression[0]
	#@TODO: Implement rationals
	#@TODO: Check arity
	if(function == "+"):
		sum = 0
		for summand in expression[1:]:
			debug_print(summand)
			sum += eval(summand)
		return sum
	elif(function == "-"):
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
		quotient = eval(expression[1])
		for divisor in expression[2:]:
			debug_print(divisor)
			quotient /= eval(divisor)
		return quotient
	elif(function == "car"):
		return car(eval(expression[1:][0]))
	elif(function == "define"):
		signature = expression[1]
		body = expression[2]
		if(is_list(signature)):
			args = len(signature) - 1
			function_definitions[signature[0]] = (args, escape_args(signature[1:], body))
			debug_print(function_definitions[signature[0]])
		else:
			variable_definitions[signature[0]] = eval(body)
		debug_print("<{0}: {1}>".format(signature, body))
	else:
		if(function in function_definitions.keys()):
			return(apply_function(function, expression[1:]))
		else:
			debug_print("<{0}> is not a valid operator.".format(expression[0]))
			return None

			
def apply_function(name, args):
	debug_print(str(function_definitions))
	body = function_definitions[name]
	num_args = body[0]
	body = unescape_args(args, body[1])
	return(eval(body))
	
def escape_args(args, body):
	for body_index in range(len(body)):
		if(is_list(body[body_index])):
			body[body_index] = escape_args(args, body[body_index])
		else:
			for args_index in range(len(args)):
				if(body[body_index] == args[args_index]):
					body[body_index] = "{" + str(args_index) + "}"
	return body
	
def unescape_args(args, fun_body):
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
	expr = []
	buffer = ""
	char = ''
	index = 0
	numParens = 0
	while(index < len(expression)):
		char = expression[index]
		buffer += char
		if(char == ' ' and numParens == 0):
			if(len(buffer) > 1):
				expr.append(buffer[:-1])
			buffer = ""
		elif(char == '('):
			if(len(buffer) > 1 and numParens == 0):
				expr.append(buffer[:-1])
				buffer = ""
			numParens += 1
		elif(char == ')'):
			numParens -= 1
			if(numParens == 0):
				expr.append(parse(buffer[1:-1]))
				buffer= ""
		index += 1
	if(len(buffer) > 0):
		expr.append(buffer)
	return expr
	
def sch_print(expression):
	print("V: " + str(expression))
	if(is_int(expression)):
		print(expression)
	elif(is_float(expression)):
		print(expression)
	elif(is_rational(expression)):
		print(expression[0] + "/" + expression[1])
#list: (a b c...)
def car(list):
	if(is_list(list)):
		return list[0]
	debug_print("car: " + str(list) + ", " + str(list[0]))
	return []

#list: (a b c...)
def cdr(list):
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
			return len(expression) > 1
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

def is_rational(value):
	try:
		num_den = value.split("/")
		if(len(num_den) != 2):
			return False
		return(is_int(num_den[0]) and is_int(num_den[1]))
	except:
		return False

def is_quoted(expression):
	try:
		return (expression[0] == "'" or expression.find("quote") == 0)
	except:
		return False

def unquote(expression):
	if(expression[0] == "'"):
		return expression[1:]
	else:
		return expression[5:]

def debug_print(str):
	if(debug):
		print(str)

if(__name__ == "__main__"):
	run()