from decimal import *
		
def main():
	
	exp = ""
	while(True):
		exp = input()
		if(exp == ""):
			break
		print(evaluate(exp))
		
def evaluate(expression):
	expr = parse(expression)
	debug_print("expression: <" + str(expr)+">")
	debug_print("start: <" + str(expr[0])+">")
	return eval(expr[0])

def eval(expression):
	if(is_list(expression)):
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
	if(function == "-"):
		difference = eval(expression[1])
		for subtrahend in expression[2:]:
			debug_print(subtrahend)
			difference -= eval(subtrahend)
		return difference
	if(function == "*"):
		product = 1
		for multiplicand in expression[1:]:
			debug_print(multiplicand)
			product *= eval(multiplicand)
		return product
	if(function == "/"):
		quotient = eval(expression[1])
		for divisor in expression[2:]:
			debug_print(divisor)
			quotient /= eval(divisor)
		return quotient
	elif(function == "car"):
		return car(expression[1:])

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
			numParens += 1
		elif(char == ')'):
			numParens -= 1
			if(numParens == 0):
				expr.append(parse(buffer[1:-1]))
				buffer = ""
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
	return []
	print("Error: List <{0}> is of length 0.".format(list))

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

def debug_print(str):
	#print(str) #Turn off this comment to enable debug printing
	str = ""
main()