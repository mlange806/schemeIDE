tokenizer_header = """current = ''
currentIndex = 0
previousIndex = -1
input = ""
fileEnded = False

def tokenize(tokenize_file):
	input = ""
	
def tokenize(tokenize_string):
	input = t_string

def increment():
	if(currentIndex < len(input) - 1):
		current = input[currentIndex]
		currentIndex += 1
	else:
		fileEnded = true
	
"""
#@TODO: Empty and EOF rules
tokenizer_footer = """
def EMPTY():
	return True

def EOF():
	return fileEnded 
"""
tokenizer_file = open("tokenizer.py", "w")

def main(file_name = "grammar.txt"):
	grammar_file = open(file_name, "r")
	write_tab(tokenizer_header)
	grammar = dict()

	#Grammar: {RULE: [[OPTION1], [OPTION2]]}
	for line in grammar_file:
		add_rule(grammar, line)
		
		#Special cases:
		#[{] Special character used for the grammar
		#[\n] Escape character
		#[""] Regular expression
		#["{}"] Regular expression with rules

	generate_first_sets(grammar)
	generate_follow_sets(grammar)
	generate_selection_sets(grammar)
	
	create_tokenizer(tokenizer_file, grammar)
	write_tab(tokenizer_footer)

def create_tokenizer(tokenizer_file, grammar):
	for rule in sorted(iter(grammar)):
	#write the functions in alphabetical order
		print_rule(tokenizer_file, rule, grammar[rule])
		
def print_rule(tokenizer_file, rule, rule_body):
	write_tab("#{" + rule + "}\n");
	write_tab("def " + rule + "():\n")
	for body in rule_body:
		print_body(tokenizer_file, body)
		write_tab("\n\n")
	write_tab(1, "return False\n\n")
		
def print_body(tokenizer_file, body):
	write_tab(1, "#:")
	numTabs = 1
	for element in body:
		write_tab(" " + element.strip())
	write_tab("\n")
		
	for element in body:
		if(element[0] == '{'):
			write_tab(numTabs, "if(" + element[1:-1] + "()):\n")
			numTabs += 1
		elif(element[0] == '['):
			print_special(numTabs, element)
			numTabs += 1
		elif(len(element) == 1):
			write_tab(numTabs, "if(current == '" + (element[0] if(element[0] != '\'' and element[0] != '\\') else "\\" + element[0]) + "'):\n")
			numTabs += 1
		else:
			write_tab(numTabs, "match_string = \"" + escape(element) + "\"\n")
			write_tab(numTabs, "match = True\n")
			write_tab(numTabs, "for i in range(len(match_string)):\n")
			write_tab(numTabs + 1, "if(current != match_string[i]):\n")
			write_tab(numTabs + 2, "match = False\n")
			write_tab(numTabs + 2, "continue\n")
			write_tab(numTabs, "if(match):\n")
			numTabs += 1
	write_tab(numTabs, "return True")


def print_special(numTabs, expression):
	write_tab(numTabs, "#"+expression + "\n")
	expression = expression[1:-1]
	operator = expression[-1]
	if(operator == '*' or operator == '+'):
		write_tab(numTabs, "iterativeMatch = " + ("True" if(operator == '*') else "False") + "\n")
		write_tab(numTabs, "previousIndex = currentIndex\n")
		write_tab(numTabs, "while(" + expression[1:-2] + "()):\n")
		write_tab(numTabs + 1, "previousIndex = currentIndex\n")
		write_tab(numTabs, "currentIndex = previousIndex\n")
		write_tab(numTabs, "if(iterativeMatch):\n")
		numTabs += 1
	elif(expression[0] == '\\'):
		write_tab(numTabs, "if(current == '" + expression + "'):\n")
	else:
		if(len(expression) == 1):
			write_tab(numTabs, "if(current == '" + (expression[0] if(expression[0] != '\'' and expression[0] != '\\') else "\\" + expression[0]) + "'):\n")
			numTabs += 1
		else:
			write_tab(numTabs, "match_string = \"" + escape(expression) + "\"\n")
			write_tab(numTabs, "match = True\n")
			write_tab(numTabs, "for i in range(len(match_string)):\n")
			write_tab(numTabs + 1, "if(current != match_string[i]):\n")
			write_tab(numTabs + 2, "match = False\n")
			write_tab(numTabs + 2, "continue\n")
			write_tab(numTabs, "if(match):\n")
			numTabs += 1
			
def generate_first_sets(grammar):
	return

def generate_follow_sets(grammar):
	return

def generate_selection_sets(grammar):
	return

def escape(string):
	escape_string = string.replace("\\", "\\\\")
	escape_string = escape_string.replace("\"", "\\\"")
	return escape_string

def write_tab(tabs, string=None):
#Python doesn't support overloading or putting the default variable first, so this is a workaround to be able to do either write_tab(string) or write_tab(tabs, string)
#Anyway, the method first writes 'tabs' number of tabs (or none if tabs is not specified), followed by the given string
	if(string == None):
		tokenizer_file.write(tabs)
	else:
		tokenizer_file.write("\t"*tabs + string)

def add_rule(grammar, line):
#The grammar grammar doesn't really lend itself to parsing with regular expressions, so this is a simple scanner that reads a line in the form {RULE}: {BODY1} | {BODY2} | ... and adds those bodies to the rule in the grammar dictionary

	if(line[0] == "#"):
		return
	# '#' denotes comments in the grammar too, so ignore those lines
		
	split = [x.strip() for x in line.split(":")]
	if(len(split) < 2):
		return
	#also ignore rules with no bodies, or vice versa (all bodies are on one line separated by | now)
	 
	rule_name = (split[0])[1:-1] #go from {RULE} to RULE
	grammar[rule_name] = []
	rule_bodies = split[1]
	in_brackets = 0
	in_braces = 0 #counters to detect blocks of text inside []{}
	body_buffer = ""
	rule_body = []
	for char in rule_bodies:
		body_buffer += char
		if(char == '['):
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1):
					rule_body.append(body_buffer[:-1])
				body_buffer = "["
			in_brackets += 1
		elif(char == ']'):
			in_brackets -= 1
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1):
					rule_body.append(body_buffer)
				body_buffer = ""
		elif(char == '{'):
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1):
					rule_body.append(body_buffer[:-1])
				body_buffer = "{"
			in_braces += 1
		elif(char == '}'):
			in_braces -= 1
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1):
					rule_body.append(body_buffer)
				body_buffer = ""
		elif(char == ' '):
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1): #>1 checks for empty because ' ' was added
					rule_body.append(body_buffer[:-1])
				body_buffer = ""
		#space logic: if you're not inside brackets or braces, then the buffer contains a token that needs to be added to this rule body's list
		
		elif(char == '|'):
			if(in_brackets == 0 and in_braces == 0):
				if(len(body_buffer) > 1): #>1 checks for empty because | was added
					rule_body.append(body_buffer[:-1])
				grammar[rule_name].append(rule_body)
				rule_body = []
				body_buffer = ""
		# '|' logic: if you're not inside brackets or braces, then this divides different rule bodies - so write whatever's in the buffer unless it's empty, then append the current body to the rule map and start a new one
		
	if(in_brackets == 0 and in_braces == 0):
		if(len(body_buffer) > 1):
			rule_body.append(body_buffer)
		grammar[rule_name].append(rule_body)
		rule_body = []
		body_buffer = ""
	#end of line logic: same as |, since you've just finished reading the last body
	
main()