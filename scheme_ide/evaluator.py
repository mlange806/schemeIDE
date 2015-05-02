from decimal import *

#This is a recursive evaluator for (a subset of) the Scheme language
#supported_functions = [+, -, *, /, define, if, and, or, not, cond, >, <, =, >=, <=, quote, car, cdr, cons, list, null?, remainder, lambda]
#There are 3 public methods: evaluate, list_print, and reference_highlight
#To evaluate an expression, call evaluate with the string representation of that expression in Scheme syntax.
#list_print converts an expression in our 'expression tree' list syntax to one in Scheme syntax, see the method for more information
#reference_highlight returns information to allow reference highlighting in the editor, see the method for more information
#
#The basic functionality of the evaluator is to detect functions, then apply those functions to their arguments
#More information can be found on the Team 8 blog
#
#

definitions = dict()
#definitions stores the state of the evaluator - every user-defined function and variable is stored here
#The format is [<number_of_arguments>, <body>]
#If number_of_arguments is 0, then body is an atom representing the value of a variable
#Otherwise, the body is a list representing a Scheme function
#To get the value of a variable or the body of a function, be careful to use definitions[<variable_or_function_name>][1], [0] will get the number of arguments
"""Reads a string expression which is then parsed into a 'tree' represented by a python list and evaluated - see __parse() and __eval()
If there are multiple expressions, each is evaluated independently and the result is returned as a list"""
def evaluate(expression):
	try:
		expr = __parse(expression) #Begin by parsing the expression so it can be evaluated
	except Exception as e: #If the expression is syntactically inorrect, we can't evaluate it so just error here.
		return "Error: " + str(e) #All errors begin with "Error:" for easy detection
	returns = [] #This is the list of outputs to be returned, one for each expression
	for subexpr in expr: #Evaluate each individual Scheme expression independently and in order
		try:
			value = __eval(subexpr) #Evaluate the expression
			if(__is_list(value) or __is_single_list(value)): #If the output is a python list, then convert it to a quoted Scheme list: i.e. ['1', '2', ['3', '4']] becomes '(1 2 (3 4)) - see list_print
				returns.append("'{0}".format(list_print(value)))
			else:
				returns.append(value)
		except Exception as e: #If the expression can't be evaluated, an exception will be returned from __eval(), so catch that and pass it up again with an "Error:" prepended to maintain consistency
		#Exceptions in the evaluation sometimes stack, so the prefix is added here at the top level for readability
			returns.append("Error: " + str(e))
			break
	if(not __is_list(returns)):
		return returns[0] #If there's only one return value (i.e. it's not a list), then return it alone
	return returns #Otherwise just return the list of outputs
	
"""Reads an expression in list 'tree' form, evaluates it and returns the result"""
def __eval(expression):
	if(__is_list(expression)): #Anything that's not an atom is a function
		return __eval_function(expression)
	elif(__is_string(expression)): #A string's value is just itself
		return expression;
	elif(__is_int(expression)): #Same with an integer
		return int(expression)
	elif(__is_float(expression)): #Or a float, which is implemented with Decimal
		return Decimal(expression)
	elif(__is_defined_variable(expression)): #A variable 
		return definitions[expression][1] #Return the value of that variable
	else: #Nothing else is supported, so if you fall through to this case there's a problem - usually undefined variables
		__wrong("Unknown form or undeclared variable: <{0}>".format(list_print(expression))) #test_input:5

"""Handles anything that isn't an atom - applies the function to all the arguments
In Scheme, the syntax of a function is (<function_name> <argument_1> <argument_2> ... <argument_n>)"""
def __eval_function(expression):
	function_name = expression[0] #The first element of the expression is the function name, as above
	#Check for all predefined functions. If it's none of them, it's a user-defined function so we call __apply_function()
	#This would be a switch statement, but python does not have a switch statement
	if(__is_list(function_name)):
	#If the function name is itself a list, then this expression is evaluating a lambda function
	#e.g. ((lambda (x) (* x x)) 5)
	#In this case, we evaluate the function name to get the lambda function, then apply the arguments to it
		return(__apply_function(__eval(function_name), expression[1:]))
	if(function_name in definitions.keys() and definitions[function_name][0] > 0): #Check the function name exists and is not a variable
	#User-defined functions take precedence over everything - users are allowed to overwrite standard function definitions, although it's not recommended
		return(__apply_function(definitions[function_name], expression[1:], function_name))
	#For the following 4 mathematical operators, an exception is thrown if any argument doesn't evaluate to a number
	elif(function_name == "+"):
	#+ can take 1 or more arguments, evaluates all the argument and then adds then together
		sum = 0
		for term in expression[1:]:
			try:
				summand = __eval(term)
				if(not __is_number(summand)): #Check each term to make sure it's a valid number, otherwise throw an exception
					__wrong("'{0}' is not a number".format(list_print(summand))) #test_input:6
				sum += summand
			except Exception as e:
				__wrong("Invalid operand for +: {0} in expression <{1}>: {2}".format(list_print(term), list_print(expression), str(e))) #test_input:7
		return sum
		
	elif(function_name == "-"):
	#- can take 1 or more arguments. If there's only one, then it's unary minus - return the negative of that argument. Otherwise, it returns arg1 - arg2 - arg3 - ... - argN
		term1 = __eval(expression[1])
		if(not __is_number(term1)):
			__wrong("Invalid operand for -: {0} in expression <{1}>".format(list_print(term1), list_print(expression))) #test_input:8
		if(len(expression[1:]) == 1): #Unary minus
			return term1 * -1
		difference = term1 #Start out with term1, then subtract each subsequent term
		for term in expression[2:]:
			try:
				subtrahend = __eval(term)
				if(not __is_number(subtrahend)):
					__wrong("'{0}' is not a number".format(list_print(subtrahend))) #test_input:9
				difference -= subtrahend
			except Exception as e:
				__wrong("Invalid operand for -: {0} in expression <{1}>: {2}".format(list_print(term), list_print(expression), str(e))) #test_input:10
		return difference
		
	elif(function_name == "*"):
	#* takes 1 or more arguments, evaluates them and multiplies them all together
		product = 1 #Start with the multiplicative identity
		for term in expression[1:]:
			try:
				multiplicand = __eval(term)
				if(not __is_number(multiplicand)):
					__wrong("'{0}' is not a number".format(list_print(multiplicand))) #test_input:11
				product *= multiplicand
			except Exception as e:
				__wrong("Invalid operand for *: {0} in expression <{1}>: {2}".format(list_print(term), list_print(expression), str(e))) #test_input:12
		return product
		
	elif(function_name == "/"):
	#/ takes 1 or more arguments. If there's only one, then it's a unary divide - 1/arg1. Otherwise, it returns (((arg1 / arg2) / arg3) ... / argN)
		quotient = __eval(expression[1]) #Need this value for any number of arguments - for unary, this is the denominator, for multiple it's the starting value
		if(not __is_number(quotient)):
			__wrong("Invalid operand for /: {0} in expression <{1}>".format(list_print(quotient), list_print(expression))) #test_input:13
		if(len(expression[1:]) == 1): #Unary divide
			if(quotient == 0):
				wrong("Cannot divide by zero") #test_input:35
			else:
				return 1 / quotient
		for term in expression[2:]:
			try:
				divisor = __eval(term)
				if(not __is_number(divisor)):
					__wrong("'{0}' is not a number".format(list_print(divisor))) #test_input:14
				elif(divisor == 0): #Python probably throws an exception for this, but it's neater to generate our own exception 
					__wrong("Cannot divide by zero") #test_input:15
				quotient /= divisor
			except Exception as e:
				__wrong("Invalid operand for /: {0} in expression <{1}>: {2}".format(list_print(term), list_print(expression), str(e))) #test_input:16
		return quotient
	
	elif(function_name == "define"):
	#define is the keyword that allows you to define your own functions in Scheme
	#There are three basic uses:
	#(define <variable_name> <variable_value>) - this assigns whatever variable_value evaluates to as the value of variable_name
	#(define (<function_name> <arg1> <arg2> ... <argN>) <function_body>) - this defines a function that takes N arguments, with name function_name and body function_body
	#(define function_name (lambda (<arg1> <arg2> ... <argN>) <lambda_body>)) - lambda creates a function with N arguments, with body function_body and no name, which is then assigned to function_name
	#Each case is detected and handled separately
		signature = expression[1] #This is either a single element or a list
		body = expression[2]
		if(__is_list(signature)): #If signature has 2+ arguments, this is defining a function
			definitions[signature[0]] = __escape_args(signature[1:], body) #This generates a function from the argument list and the body
			#Define the function to be the body, with the variables replaced by generics: see __escape_args()
		else: #This is defining a variable or assigning a name to a lambda function, so either set the value of the variable or the function
			value = __eval(body)
			if(__is_list(body) and body[0] == "lambda"): #lambda
				definitions[signature] = value #If it's a lambda, value will contain the number of arguments and the function body
			else:
				definitions[signature] = [0, value] #Otherwise for a variable, the number of arguments is 0
				
	elif(function_name == "if"):
	#The syntax of an if is (if <predicate> <consequent> <alternative>)
	#If predicate is true, evaluate and return consequent
	#If predicate is false, evaluate and return alternative
	#In the evaluator, we use #t and #f to denote true and false respectively, to avoid python's annoying type-casting behavior
		predicate = __eval(expression[1])
		consequent = expression[2]
		alternative = expression[3]
		if(predicate == "#t"):
			return __eval(consequent)
		elif(predicate == "#f"):
			return __eval(alternative)
		else:
			__wrong("Improper form in predicate of 'if': <{0}>".format(list_print(predicate))) #test_input:17
			
	elif(function_name == "and"):
	#The syntax of an and is (and <condition1> <condition2> ... <conditionN>)
	#Conditions are evaluated in order until one of them is false, then false is returned (#f)
	#If no conditions are false, true is returned (#t)
	#If one of the conditions isn't a boolean #t/#f value, throw an exception
		for term in expression[1:]:
			predicate = __eval(term)
			if(predicate == "#f"):
				return "#f"
			elif(not predicate == "#t"):
				__wrong("Improper value in predicate of 'and': <{0}>".format(list_print(predicate))) #test_input:18
		return "#t"
		
	elif(function_name == "or"):
	#The syntax of an or is (or <condition1> <condition2> ... <conditionN>)
	#Conditions are evaluated in order until one of them is true, then true is returned (#t)
	#If no conditions are true, false is returned (#f)
	#If one of the conditions isn't a boolean #t/#f value, throw an exception
		for term in expression[1:]:
			predicate = __eval(term)
			if(predicate == "#t"):
				return "#t"
			elif(not predicate == "#f"):
				__wrong("Improper value in predicate of 'or': <{0}>".format(list_print(predicate))) #test_input:19
		return "#f"
		
	elif(function_name == "not"):
	#The syntax of a not is (not <condition>)
	#If condition is #t, return #f
	#If condition is #f, return #t
	#If it's neither, throw an exception
		predicate = __eval(expression[1])
		if(predicate == "#t"):
			return "#f"
		elif(predicate == "#f"):
			return "#t"
		else:
			__wrong("Improper value in predicate of 'not': <{0}>".format(list_print(predicate))) #test_input:20
			
	elif(function_name == "cond"):
	#The syntax for cond is (cond (<predicate1> <expression_list1>) (<predicate2> <expression_list2>) ... (<predicateN> <expression_listN>) [(else <expression_else>)])
	#Each predicate is evaluated in order. If it's true, all the expressions in the corresponding expression_list are evaluated and the value of the last one is returned.
	#If none is true, then the expression_else is evaluated and its function is returned.
	#If no predicate is true and there is no else block, throw an exception.
		for pair in expression[1:]: #For each predicate, expression_list pair
			term = pair[0] #This is either the predicate or 'else'
			consequent = pair[1:] #This is an expression_list
			if(term == "else"): #If you see an else, evaluate the associated expression_list no matter what
				if(len(pair) == 2): #If there's only two things in the pair, the expression_list is a single expression
					return __eval(consequent[0]) #So just eval it and return
				value = "";
				for cons in consequent: #Otherwise, evaluate the whole list in order and then return the last one
					value = __eval(cons)
				return value
			else: #If this isn't an else, it's a predicate 
				predicate = __eval(term)
				if(predicate == "#t"): #If it evaluates to true (#t), then evaluate the expression_list and return just like for an 'else'
					if(len(pair) == 2):
						return __eval(consequent[0])
					value = "";
					for cons in consequent:
						value = __eval(cons)
					return value
				elif(not predicate == "#f"): #Predicate must evaluate to either #t or #f
					__wrong("Improper value in predicate of 'cond': <{0}>".format(list_print(predicate))) #test_input:21
		__wrong("No true predicate in 'cond' and no else statement: <{0}>".format(list_print(expression))) #test_input:22
		
	#Both arguments to the following 5 boolean operators must be numbers, otherwise an exception is thrown
	elif(function_name == ">"):
	#Syntax for > is (> <expression1> <expression2>)
	#These are pretty self-explanatory - evaluate both expressions and compare
		try:
			if(__eval(expression[1]) > __eval(expression[2])):
				return "#t"
			return "#f"
		except:
			__wrong("Both arguments to > must be numbers: <{0}>".format(list_print(expression))) #test_input:23
			
	elif(function_name == "<"):
	#Syntax for < is (< <expression1> <expression2>)
		try:
			if(__eval(expression[1]) < __eval(expression[2])):
				return "#t"
			return "#f"
		except:
			__wrong("Both arguments to < must be numbers: <{0}>".format(list_print(expression))) #test_input:24
			
	elif(function_name == "="):
	#Syntax for = is (= <expression1> <expression2>)
		try:
			#Here, the +1-1 tests that both arguments are numbers, otherwise python's == is too broad and won't catch type mismatches
			if((__eval(expression[1])+1-1) == (__eval(expression[2])+1-1)):
				return "#t"
			return "#f"
		except:
			__wrong("Both arguments to = must be numbers: <{0}>".format(list_print(expression))) #test_input:25
			
	elif(function_name == "<="):
	#Syntax for <= is (<= <expression1> <expression2>)
		try:
			if(__eval(expression[1]) <= __eval(expression[2])):
				return "#t"
			return "#f"
		except:
			__wrong("Both arguments to <= must be numbers: <{0}>".format(list_print(expression))) #test_input:26
			
	elif(function_name == ">="):
	#Syntax for >= is (>= <expression1> <expression2>)
		try:
			if(__eval(expression[1]) >= __eval(expression[2])):
				return "#t"
			return "#f"
		except:
			__wrong("Both arguments to >= must be numbers: <{0}>".format(list_print(expression))) #test_input:27
	
	elif(function_name == "quote"):
	#Syntax for quote is (quote <expression>)
	#If the expression is an atom, return the value of that atom
	#Otherwise return the atom itself
		if(__is_int(expression[1])):
			return int(expression[1])
		elif(__is_float(expression[1])):
			return float(expression[1])
		return expression[1] #This handles strings, lists, and variables
		
	elif(function_name == "car"):
	#Syntax for car is (car <list>)
	#Returns the first element of the list
	#If list isn't an actual list, then throw an exception
		list = __eval(expression[1])
		if(__is_list(list)):
			return list[0]
		__wrong("car: <{0}> is not a list.".format(list_print(list))) #test_input:28
		
	elif(function_name == "cdr"):
	#Syntax for cdr is (cdr <list>)
	#Returns list with the first element removed
	#If list isn't an actual list, then throw an exception
		list = __eval(expression[1])
		if(__is_list(list)):
			if(len(list) > 0):
				return list[1:]
		elif(__is_single_list(list)):
			return []
		else:
			__wrong("cdr: <{0}> is not a list.".format(list_print(list))) #test_input:29
			
	elif(function_name == "cons"):
	#Syntax for cons is (cons <expression1> <expression2>)
	#Returns '(expression1 expression2)
		if(len(expression) != 3):
			__wrong("cons expects 2 arguments, got {0}".format(len(expression) - 1)) #test_input:30
		pair = [__eval(expression[1])]
		pair.append(__eval(expression[2]))
		return pair
		
	elif(function_name == "list"):
	#Syntax for list is (list <expression1> <expression2> ... <expressionN>)
	#Returns '(expression1 expression2 ... expressionN)
	#Because of the way lists are expressed as python lists, we can just return everything except the keyword list and it automatically becomes a list
		return expression[1:]
		
	elif(function_name == "null?"):
	#Syntax for null? is (null? <list>)
	#Returns #t if list is '(), the empty list
	#Otherwise it returns #f
		if(__eval(expression[1]) == []):
			return "#t"
		else:
			return "#f"
			
	elif(function_name == "remainder"):
	#Syntax for remainder is (remainder <expression1> <expression2>)
	#Returns expression1 % expression2
	#If either expression isn't a valid number, that will be caught by the % operator
		return __eval(expression[1]) % __eval(expression[2])
		
	elif(function_name == "lambda"):
	#Syntax for lambda is (lambda (<arg1> <arg2> ... <argN>) <function_body>)
	#The arguments and the function body get passed to __escape_args(), which creates the function and returns it
		return __escape_args(expression[1], expression[2])
		
	else:
	#If it's not a user-defined function or a predefined function, throw an exception
		__wrong("<{0}> is not a valid operator in expression <{1}>.".format(expression[0], list_print(expression))) #test_input:31
		return None

"""This function evaluates user-defined functions. Given the body of a function and a list of arguments, it combines them into a valid Scheme expression, evaluates that expression and returns the value. Performs arity checking."""
def __apply_function(fun_body, args, function_name = "lambda"): 
	#Recall a function is stored in definitions[] as [<number_of_arguments>, <body>]	
	body = fun_body[1]
	required_args = fun_body[0] #The number of arguments the function was defined for
	given_args = len(args) #The actual number of arguments given here
	if(required_args != given_args): #If they're not equal, obviously that's a problem
		__wrong("Incorrect number of arguments for function <{0}>: The function takes {1} argument{2} but {3} were given".format(function_name, required_args, "s"*(1 - (int)(1/required_args)), given_args)) #test_input:33
	body = __unescape_args(args, fun_body) #If the number of arguments match, substitute the arguments into the body, evaluate and return
	return(__eval(body))

"""This function takes as input a list of named arguments and a function body, and returns a function with those named arguments replaed by generic variables to facilitate later evaluation."""
def __escape_args(args, body):
	#Replace the temporary variables with index variables: For instance, (define (square x) (* x x)) is mapped to [*, {0}, {0}]
	#And (define (sum-of_squares x y) (+ (square x) (square y))) becomes [+ [square, {0}] [square, {1}]]
	#The order of the variables is kept, but the names are anonymized
	#Essentially, every element of the body is checked and if it matches the name of a variable, it's replaced with the index of that variable in the arg list
	
	if(not __is_list(body)): #If the body is a single element, then we're escaping a subexpression of the body
		for args_index in range(len(args)): #Check all the args in the list to see if they match the body
				if(body == args[args_index]):
					body = "{" + str(args_index) + "}" #If they do, replace the body with the index of the matching variable
		return [len(args), body] #And return
	for body_index in range(len(body)): #Otherwise for a list, iterate through the elements
		if(__is_list(body[body_index])): #If those elements are themselves lists, escape those lists too
			body[body_index] = __escape_args(args, body[body_index])
		else:
			for args_index in range(len(args)): #Otherwise check the arguments and replace any matches, as above
				if(body[body_index] == args[args_index]):
					body[body_index] = "{" + str(args_index) + "}"
	return [len(args), body]

"""This function takes as input a list of actual arguments and a function body with generic arguments (as generated by __escape_args()), replaces the generics with the actual arguments and returns that body which can then be evaluated."""
def __unescape_args(args, fun_body):
	#This is the opposite of escape_args - actual arguments are substituted into the body to replace the anonymous ones
	#Every element of fun_body is checked and if it's a generic argument of the form {n} for an integer n, replace it with the nth argument
	#Arity checking is already performed in __apply_function(), so we skip it here
	
	fun_body = fun_body[1]
	if(not __is_list(fun_body)): #For a single element
		if(fun_body[0] == '{' and fun_body[-1] == '}'): #If it's a generic argument
			arg_index = int(fun_body[1:-1]) #Get the number of the argument
			body = args[arg_index] #And replace it
		else:
			body = fun_body
		return body
	body = list(fun_body)
	for body_index in range(len(body)): #Otherwise, do the same thing as above, but recursively to check all elements
		if(__is_list(body[body_index])):
			body[body_index] = __unescape_args(args, body[body_index])
		else:
			if(body[body_index][0] == '{' and body[body_index][-1] == '}'):
				arg_index = int(body[body_index][1:-1])
				body[body_index] = args[arg_index]
	return body

"""This method converts the quote form '(1 2 3) to (quote (1 2 3)) - the apostrophe form is syntactic sugar for the quote function anyway, and this maintains consistency with the standard Scheme syntax to make eval() easier to write."""
def __unquote(expression):
	#Check for any instance of '<expression> and replace it with (quote <expression>)
	#There's a little work to be done to find the matching parenthesis of the expression
	
	quote_index = expression.find("'")
	if(quote_index < 0): #If the expression does not contain an apostrophe, don't need to do any replacement
		return expression
	new_expression = expression[:quote_index] #This is everything that comes before the apostrophe, which is kept verbatim
	rest = expression[quote_index+1:] #This is everything after
	new_expression += "(quote " #Replace the apostrophe with the quote function
	if(rest[0] == '('):
	#If the quoted expression was in parentheses, we need to find the matching one so we know the scope of the quote
		num_parens = 0 #Basic parentheses matching technique: keep a count of parenthese, increment on an open paren and decrement on a close paren
		index = 0
		while(index < len(rest)): #Check every character
			char = rest[index]
			new_expression += char #Add it to the new expression so that by the end, it contains the whole quoted expression
			if(char == '('): #Increment on open
				num_parens += 1
			elif(char == ')'): #Decrement on close
				num_parens -= 1
				if(num_parens == 0): #Found the matching parenthesis
					new_expression += ")" + rest[index+1:] #Add the close paren for the quote function, then add the rest of the expression
					if(new_expression.find("'") < 0): #If the new expression contains no apostrophes, it's done
						return new_expression
					else:
						return __unquote(new_expression) #Otherwise unquote again
			index += 1
	else:
	#Otherwise, it's an atom that's being quoted (e.g. 'atomName)
		index = 0
		while(index < len(rest)):
			char = rest[index]
			if(char not in ['(', ' ', ')', '\t', '\r', '\n']): #The only delimiters are whitespace (space, tab, newline chars) and parentheses
				new_expression += char #If it's not any of these, then we're still in the body of the atom
			else: #Once you see one of these, then the atom is over so we close the quote paren and add the rest of the expression
				new_expression += ")" + rest[index:]
				if(new_expression.find("'") < 0): #And of course check for more quotes
					return new_expression
				else:
					return __unquote(new_expression)
			index += 1
	#If the expression is only 'atomName, we need a closing parenthesis because the while loop above doesn't catch that
	return new_expression + ")"

"""This function converts an expression in Scheme syntax to a python list representing that expression. Essentially every parentheses block becomes its own list or sublist, where the elements are the atoms inside that parentheses block."""
def __parse(expression):
	expression = expression.strip() #Trim whitespace
	expression = __unquote(expression) #Convert apostrophes to quote functions to maintain consistency
	#Converts a string expression to a list 'expression tree'
	expr = [] #This is the list that will become our expression
	buffer = ""
	char = ''
	index = 0
	numParens = 0 #This detects parentheses blocks
	while(index < len(expression)): #Go through the expression character by character
		char = expression[index]
		buffer += char #Add it to the buffer, which builds names
		if((char == ' ' or char == '\t' or char == '\n' or char == '\r') and numParens == 0):
			#Whitespace\newline\tab is a delimiter, but only one counts
			if(len(buffer) > 1): #The newline char is in the buffer, so check for len > 1
				expr.append(buffer[:-1]) #If anything is in the buffer, add it as a new list element
			buffer = "" #And clear the buffer
		elif(char == '('): #Parentheses are also a delimiter, so perform the same logic
			if(len(buffer) > 1 and numParens == 0): #However, parentheses blocks need to be their own sublists, so don't append to the expression if we're inside a block
				expr.append(buffer[:-1])
				buffer = ""
			numParens += 1
		elif(char == ')'): #This is the end of a parentheses block
			numParens -= 1
			if(numParens == 0):
			#If you're back up to the top level, then you have an entire parentheses block here
			#So create a list from the block read so far (by calling __parse()) and then append that list to the expression
				if(buffer[0] == '('):
					expr.append(__parse(buffer[1:-1])) #Strip off opening and closing parentheses
				else:
					expr.append(__parse(buffer[:-1]))
				buffer= ""
		index += 1
	if(len(buffer) > 0):
		expr.append(buffer)
		#Add any trailing items
	if(numParens != 0): #Gotta have those matching parentheses
		__wrong("Mismatched parentheses in <{0}>".format(list_print(expression))) #test_input:34
	return expr
	
"""This function returns true if the input expression is a python list of length at least 2, false otherwise."""
def __is_list(expression):
	try:
		if(not isinstance(expression, str)):
			return(len(expression) > 1)
		return False
	except:
		return False

"""This function returns true if the input expression is a python list of length 1, false otherwise. We need both this and __is_list() to check for different variations in our list formats."""
def __is_single_list(expression):
	try:
		if(not isinstance(expression, str)):
			return(len(expression) == 1)
		return False
	except:
		return False

"""This function returns true if the input expression is a valid integer or floating-point number, false otherwise."""
def __is_number(value):
	return __is_int(value) or __is_float(value)

"""This function returns true if the input expression is a valid integer number, false otherwise."""
def __is_int(value):
	try:
		int(value)
		return True
	except:
		return False
		
"""This function returns true if the input expression is a valid floating-point number, false otherwise."""
def __is_float(value):
	try:
		float(value)
		return True
	except:
		return False

"""This function returns true if the input expression represents a string - i.e. "<string_value>", false otherwise."""
def __is_string(value):
	if(not __is_list(value)):
		if(value[0] == '"' and value[-1] == '"'):
			return True

"""This function returns true if the expression refers to a variable in definitions[], false otherwise."""
def __is_defined_variable(expression):
	return(expression in definitions.keys() and definitions[expression][0] == 0)

"""This function converts our python list format back to Scheme formatting, for printing."""
def list_print(expr):
	#Essentially our python lists get replaced with parentheses blocks
	list_string = "(" #Open with an open paren
	if(__is_list(expr) or __is_single_list(expr)): #If it's a list, write out every element of the list
		for i in range(len(expr)):
			if(__is_list(expr[i])):
				list_string += list_print(expr[i]) + " "  #Sublists get their own parentheses blocks
			elif(__is_single_list(expr[i])):
				list_string += list_print(expr[i])
			else:
				list_string += str(expr[i]) + " "
	else:
		return str(expr)
	list_string = list_string[:-1] + ")"
	return list_string
	
"""This function throws an exception with the given input string as its value. This allows us to standardize our exception handling."""
def __wrong(str):
	raise Exception(str)
	
#Reference highlighting section
#These global variables are needed to convert our nested list format to a linear list
tokens, scopetokens = [], [] #tokens will be the list of tokens, scopetokens will be the list of tokens with scopes added
#For instance, suppose the code is (define (square x) ((lambda (x) (* x x)) x))
#Tokens will be ['define', 'square', 'x', 'lambda', 'x', '*', 'x', 'x', 'x'], just the list of all the tokens in order
#Scopetokens will be ['arg0/define', 'arg0/square', 'arg0/x', 'arg0/arg1/lambda', 'arg0/arg1/x', 'arg0/arg1/*', 'arg0/arg1/x', 'arg0/arg1/x', 'arg0/x']
#As you can see, the x atoms inside the lambda function are arg0/arg1/x, different from the ones outside which are arg0/x
#So the scoped name identifies which x is being referred to
scope = "" #This keeps track of the current scope
count = 0

"""This function reads in a list of input as specified, then returns that input with information added to enable the editor to highlight matching references to a given atom."""
def reference_highlight(data):
	#The format of data is:
	#data[0] is the full text of the expression
	#data[1] is the name of the atom being highlighted
	#data[2] is the position of the atom in the full text
	#data[3] is the position of the atom in the window, which we do not use
	#data[4] is a list of instances of the format [<text_position>, <window_position>, 0]
	#This list of instances will be modified: The third element will be set to 2 if that instance is the definition of the atom, and set to 1 if it is a reference to the same atom
	
	global tokens, count, scopetokens
	tokens = []
	scopetokens = [] #Clear the token lists, since they're global
	text = data[0] #The full text
	exp = __parse(text) #We need to parse the text into an expression to be able to determine scopes
	__tokenize_linear(exp) #Write the tokens out
	__addscopes(exp) #And add the scopes
	count = 0
	start_index = data[2] #This is the index of the atom in the text
	instances = data[4] #This is our list of instances
	reference_name = data[1] #And finally, this is the name of the atom
	reference_index = -1
	for i in range(len(instances)):
	#Check each instance in the list to see if its text position matches the text position of our atom
	#This allows us to convert from text position to instance number - e.g. we can know the atom at position 15 is the 3rd instance
		if(instances[i][0] == start_index):
			reference_index = i
			break
	if(reference_index == -1): #If this happens, invalid data was passed to us
		raise Exception("Something went wrong with " + str(data) + ", could not find a reference")
	tokenindex = -1
	count = -1
	
	#We need to determine the scoped name of our atom to know exactly which variable it's referring to
	#So we go along the instance list until we find our instance number, while keeping track of the token number
	#When we find our instance number, the scoped name is at the index of the token number
	for i in range(len(tokens)):
		tokenindex += 1
		#Keep track of location in the token list
		if(tokens[i] == reference_name):
		#If you see the same atom name, move up in the instance list
			count += 1
			if(reference_index == count):
			#This means we found our original atom
				break
	scope_name = scopetokens[tokenindex] #And now we get the scope name
	firstflag = True
	count = 0
	
	#Now we go through each token in the token list to match up the instances to their indices in the full list, and check if the scoped names match
	for i in range(len(tokens)):
		if(tokens[i] == reference_name):
		#If the name of the token matches our atom, we're moving along in the list of instances
		#However, it's not necessarily a reference to the same variable, so we have to check the scoped names
			if(scopetokens[i] == scope_name):
			#If those match, then we have a reference
				if(firstflag): #The first reference is the definition, which means it gets a 2
					instances[count][2] = 2
					firstflag = False
				else: #Every other reference just gets a 1
					instances[count][2] = 1
			count += 1
	count = 0
	return (data[0], data[1], data[2], data[3], instances) #Now we return so the editor can highlight

"""This function reads in an expression as a (possibly nested) list and then sets tokens to be that same list but flattened - every sublist has its elements written out in order in the main list (e.g. [1, 2, [3, [4, 5], 6]]] becomes [1, 2, 3, 4, 5, 6])."""
def __tokenize_linear(exp):
	global tokens
	#Since we have a global list of tokens, we just recursively traverse the list and write out each token we encounter
	if(__is_list(exp) or __is_single_list(exp)):
		for e in exp:
			__tokenize_linear(e)
	else:
		tokens.append(exp)

"""This function also flattens a list, as __tokenize_linear(), but prepends each token with a string indicating its scope."""
def __addscopes(exp):
	global scope, count, scopetokens
	if(__is_list(exp) or __is_single_list(exp)):
		if(exp[0] == "define" or exp[0] == "lambda"): #The only thing that changes scope is a new function definition, named or lambda
			scope += "arg" + str(count) + "/" #Add a generic, unique name to the scope indicating a new function - this allows us to distinguis between different functions with the same name, if that happens
			count += 1
			for e in exp: #Go through every element of the current list and add the scopes in there
				__addscopes(e)
			__upscope() #Once we're done with this define or lambda, return to the next step up in the scope
		else:
			for e in exp: #If you're not changing the scope, just traverse the list
				__addscopes(e)
	else:
		scopetokens.append(scope + exp) #Write the scope before the token
		
"""This 'pops off' the latest scope: e.g. if scope is currently arg0/arg1/arg2/arg3, after calling __upscope() scope will be arg0/arg1/arg2."""
def __upscope():
	global scope
	index = scope[:-1].rfind("/") #Simple string search to remove the rightmost slash
	scope = scope[0:max(index+1, 0)] #If there's none, we're back at the top so set the scope to blank
