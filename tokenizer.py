current = ''
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
	
#{ABBREVIATION}
def ABBREVIATION():
	#: {ABBREV_PREFIX} {DATUM}
	if(ABBREV_PREFIX()):
		if(DATUM()):
			return True

	return False

#{ABBREV_PREFIX}
def ABBREV_PREFIX():
	#: '
	if(current == '\''):
		return True

	#: `
	if(current == '`'):
		return True

	#: ,
	if(current == ','):
		return True

	#: ,@
	match_string = ",@"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{ACCESSOR}
def ACCESSOR():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	return False

#{ALTERNATE}
def ALTERNATE():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	#: {EMPTY}
	if(EMPTY()):
		return True

	return False

#{ASSIGNMENT}
def ASSIGNMENT():
	#: (set! {IDENTIFIER} {EXPRESSION}
	match_string = "(set!"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IDENTIFIER()):
			if(EXPRESSION()):
				return True

	return False

#{ATMOSPHERE}
def ATMOSPHERE():
	#: {WHITESPACE}
	if(WHITESPACE()):
		return True

	#: {COMMENT}
	if(COMMENT()):
		return True

	#: {DIRECTIVE}
	if(DIRECTIVE()):
		return True

	return False

#{BINDING_SPEC}
def BINDING_SPEC():
	#: ( {IDENTIFIER} {EXPRESSION}
	if(current == '('):
		if(IDENTIFIER()):
			if(EXPRESSION()):
				return True

	return False

#{BODY}
def BODY():
	#: [{DEFINITION}*] {SEQUENCE}
	#[{DEFINITION}*]
	iterativeMatch = True
	previousIndex = currentIndex
	while(DEFINITION()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		if(SEQUENCE()):
			return True

	return False

#{BOOLEAN}
def BOOLEAN():
	#: #t
	match_string = "#t"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #f
	match_string = "#f"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #true
	match_string = "#true"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #false
	match_string = "#false"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{BYTE}
def BYTE():
	#: {FIRST_DIGIT} {SECOND_DIGIT} {THIRD_DIGIT}
	if(FIRST_DIGIT()):
		if(SECOND_DIGIT()):
			if(THIRD_DIGIT()):
				return True

	return False

#{BYTEVECTOR}
def BYTEVECTOR():
	#: #u8( [{BYTE}*]
	match_string = "#u8("
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{BYTE}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(BYTE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{CASE_CLAUSE}
def CASE_CLAUSE():
	#: ( [{DATUM}*] ) {SEQUENCE} )
	if(current == '('):
		#[{DATUM}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DATUM()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				if(SEQUENCE()):
					if(current == ')'):
						return True

	#: (( [{DATUM}*] ) => {RECIPIENT}
	match_string = "(("
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{DATUM}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DATUM()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				match_string = "=>"
				match = True
				for i in range(len(match_string)):
					if(current != match_string[i]):
						match = False
						continue
				if(match):
					if(RECIPIENT()):
						return True

	return False

#{CASE_LAMBDA_CLAUSE}
def CASE_LAMBDA_CLAUSE():
	#: ( {FORMALS} {BODY}
	if(current == '('):
		if(FORMALS()):
			if(BODY()):
				return True

	return False

#{CHARACTER}
def CHARACTER():
	#: #\ {ANY_CHARACTER}
	match_string = "#\\"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(ANY_CHARACTER()):
			return True

	#: #\ {CHARACTER_NAME}
	match_string = "#\\"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(CHARACTER_NAME()):
			return True

	#: #\x {HEX_SCALAR_VALUE}
	match_string = "#\\x"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(HEX_SCALAR_VALUE()):
			return True

	return False

#{CHARACTER_NAME}
def CHARACTER_NAME():
	#: alarm
	match_string = "alarm"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: backspace
	match_string = "backspace"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: delete
	match_string = "delete"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: escape
	match_string = "escape"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: newline
	match_string = "newline"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: null
	match_string = "null"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: return
	match_string = "return"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: space
	match_string = "space"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: tab
	match_string = "tab"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{COMMAND}
def COMMAND():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{COMMAND_OR_DEFINITION}
def COMMAND_OR_DEFINITION():
	#: {COMMAND}
	if(COMMAND()):
		return True

	#: {DEFINITION}
	if(DEFINITION()):
		return True

	#: (begin [{COMMAND_OR_DEFINITION}+]
	match_string = "(begin"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COMMAND_OR_DEFINITION}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(COMMAND_OR_DEFINITION()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{COMMENT}
def COMMENT():
	#: ; [{COMMENT_CHARACTER}*] {LINE_ENDING}
	if(current == ';'):
		#[{COMMENT_CHARACTER}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(COMMENT_CHARACTER()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(LINE_ENDING()):
				return True

	#: {NESTED_COMMENT}
	if(NESTED_COMMENT()):
		return True

	#: #; {INTERTOKEN_SPACE} {DATUM}
	match_string = "#;"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(INTERTOKEN_SPACE()):
			if(DATUM()):
				return True

	return False

#{COMMENT_CHARACTER}
def COMMENT_CHARACTER():
	#: {SUBSEQUENT}
	if(SUBSEQUENT()):
		return True

	return False

#{COMMENT_CONT}
def COMMENT_CONT():
	#: {NESTED_COMMENT} {COMMENT_TEXT}
	if(NESTED_COMMENT()):
		if(COMMENT_TEXT()):
			return True

	return False

#{COMMENT_TEXT}
def COMMENT_TEXT():
	#: {COMMENT_CHARACTER}
	if(COMMENT_CHARACTER()):
		return True

	return False

#{COMPLEX_10}
def COMPLEX_10():
	#: {REAL_10}
	if(REAL_10()):
		return True

	#: {REAL_10} @ {REAL_10}
	if(REAL_10()):
		if(current == '@'):
			if(REAL_10()):
				return True

	#: {REAL_10} + {UREAL_10} i
	if(REAL_10()):
		if(current == '+'):
			if(UREAL_10()):
				if(current == 'i'):
					return True

	#: {REAL_10} - {UREAL_10} i
	if(REAL_10()):
		if(current == '-'):
			if(UREAL_10()):
				if(current == 'i'):
					return True

	#: {REAL_10} + i
	if(REAL_10()):
		if(current == '+'):
			if(current == 'i'):
				return True

	#: {REAL_10} - i
	if(REAL_10()):
		if(current == '-'):
			if(current == 'i'):
				return True

	#: {REAL_10} {INFNAN} i
	if(REAL_10()):
		if(INFNAN()):
			if(current == 'i'):
				return True

	#: + {UREAL_10} i
	if(current == '+'):
		if(UREAL_10()):
			if(current == 'i'):
				return True

	#: - {UREAL_10} i
	if(current == '-'):
		if(UREAL_10()):
			if(current == 'i'):
				return True

	#: {INFNAN} i
	if(INFNAN()):
		if(current == 'i'):
			return True

	#: + i
	if(current == '+'):
		if(current == 'i'):
			return True

	#: -
	if(current == '-'):
		return True

	return False

#{COMPLEX_16}
def COMPLEX_16():
	#: {REAL_16}
	if(REAL_16()):
		return True

	#: {REAL_16} @ {REAL_16}
	if(REAL_16()):
		if(current == '@'):
			if(REAL_16()):
				return True

	#: {REAL_16} + {UREAL_16} i
	if(REAL_16()):
		if(current == '+'):
			if(UREAL_16()):
				if(current == 'i'):
					return True

	#: {REAL_16} - {UREAL_16} i
	if(REAL_16()):
		if(current == '-'):
			if(UREAL_16()):
				if(current == 'i'):
					return True

	#: {REAL_16} + i
	if(REAL_16()):
		if(current == '+'):
			if(current == 'i'):
				return True

	#: {REAL_16} - i
	if(REAL_16()):
		if(current == '-'):
			if(current == 'i'):
				return True

	#: {REAL_16} {INFNAN} i
	if(REAL_16()):
		if(INFNAN()):
			if(current == 'i'):
				return True

	#: + {UREAL_16} i
	if(current == '+'):
		if(UREAL_16()):
			if(current == 'i'):
				return True

	#: - {UREAL_16} i
	if(current == '-'):
		if(UREAL_16()):
			if(current == 'i'):
				return True

	#: {INFNAN} i
	if(INFNAN()):
		if(current == 'i'):
			return True

	#: + i
	if(current == '+'):
		if(current == 'i'):
			return True

	#: -
	if(current == '-'):
		return True

	return False

#{COMPLEX_2}
def COMPLEX_2():
	#: {REAL_2}
	if(REAL_2()):
		return True

	#: {REAL_2} @ {REAL_2}
	if(REAL_2()):
		if(current == '@'):
			if(REAL_2()):
				return True

	#: {REAL_2} + {UREAL_2} i
	if(REAL_2()):
		if(current == '+'):
			if(UREAL_2()):
				if(current == 'i'):
					return True

	#: {REAL_2} - {UREAL_2} i
	if(REAL_2()):
		if(current == '-'):
			if(UREAL_2()):
				if(current == 'i'):
					return True

	#: {REAL_2} + i
	if(REAL_2()):
		if(current == '+'):
			if(current == 'i'):
				return True

	#: {REAL_2} - i
	if(REAL_2()):
		if(current == '-'):
			if(current == 'i'):
				return True

	#: {REAL_2} {INFNAN} i
	if(REAL_2()):
		if(INFNAN()):
			if(current == 'i'):
				return True

	#: + {UREAL_2} i
	if(current == '+'):
		if(UREAL_2()):
			if(current == 'i'):
				return True

	#: - {UREAL_2} i
	if(current == '-'):
		if(UREAL_2()):
			if(current == 'i'):
				return True

	#: {INFNAN} i
	if(INFNAN()):
		if(current == 'i'):
			return True

	#: + i
	if(current == '+'):
		if(current == 'i'):
			return True

	#: -
	if(current == '-'):
		return True

	return False

#{COMPLEX_8}
def COMPLEX_8():
	#: {REAL_8}
	if(REAL_8()):
		return True

	#: {REAL_8} @ {REAL_8}
	if(REAL_8()):
		if(current == '@'):
			if(REAL_8()):
				return True

	#: {REAL_8} + {UREAL_8} i
	if(REAL_8()):
		if(current == '+'):
			if(UREAL_8()):
				if(current == 'i'):
					return True

	#: {REAL_8} - {UREAL_8} i
	if(REAL_8()):
		if(current == '-'):
			if(UREAL_8()):
				if(current == 'i'):
					return True

	#: {REAL_8} + i
	if(REAL_8()):
		if(current == '+'):
			if(current == 'i'):
				return True

	#: {REAL_8} - i
	if(REAL_8()):
		if(current == '-'):
			if(current == 'i'):
				return True

	#: {REAL_8} {INFNAN} i
	if(REAL_8()):
		if(INFNAN()):
			if(current == 'i'):
				return True

	#: + {UREAL_8} i
	if(current == '+'):
		if(UREAL_8()):
			if(current == 'i'):
				return True

	#: - {UREAL_8} i
	if(current == '-'):
		if(UREAL_8()):
			if(current == 'i'):
				return True

	#: {INFNAN} i
	if(INFNAN()):
		if(current == 'i'):
			return True

	#: + i
	if(current == '+'):
		if(current == 'i'):
			return True

	#: -
	if(current == '-'):
		return True

	return False

#{COMPOUND_DATUM}
def COMPOUND_DATUM():
	#: {LIST}
	if(LIST()):
		return True

	#: {VECTOR}
	if(VECTOR()):
		return True

	#: {ABBREVIATION}
	if(ABBREVIATION()):
		return True

	return False

#{CONDITIONAL}
def CONDITIONAL():
	#: (if {TEST} {CONSEQUENT} {ALTERNATE}
	match_string = "(if"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(TEST()):
			if(CONSEQUENT()):
				if(ALTERNATE()):
					return True

	return False

#{COND_CLAUSE}
def COND_CLAUSE():
	#: ( {TEST} {SEQUENCE} )
	if(current == '('):
		if(TEST()):
			if(SEQUENCE()):
				if(current == ')'):
					return True

	#: ( {TEST} )
	if(current == '('):
		if(TEST()):
			if(current == ')'):
				return True

	#: ( {TEST} => {RECIPIENT}
	if(current == '('):
		if(TEST()):
			match_string = "=>"
			match = True
			for i in range(len(match_string)):
				if(current != match_string[i]):
					match = False
					continue
			if(match):
				if(RECIPIENT()):
					return True

	return False

#{COND_EXPAND_CLAUSE}
def COND_EXPAND_CLAUSE():
	#: ( {FEATURE_REQUIREMENT} [{LIBRARY_DECLARATION}*]
	if(current == '('):
		if(FEATURE_REQUIREMENT()):
			#[{LIBRARY_DECLARATION}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(LIBRARY_DECLARATION()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{CONSEQUENT}
def CONSEQUENT():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{CONSTRUCTOR}
def CONSTRUCTOR():
	#: ( {IDENTIFIER} [{FIELD_NAME}*]
	if(current == '('):
		if(IDENTIFIER()):
			#[{FIELD_NAME}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(FIELD_NAME()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{DATUM}
def DATUM():
	#: {SIMPLE_DATUM}
	if(SIMPLE_DATUM()):
		return True

	#: {COMPOUND_DATUM}
	if(COMPOUND_DATUM()):
		return True

	#: {LABEL} = {DATUM}
	if(LABEL()):
		if(current == '='):
			if(DATUM()):
				return True

	#: {LABEL}
	if(LABEL()):
		return True

	return False

#{DEFINITION}
def DEFINITION():
	#: (define {IDENTIFIER} {EXPRESSION} )
	match_string = "(define"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IDENTIFIER()):
			if(EXPRESSION()):
				if(current == ')'):
					return True

	#: (define ( {IDENTIFIER} {DEF_FORMALS} ) {BODY} )
	match_string = "(define"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			if(IDENTIFIER()):
				if(DEF_FORMALS()):
					if(current == ')'):
						if(BODY()):
							if(current == ')'):
								return True

	#: {SYNTAX_DEFINITION}
	if(SYNTAX_DEFINITION()):
		return True

	#: (define-values {FORMALS} {BODY} )
	match_string = "(define-values"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(FORMALS()):
			if(BODY()):
				if(current == ')'):
					return True

	#: (define-record-type {IDENTIFIER} {CONSTRUCTOR} {IDENTIFIER} [{FIELD_SPEC}*] )
	match_string = "(define-record-type"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IDENTIFIER()):
			if(CONSTRUCTOR()):
				if(IDENTIFIER()):
					#[{FIELD_SPEC}*]
					iterativeMatch = True
					previousIndex = currentIndex
					while(FIELD_SPEC()):
						previousIndex = currentIndex
					currentIndex = previousIndex
					if(iterativeMatch):
						if(current == ')'):
							return True

	#: (begin [{DEFINITION}*]
	match_string = "(begin"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{DEFINITION}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DEFINITION()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{DEF_FORMALS}
def DEF_FORMALS():
	#: [{IDENTIFIER}*]
	#[{IDENTIFIER}*]
	iterativeMatch = True
	previousIndex = currentIndex
	while(IDENTIFIER()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	#: [{IDENTIFIER}*] . {IDENTIFIER}
	#[{IDENTIFIER}*]
	iterativeMatch = True
	previousIndex = currentIndex
	while(IDENTIFIER()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		if(current == '.'):
			if(IDENTIFIER()):
				return True

	return False

#{DELIMITER}
def DELIMITER():
	#: {WHITESPACE}
	if(WHITESPACE()):
		return True

	#: {VERTICAL_LINE}
	if(VERTICAL_LINE()):
		return True

	#: (
	if(current == '('):
		return True

	#: )
	if(current == ')'):
		return True

	#: "
	if(current == '"'):
		return True

	#:
	return True

	return False

#{DERIVED_EXPRESSION}
def DERIVED_EXPRESSION():
	#: (cond [{COND_CLAUSE}+] )
	match_string = "(cond"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COND_CLAUSE}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(COND_CLAUSE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (cond [{COND_CLAUSE}*] (else {SEQUENCE} ))
	match_string = "(cond"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COND_CLAUSE}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(COND_CLAUSE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			match_string = "(else"
			match = True
			for i in range(len(match_string)):
				if(current != match_string[i]):
					match = False
					continue
			if(match):
				if(SEQUENCE()):
					match_string = "))"
					match = True
					for i in range(len(match_string)):
						if(current != match_string[i]):
							match = False
							continue
					if(match):
						return True

	#: (case {EXPRESSION} [{CASE_CLAUSE}+] )
	match_string = "(case"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(EXPRESSION()):
			#[{CASE_CLAUSE}+]
			iterativeMatch = False
			previousIndex = currentIndex
			while(CASE_CLAUSE()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					return True

	#: (case {EXPRESSION} [{CASE_CLAUSE}*] (else {sequence} ))
	match_string = "(case"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(EXPRESSION()):
			#[{CASE_CLAUSE}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(CASE_CLAUSE()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				match_string = "(else"
				match = True
				for i in range(len(match_string)):
					if(current != match_string[i]):
						match = False
						continue
				if(match):
					if(sequence()):
						match_string = "))"
						match = True
						for i in range(len(match_string)):
							if(current != match_string[i]):
								match = False
								continue
						if(match):
							return True

	#: (case {EXPRESSION} [{CASE_CLAUSE}*] (else => {RECIPIENT} ))
	match_string = "(case"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(EXPRESSION()):
			#[{CASE_CLAUSE}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(CASE_CLAUSE()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				match_string = "(else"
				match = True
				for i in range(len(match_string)):
					if(current != match_string[i]):
						match = False
						continue
				if(match):
					match_string = "=>"
					match = True
					for i in range(len(match_string)):
						if(current != match_string[i]):
							match = False
							continue
					if(match):
						if(RECIPIENT()):
							match_string = "))"
							match = True
							for i in range(len(match_string)):
								if(current != match_string[i]):
									match = False
									continue
							if(match):
								return True

	#: (and [{TEST}*] )
	match_string = "(and"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{TEST}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(TEST()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (or [{TEST}*] )
	match_string = "(or"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{TEST}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(TEST()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (when {TEST} {SEQUENCE} )
	match_string = "(when"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(TEST()):
			if(SEQUENCE()):
				if(current == ')'):
					return True

	#: (unless {TEST} {SEQUENCE} )
	match_string = "(unless"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(TEST()):
			if(SEQUENCE()):
				if(current == ')'):
					return True

	#: (let ( [{BINDING_SPEC}*] ) {BODY} )
	match_string = "(let"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (let {IDENTIFIER} ( [{BINDING_SPEC}*] ) {BODY} )
	match_string = "(let"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IDENTIFIER()):
			if(current == '('):
				#[{BINDING_SPEC}*]
				iterativeMatch = True
				previousIndex = currentIndex
				while(BINDING_SPEC()):
					previousIndex = currentIndex
				currentIndex = previousIndex
				if(iterativeMatch):
					if(current == ')'):
						if(BODY()):
							if(current == ')'):
								return True

	#: (let* ( [{BINDING_SPEC}*] ) {BODY} )
	match_string = "(let*"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (letrec ( [{BINDING_SPEC}*] ) {BODY} )
	match_string = "(letrec"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (letrec* ( [{BINDING_SPEC}*] ) {BODY} )
	match_string = "(letrec*"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (let-values ( [{MV_BINDING_SPEC}*] ) {BODY} )
	match_string = "(let-values"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{MV_BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(MV_BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (let*-values ( [{MV_BINDING_SPEC}*] ) {BODY} )
	match_string = "(let*-values"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{MV_BINDING_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(MV_BINDING_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (begin {SEQUENCE} )
	match_string = "(begin"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(SEQUENCE()):
			if(current == ')'):
				return True

	#: (do ( [{ITERATION_SPEC}*] ) ( {TESTI_HDO_RESULT} ) [{COMMAND}*] )
	match_string = "(do"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{ITERATION_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(ITERATION_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(current == '('):
						if(TESTI_HDO_RESULT()):
							if(current == ')'):
								#[{COMMAND}*]
								iterativeMatch = True
								previousIndex = currentIndex
								while(COMMAND()):
									previousIndex = currentIndex
								currentIndex = previousIndex
								if(iterativeMatch):
									if(current == ')'):
										return True

	#: (delay {EXPRESSION} )
	match_string = "(delay"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(EXPRESSION()):
			if(current == ')'):
				return True

	#: (delay-force {EXPRESSION} )
	match_string = "(delay-force"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(EXPRESSION()):
			if(current == ')'):
				return True

	#: (parameterize [{DOUBLE_EXPRESSION}*] ) {BODY} )
	match_string = "(parameterize"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{DOUBLE_EXPRESSION}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DOUBLE_EXPRESSION()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				if(BODY()):
					if(current == ')'):
						return True

	#: (guard ( {IDENTIFIER} [{COND_CLAUSE}*] ) {BODY} )
	match_string = "(guard"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			if(IDENTIFIER()):
				#[{COND_CLAUSE}*]
				iterativeMatch = True
				previousIndex = currentIndex
				while(COND_CLAUSE()):
					previousIndex = currentIndex
				currentIndex = previousIndex
				if(iterativeMatch):
					if(current == ')'):
						if(BODY()):
							if(current == ')'):
								return True

	#: {QUASIQUOTATION}
	if(QUASIQUOTATION()):
		return True

	#: (case-lambda [{CASE_LAMBDA_CLAUSE}*]
	match_string = "(case-lambda"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{CASE_LAMBDA_CLAUSE}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(CASE_LAMBDA_CLAUSE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{DIGIT}
def DIGIT():
	#: 0
	if(current == '0'):
		return True

	#: 1
	if(current == '1'):
		return True

	#: 2
	if(current == '2'):
		return True

	#: 3
	if(current == '3'):
		return True

	#: 4
	if(current == '4'):
		return True

	#: 5
	if(current == '5'):
		return True

	#: 6
	if(current == '6'):
		return True

	#: 7
	if(current == '7'):
		return True

	#: 8
	if(current == '8'):
		return True

	#:
	return True

	return False

#{DIGIT_10}
def DIGIT_10():
	#: {DIGIT}
	if(DIGIT()):
		return True

	return False

#{DIGIT_16}
def DIGIT_16():
	#: {DIGIT_10}
	if(DIGIT_10()):
		return True

	#: a
	if(current == 'a'):
		return True

	#: b
	if(current == 'b'):
		return True

	#: c
	if(current == 'c'):
		return True

	#: d
	if(current == 'd'):
		return True

	#: e
	if(current == 'e'):
		return True

	#:
	return True

	return False

#{DIGIT_2}
def DIGIT_2():
	#: 0
	if(current == '0'):
		return True

	#:
	return True

	return False

#{DIGIT_8}
def DIGIT_8():
	#: 0
	if(current == '0'):
		return True

	#: 1
	if(current == '1'):
		return True

	#: 2
	if(current == '2'):
		return True

	#: 3
	if(current == '3'):
		return True

	#: 4
	if(current == '4'):
		return True

	#: 5
	if(current == '5'):
		return True

	#: 6
	if(current == '6'):
		return True

	#:
	return True

	return False

#{DIRECTIVE}
def DIRECTIVE():
	#: #!fold-case
	match_string = "#!fold-case"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #!no-fold-case
	match_string = "#!no-fold-case"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{DOT_SUBSEQUENT}
def DOT_SUBSEQUENT():
	#: {SIGN_SUBSEQUENT}
	if(SIGN_SUBSEQUENT()):
		return True

	#:
	return True

	return False

#{DOUBLE_IDENTIFIER}
def DOUBLE_IDENTIFIER():
	#: ( {IDENTIFIER} {IDENTIFIER}
	if(current == '('):
		if(IDENTIFIER()):
			if(IDENTIFIER()):
				return True

	return False

#{DO_RESULT}
def DO_RESULT():
	#: {SEQUENCE}
	if(SEQUENCE()):
		return True

	#: {EMPTY}
	if(EMPTY()):
		return True

	return False

#{EXACTNESS}
def EXACTNESS():
	#: {EMPTY}
	if(EMPTY()):
		return True

	#: #i
	match_string = "#i"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #e
	match_string = "#e"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{EXPLICIT_SIGN}
def EXPLICIT_SIGN():
	#: +
	if(current == '+'):
		return True

	#:
	return True

	return False

#{EXPONENT_MARKER}
def EXPONENT_MARKER():
	#:
	return True

	return False

#{EXPORT_SPEC}
def EXPORT_SPEC():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: (rename {IDENTIFIER} {IDENTIFIER}
	match_string = "(rename"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IDENTIFIER()):
			if(IDENTIFIER()):
				return True

	return False

#{EXPRESSION}
def EXPRESSION():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: {LITERAL}
	if(LITERAL()):
		return True

	#: {PROCEDURE_CALL}
	if(PROCEDURE_CALL()):
		return True

	#: {LAMBDA_EXPRESSION}
	if(LAMBDA_EXPRESSION()):
		return True

	#: {CONDITIONAL}
	if(CONDITIONAL()):
		return True

	#: {ASSIGNMENT}
	if(ASSIGNMENT()):
		return True

	#: {DERIVED_EXPRESSION}
	if(DERIVED_EXPRESSION()):
		return True

	#: {MACRO_USE}
	if(MACRO_USE()):
		return True

	#: {MACRO_BLOCK}
	if(MACRO_BLOCK()):
		return True

	#: {INCLUDER}
	if(INCLUDER()):
		return True

	return False

#{FEATURE_REQUIREMENT}
def FEATURE_REQUIREMENT():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: {LIBRARY_NAME}
	if(LIBRARY_NAME()):
		return True

	#: (and [{FEATURE_REQUIREMENT}*] )
	match_string = "(and"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{FEATURE_REQUIREMENT}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(FEATURE_REQUIREMENT()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (or [{FEATURE_REQUIREMENT}*] )
	match_string = "(or"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{FEATURE_REQUIREMENT}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(FEATURE_REQUIREMENT()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (not {FEATURE_REQUIREMENT}
	match_string = "(not"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(FEATURE_REQUIREMENT()):
			return True

	return False

#{FIELD_NAME}
def FIELD_NAME():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	return False

#{FIELD_SPEC}
def FIELD_SPEC():
	#: ( {FIELD_NAME} {ACCESSOR} )
	if(current == '('):
		if(FIELD_NAME()):
			if(ACCESSOR()):
				if(current == ')'):
					return True

	#: ( {FIELD_NAME} {ACCESSOR} {MUTATOR}
	if(current == '('):
		if(FIELD_NAME()):
			if(ACCESSOR()):
				if(MUTATOR()):
					return True

	return False

#{FIRST_DIGIT}
def FIRST_DIGIT():
	#: 0
	if(current == '0'):
		return True

	#: 1
	if(current == '1'):
		return True

	#:
	return True

	return False

#{FORMALS}
def FORMALS():
	#: ( [{IDENTIFIER}*] )
	if(current == '('):
		#[{IDENTIFIER}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(IDENTIFIER()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: ( [{IDENTIFIER}+] . {IDENTIFIER}
	if(current == '('):
		#[{IDENTIFIER}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(IDENTIFIER()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == '.'):
				if(IDENTIFIER()):
					return True

	return False

#{HEX_DIGIT}
def HEX_DIGIT():
	#: {DIGIT}
	if(DIGIT()):
		return True

	#: a
	if(current == 'a'):
		return True

	#: b
	if(current == 'b'):
		return True

	#: c
	if(current == 'c'):
		return True

	#: d
	if(current == 'd'):
		return True

	#: e
	if(current == 'e'):
		return True

	#: f
	if(current == 'f'):
		return True

	#: A
	if(current == 'A'):
		return True

	#: B
	if(current == 'B'):
		return True

	#: C
	if(current == 'C'):
		return True

	#: D
	if(current == 'D'):
		return True

	#: E
	if(current == 'E'):
		return True

	#:
	return True

	return False

#{HEX_SCALAR_VALUE}
def HEX_SCALAR_VALUE():
	#: [{HEX_DIGIT}+]
	#[{HEX_DIGIT}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(HEX_DIGIT()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{IDENTIFIER}
def IDENTIFIER():
	#: {INITIAL} [{SUBSEQUENT}*]
	if(INITIAL()):
		#[{SUBSEQUENT}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(SUBSEQUENT()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	#: {VERTICAL_LINE} [{SYMBOL_ELEMENT}*] {VERTICAL_LINE}
	if(VERTICAL_LINE()):
		#[{SYMBOL_ELEMENT}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(SYMBOL_ELEMENT()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(VERTICAL_LINE()):
				return True

	#: {PECULIAR_IDENTIFIER}
	if(PECULIAR_IDENTIFIER()):
		return True

	return False

#{IMPORT_DECLARATION}
def IMPORT_DECLARATION():
	#: (import [{IMPORT_SET}+]
	match_string = "(import"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{IMPORT_SET}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(IMPORT_SET()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{IMPORT_SET}
def IMPORT_SET():
	#: {LIBRARY_NAME}
	if(LIBRARY_NAME()):
		return True

	#: (only {IMPORT_SET} [{IDENTIFIER}+] )
	match_string = "(only"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IMPORT_SET()):
			#[{IDENTIFIER}+]
			iterativeMatch = False
			previousIndex = currentIndex
			while(IDENTIFIER()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					return True

	#: (except {IMPORT_SET} [{IDENTIFIER}+] )
	match_string = "(except"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IMPORT_SET()):
			#[{IDENTIFIER}+]
			iterativeMatch = False
			previousIndex = currentIndex
			while(IDENTIFIER()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					return True

	#: (prefix {IMPORT_SET} {IDENTIFIER} )
	match_string = "(prefix"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IMPORT_SET()):
			if(IDENTIFIER()):
				if(current == ')'):
					return True

	#: (rename {IMPORT_SET} [{DOUBLE_IDENTIFIER}+]
	match_string = "(rename"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(IMPORT_SET()):
			#[{DOUBLE_IDENTIFIER}+]
			iterativeMatch = False
			previousIndex = currentIndex
			while(DOUBLE_IDENTIFIER()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{INCLUDER}
def INCLUDER():
	#:
	return True

	#: (include [{STRING}+] )
	match_string = "(include"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{STRING}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(STRING()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (include-ci [{STRING}+]
	match_string = "(include-ci"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{STRING}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(STRING()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{INFNAN}
def INFNAN():
	#: +inf.0
	match_string = "+inf.0"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: -inf.0
	match_string = "-inf.0"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: +nan.0
	match_string = "+nan.0"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: -nan.0
	match_string = "-nan.0"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{INIT}
def INIT():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{INITIAL}
def INITIAL():
	#: {LETTER}
	if(LETTER()):
		return True

	#: {SPECIAL_INITIAL}
	if(SPECIAL_INITIAL()):
		return True

	return False

#{INLINE_HEX_ESCAPE}
def INLINE_HEX_ESCAPE():
	#: \x {HEX_SCALAR_VALUE}
	match_string = "\\x"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(HEX_SCALAR_VALUE()):
			return True

	return False

#{INTERTOKEN_SPACE}
def INTERTOKEN_SPACE():
	#: [{ATMOSPHERE}*]
	#[{ATMOSPHERE}*]
	iterativeMatch = True
	previousIndex = currentIndex
	while(ATMOSPHERE()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{INTRALINE_WHITESPACE}
def INTRALINE_WHITESPACE():
	#: [\ ]
	#[\ ]
	if(current == '\ '):
		return True

	#: [\t]
	#[\t]
	if(current == '\t'):
		return True

	return False

#{ITERATION_SPEC}
def ITERATION_SPEC():
	return False

#{KEYWORD}
def KEYWORD():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	return False

#{LABEL}
def LABEL():
	#: # {UINTEGER_10}
	if(current == '#'):
		if(UINTEGER_10()):
			return True

	return False

#{LAMBDA_EXPRESSION}
def LAMBDA_EXPRESSION():
	#: (lambda {FORMALS} {BODY}
	match_string = "(lambda"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(FORMALS()):
			if(BODY()):
				return True

	return False

#{LETTER}
def LETTER():
	#: a
	if(current == 'a'):
		return True

	#: b
	if(current == 'b'):
		return True

	#: c
	if(current == 'c'):
		return True

	#: d
	if(current == 'd'):
		return True

	#: e
	if(current == 'e'):
		return True

	#: f
	if(current == 'f'):
		return True

	#: g
	if(current == 'g'):
		return True

	#: h
	if(current == 'h'):
		return True

	#: i
	if(current == 'i'):
		return True

	#: j
	if(current == 'j'):
		return True

	#: k
	if(current == 'k'):
		return True

	#: l
	if(current == 'l'):
		return True

	#: m
	if(current == 'm'):
		return True

	#: n
	if(current == 'n'):
		return True

	#: o
	if(current == 'o'):
		return True

	#: p
	if(current == 'p'):
		return True

	#: q
	if(current == 'q'):
		return True

	#: r
	if(current == 'r'):
		return True

	#: s
	if(current == 's'):
		return True

	#: t
	if(current == 't'):
		return True

	#: u
	if(current == 'u'):
		return True

	#: v
	if(current == 'v'):
		return True

	#: w
	if(current == 'w'):
		return True

	#: x
	if(current == 'x'):
		return True

	#: y
	if(current == 'y'):
		return True

	#: z
	if(current == 'z'):
		return True

	#: A
	if(current == 'A'):
		return True

	#: B
	if(current == 'B'):
		return True

	#: C
	if(current == 'C'):
		return True

	#: D
	if(current == 'D'):
		return True

	#: E
	if(current == 'E'):
		return True

	#: F
	if(current == 'F'):
		return True

	#: G
	if(current == 'G'):
		return True

	#: H
	if(current == 'H'):
		return True

	#: I
	if(current == 'I'):
		return True

	#: J
	if(current == 'J'):
		return True

	#: K
	if(current == 'K'):
		return True

	#: L
	if(current == 'L'):
		return True

	#: M
	if(current == 'M'):
		return True

	#: N
	if(current == 'N'):
		return True

	#: O
	if(current == 'O'):
		return True

	#: P
	if(current == 'P'):
		return True

	#: Q
	if(current == 'Q'):
		return True

	#: R
	if(current == 'R'):
		return True

	#: S
	if(current == 'S'):
		return True

	#: T
	if(current == 'T'):
		return True

	#: U
	if(current == 'U'):
		return True

	#: V
	if(current == 'V'):
		return True

	#: W
	if(current == 'W'):
		return True

	#: X
	if(current == 'X'):
		return True

	#: Y
	if(current == 'Y'):
		return True

	#:
	return True

	return False

#{LIBRARY}
def LIBRARY():
	#: (define-library {LIBRARY_NAME} [{LIBRARY_DECLARATION}*]
	match_string = "(define-library"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(LIBRARY_NAME()):
			#[{LIBRARY_DECLARATION}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(LIBRARY_DECLARATION()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{LIBRARY_DECLARATION}
def LIBRARY_DECLARATION():
	#: (export [{EXPORT_SPEC}*] )
	match_string = "(export"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{EXPORT_SPEC}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(EXPORT_SPEC()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: {IMPORT_DECLARATION}
	if(IMPORT_DECLARATION()):
		return True

	#: (begin [{COMMAND_OR_DEFINITION}*] )
	match_string = "(begin"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COMMAND_OR_DEFINITION}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(COMMAND_OR_DEFINITION()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: {INCLUDER}
	if(INCLUDER()):
		return True

	#: (include-library-declarations [{STRING}+] )
	match_string = "(include-library-declarations"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{STRING}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(STRING()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (cond-expand [{COND_EXPAND_CLAUSE}+] )
	match_string = "(cond-expand"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COND_EXPAND_CLAUSE}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(COND_EXPAND_CLAUSE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: (cond-expand [{COND_EXPAND_CLAUSE}+] (else [{LIBRARY_DECLARATION}*] ))
	match_string = "(cond-expand"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{COND_EXPAND_CLAUSE}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(COND_EXPAND_CLAUSE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			match_string = "(else"
			match = True
			for i in range(len(match_string)):
				if(current != match_string[i]):
					match = False
					continue
			if(match):
				#[{LIBRARY_DECLARATION}*]
				iterativeMatch = True
				previousIndex = currentIndex
				while(LIBRARY_DECLARATION()):
					previousIndex = currentIndex
				currentIndex = previousIndex
				if(iterativeMatch):
					match_string = "))"
					match = True
					for i in range(len(match_string)):
						if(current != match_string[i]):
							match = False
							continue
					if(match):
						return True

	return False

#{LIBRARY_NAME}
def LIBRARY_NAME():
	#: ( [{LIBRARY_NAME_PART}+]
	if(current == '('):
		#[{LIBRARY_NAME_PART}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(LIBRARY_NAME_PART()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{LIBRARY_NAME_PART}
def LIBRARY_NAME_PART():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: {UINTEGER_10}
	if(UINTEGER_10()):
		return True

	return False

#{LINE_ENDING}
def LINE_ENDING():
	#: [\n]
	#[\n]
	if(current == '\n'):
		return True

	#: [\r] [\n]
	#[\r]
	if(current == '\r'):
		#[\n]
		if(current == '\n'):
			return True

	#: [\r]
	#[\r]
	if(current == '\r'):
		return True

	return False

#{LIST}
def LIST():
	#: ( [{DATUM}*] )
	if(current == '('):
		#[{DATUM}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DATUM()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == ')'):
				return True

	#: ( [{DATUM}+] . {DATUM}
	if(current == '('):
		#[{DATUM}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(DATUM()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(current == '.'):
				if(DATUM()):
					return True

	return False

#{LITERAL}
def LITERAL():
	#: {QUOTATION}
	if(QUOTATION()):
		return True

	#: {SELF_EVALUATING}
	if(SELF_EVALUATING()):
		return True

	return False

#{MACRO_BLOCK}
def MACRO_BLOCK():
	#: (let-syntax ( [{SYNTAX_SPEC}*] ) {BODY} )
	match_string = "(let-syntax"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{SYNTAX_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(SYNTAX_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						if(current == ')'):
							return True

	#: (letrec-syntax ( [{SYNTAX_SPEC}*] ) {BODY}
	match_string = "(letrec-syntax"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(current == '('):
			#[{SYNTAX_SPEC}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(SYNTAX_SPEC()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				if(current == ')'):
					if(BODY()):
						return True

	return False

#{MACRO_USE}
def MACRO_USE():
	#: ( {KEYWORD} [{DATUM}*]
	if(current == '('):
		if(KEYWORD()):
			#[{DATUM}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(DATUM()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{MNEMONIC_ESCAPE}
def MNEMONIC_ESCAPE():
	#: \a
	match_string = "\\a"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \b
	match_string = "\\b"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \t
	match_string = "\\t"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \n
	match_string = "\\n"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \r
	match_string = "\\r"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{MUTATOR}
def MUTATOR():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	return False

#{MV_BINDING_SPEC}
def MV_BINDING_SPEC():
	#: ( {FORMALS} {EXPRESSION}
	if(current == '('):
		if(FORMALS()):
			if(EXPRESSION()):
				return True

	return False

#{NESTED_COMMENT}
def NESTED_COMMENT():
	#: [#|] {COMMENT_TEXT} [{COMMENT_CONT}*] [|#]
	#[#|]
	match_string = "#|"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(COMMENT_TEXT()):
			#[{COMMENT_CONT}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(COMMENT_CONT()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				#[|#]
				match_string = "|#"
				match = True
				for i in range(len(match_string)):
					if(current != match_string[i]):
						match = False
						continue
				if(match):
					return True

	return False

#{NUMBER}
def NUMBER():
	#: {NUM_2}
	if(NUM_2()):
		return True

	#: {NUM_8}
	if(NUM_8()):
		return True

	#: {NUM_10}
	if(NUM_10()):
		return True

	#: {NUM_16}
	if(NUM_16()):
		return True

	return False

#{NUM_10}
def NUM_10():
	return False

#{NUM_16}
def NUM_16():
	return False

#{NUM_2}
def NUM_2():
	return False

#{NUM_8}
def NUM_8():
	return False

#{OPERAND}
def OPERAND():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{OPERATOR}
def OPERATOR():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{PECULIAR_IDENTIFIER}
def PECULIAR_IDENTIFIER():
	#: {EXPLICIT_SIGN}
	if(EXPLICIT_SIGN()):
		return True

	#: {EXPLICIT_SIGN} {SIGN_SUBSEQUENT} [{SUBSEQUENT}*]
	if(EXPLICIT_SIGN()):
		if(SIGN_SUBSEQUENT()):
			#[{SUBSEQUENT}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(SUBSEQUENT()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	#: {EXPLICIT_SIGN} . {DOT_SUBSEQUENT} [{SUBSEQUENT}*]
	if(EXPLICIT_SIGN()):
		if(current == '.'):
			if(DOT_SUBSEQUENT()):
				#[{SUBSEQUENT}*]
				iterativeMatch = True
				previousIndex = currentIndex
				while(SUBSEQUENT()):
					previousIndex = currentIndex
				currentIndex = previousIndex
				if(iterativeMatch):
					return True

	#: . {DOT_SUBSEQUENT} [{SUBSEQUENT}*]
	if(current == '.'):
		if(DOT_SUBSEQUENT()):
			#[{SUBSEQUENT}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(SUBSEQUENT()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{PREFIX_10}
def PREFIX_10():
	#: {RADIX_10} {EXACTNESS}
	if(RADIX_10()):
		if(EXACTNESS()):
			return True

	#: {EXACTNESS} {RADIX_10}
	if(EXACTNESS()):
		if(RADIX_10()):
			return True

	return False

#{PREFIX_16}
def PREFIX_16():
	#: {RADIX_16} {EXACTNESS}
	if(RADIX_16()):
		if(EXACTNESS()):
			return True

	#: {EXACTNESS} {RADIX_16}
	if(EXACTNESS()):
		if(RADIX_16()):
			return True

	return False

#{PREFIX_2}
def PREFIX_2():
	#: {RADIX_2} {EXACTNESS}
	if(RADIX_2()):
		if(EXACTNESS()):
			return True

	#: {EXACTNESS} {RADIX_2}
	if(EXACTNESS()):
		if(RADIX_2()):
			return True

	return False

#{PREFIX_8}
def PREFIX_8():
	#: {RADIX_8} {EXACTNESS}
	if(RADIX_8()):
		if(EXACTNESS()):
			return True

	#: {EXACTNESS} {RADIX_8}
	if(EXACTNESS()):
		if(RADIX_8()):
			return True

	return False

#{PROCEDURE_CALL}
def PROCEDURE_CALL():
	#: ( {OPERATOR} [{OPERAND}*]
	if(current == '('):
		if(OPERATOR()):
			#[{OPERAND}*]
			iterativeMatch = True
			previousIndex = currentIndex
			while(OPERAND()):
				previousIndex = currentIndex
			currentIndex = previousIndex
			if(iterativeMatch):
				return True

	return False

#{PROGRAM}
def PROGRAM():
	#: [{IMPORT_DECLARATION}+] [{COMMAND_OR_DEFINITION}+] {EOF}
	#[{IMPORT_DECLARATION}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(IMPORT_DECLARATION()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		#[{COMMAND_OR_DEFINITION}+]
		iterativeMatch = False
		previousIndex = currentIndex
		while(COMMAND_OR_DEFINITION()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(EOF()):
				return True

	return False

#{QUOTATION}
def QUOTATION():
	#: ' {DATUM}
	if(current == '\''):
		if(DATUM()):
			return True

	#: (quote {DATUM}
	match_string = "(quote"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(DATUM()):
			return True

	return False

#{RADIX_10}
def RADIX_10():
	#: {EMPTY}
	if(EMPTY()):
		return True

	#: #d
	match_string = "#d"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{RADIX_16}
def RADIX_16():
	#: #x
	match_string = "#x"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{RADIX_2}
def RADIX_2():
	#: #b
	match_string = "#b"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{RADIX_8}
def RADIX_8():
	#: #o
	match_string = "#o"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{REAL_10}
def REAL_10():
	#: {SIGN} {UREAL_10}
	if(SIGN()):
		if(UREAL_10()):
			return True

	#: {INFNAN}
	if(INFNAN()):
		return True

	return False

#{REAL_16}
def REAL_16():
	#: {SIGN} {UREAL_16}
	if(SIGN()):
		if(UREAL_16()):
			return True

	#: {INFNAN}
	if(INFNAN()):
		return True

	return False

#{REAL_2}
def REAL_2():
	#: {SIGN} {UREAL_2}
	if(SIGN()):
		if(UREAL_2()):
			return True

	#: {INFNAN}
	if(INFNAN()):
		return True

	return False

#{REAL_8}
def REAL_8():
	#: {SIGN} {UREAL_8}
	if(SIGN()):
		if(UREAL_8()):
			return True

	#: {INFNAN}
	if(INFNAN()):
		return True

	return False

#{RECIPIENT}
def RECIPIENT():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{SECOND_DIGIT}
def SECOND_DIGIT():
	#: {DIGIT}
	if(DIGIT()):
		return True

	#: {EMPTY}
	if(EMPTY()):
		return True

	return False

#{SELF_EVALUATING}
def SELF_EVALUATING():
	#: {BOOLEAN}
	if(BOOLEAN()):
		return True

	#: {NUMBER}
	if(NUMBER()):
		return True

	#: {VECTOR}
	if(VECTOR()):
		return True

	#: {CHARACTER}
	if(CHARACTER()):
		return True

	#: {STRING}
	if(STRING()):
		return True

	#: {BYTEVECTOR}
	if(BYTEVECTOR()):
		return True

	return False

#{SEQUENCE}
def SEQUENCE():
	#: [{COMMAND}*] {EXPRESSION}
	#[{COMMAND}*]
	iterativeMatch = True
	previousIndex = currentIndex
	while(COMMAND()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		if(EXPRESSION()):
			return True

	return False

#{SIGN}
def SIGN():
	#: {EMPTY}
	if(EMPTY()):
		return True

	#: +
	if(current == '+'):
		return True

	#:
	return True

	return False

#{SIGN_SUBSEQUENT}
def SIGN_SUBSEQUENT():
	#: {INITIAL}
	if(INITIAL()):
		return True

	#: {EXPLICIT_SIGN}
	if(EXPLICIT_SIGN()):
		return True

	#:
	return True

	return False

#{SIMPLE_DATUM}
def SIMPLE_DATUM():
	#: {BOOLEAN}
	if(BOOLEAN()):
		return True

	#: {NUMBER}
	if(NUMBER()):
		return True

	#: {CHARACTER}
	if(CHARACTER()):
		return True

	#: {STRING}
	if(STRING()):
		return True

	#: {SYMBOL}
	if(SYMBOL()):
		return True

	#: {BYTEVECTOR}
	if(BYTEVECTOR()):
		return True

	return False

#{SPACE_OR_TAB}
def SPACE_OR_TAB():
	#: \n
	match_string = "\\n"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \t
	match_string = "\\t"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	return False

#{SPECIAL_INITIAL}
def SPECIAL_INITIAL():
	#: !
	if(current == '!'):
		return True

	#: $
	if(current == '$'):
		return True

	#: %
	if(current == '%'):
		return True

	#: &
	if(current == '&'):
		return True

	#: *
	if(current == '*'):
		return True

	#: /
	if(current == '/'):
		return True

	#:
	return True

	return False

#{SPECIAL_SUBSEQUENT}
def SPECIAL_SUBSEQUENT():
	#: {EXPLICIT_SIGN}
	if(EXPLICIT_SIGN()):
		return True

	#: .
	if(current == '.'):
		return True

	#:
	return True

	return False

#{STEP}
def STEP():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{STRING}
def STRING():
	#: " [{STRING_ELEMENT}*]
	if(current == '"'):
		#[{STRING_ELEMENT}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(STRING_ELEMENT()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{STRING_ELEMENT}
def STRING_ELEMENT():
	#: {SUBSEQUENT}
	if(SUBSEQUENT()):
		return True

	#: {MNEMONIC_ESCAPE}
	if(MNEMONIC_ESCAPE()):
		return True

	#: \"
	match_string = "\\\""
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \\
	match_string = "\\\\"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: \ [{INTRALINE_WHITESPACE}*] {LINE_ENDING} [{INTRALINE_WHITESPACE}*]
	if(current == '\\'):
		#[{INTRALINE_WHITESPACE}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(INTRALINE_WHITESPACE()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			if(LINE_ENDING()):
				#[{INTRALINE_WHITESPACE}*]
				iterativeMatch = True
				previousIndex = currentIndex
				while(INTRALINE_WHITESPACE()):
					previousIndex = currentIndex
				currentIndex = previousIndex
				if(iterativeMatch):
					return True

	#: {INLINE_HEX_ESCAPE}
	if(INLINE_HEX_ESCAPE()):
		return True

	return False

#{SUBSEQUENT}
def SUBSEQUENT():
	#: {INITIAL}
	if(INITIAL()):
		return True

	#: {DIGIT}
	if(DIGIT()):
		return True

	#: {SPECIAL_SUBSEQUENT}
	if(SPECIAL_SUBSEQUENT()):
		return True

	return False

#{SUFFIX}
def SUFFIX():
	#: {EMPTY}
	if(EMPTY()):
		return True

	return False

#{SYMBOL}
def SYMBOL():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	return False

#{SYMBOL_ELEMENT}
def SYMBOL_ELEMENT():
	#: {SUBSEQUENT}
	if(SUBSEQUENT()):
		return True

	#: {INLINE_HEX_ESCAPE}
	if(INLINE_HEX_ESCAPE()):
		return True

	#: {MNEMONIC_ESCAPE}
	if(MNEMONIC_ESCAPE()):
		return True

	#: \ [|]
	if(current == '\\'):
		#[|]
		if(current == '|'):
			return True

	return False

#{SYNTAX_DEFINITION}
def SYNTAX_DEFINITION():
	#: (define-syntax {KEYWORD} {TRANSFORMER_SPEC}
	match_string = "(define-syntax"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		if(KEYWORD()):
			if(TRANSFORMER_SPEC()):
				return True

	return False

#{SYNTAX_SPEC}
def SYNTAX_SPEC():
	#: ( {KEYWORD} {TRANSFORMER_SPEC}
	if(current == '('):
		if(KEYWORD()):
			if(TRANSFORMER_SPEC()):
				return True

	return False

#{TEST}
def TEST():
	#: {EXPRESSION}
	if(EXPRESSION()):
		return True

	return False

#{THIRD_DIGIT}
def THIRD_DIGIT():
	#: {DIGIT}
	if(DIGIT()):
		return True

	#: {EMPTY}
	if(EMPTY()):
		return True

	return False

#{TOKEN}
def TOKEN():
	#: {IDENTIFIER}
	if(IDENTIFIER()):
		return True

	#: {BOOLEAN}
	if(BOOLEAN()):
		return True

	#: {NUMBER}
	if(NUMBER()):
		return True

	#: {CHARACTER}
	if(CHARACTER()):
		return True

	#: {STRING}
	if(STRING()):
		return True

	#: (
	if(current == '('):
		return True

	#: )
	if(current == ')'):
		return True

	#: #\(
	match_string = "#\\("
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: #u8(
	match_string = "#u8("
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#: '
	if(current == '\''):
		return True

	#: `
	if(current == '`'):
		return True

	#: ,
	if(current == ','):
		return True

	#: ,@
	match_string = ",@"
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		return True

	#:
	return True

	return False

#{UINTEGER_10}
def UINTEGER_10():
	#: [{DIGIT_10}+]
	#[{DIGIT_10}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(DIGIT_10()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{UINTEGER_16}
def UINTEGER_16():
	#: [{DIGIT_16}+]
	#[{DIGIT_16}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(DIGIT_16()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{UINTEGER_2}
def UINTEGER_2():
	#: [{DIGIT_2}+]
	#[{DIGIT_2}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(DIGIT_2()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{UINTEGER_8}
def UINTEGER_8():
	#: [{DIGIT_8}+]
	#[{DIGIT_8}+]
	iterativeMatch = False
	previousIndex = currentIndex
	while(DIGIT_8()):
		previousIndex = currentIndex
	currentIndex = previousIndex
	if(iterativeMatch):
		return True

	return False

#{UREAL_10}
def UREAL_10():
	#: {UINTEGER_10}
	if(UINTEGER_10()):
		return True

	#: {UINTEGER_10} / {UINTEGER_10}
	if(UINTEGER_10()):
		if(current == '/'):
			if(UINTEGER_10()):
				return True

	#: {DECIMAL_10}
	if(DECIMAL_10()):
		return True

	return False

#{UREAL_16}
def UREAL_16():
	#: {UINTEGER_16}
	if(UINTEGER_16()):
		return True

	#: {UINTEGER_16} / {UINTEGER_16}
	if(UINTEGER_16()):
		if(current == '/'):
			if(UINTEGER_16()):
				return True

	return False

#{UREAL_2}
def UREAL_2():
	#: {UINTEGER_2}
	if(UINTEGER_2()):
		return True

	#: {UINTEGER_2} / {UINTEGER_2}
	if(UINTEGER_2()):
		if(current == '/'):
			if(UINTEGER_2()):
				return True

	return False

#{UREAL_8}
def UREAL_8():
	#: {UINTEGER_8}
	if(UINTEGER_8()):
		return True

	#: {UINTEGER_8} / {UINTEGER_8}
	if(UINTEGER_8()):
		if(current == '/'):
			if(UINTEGER_8()):
				return True

	return False

#{VECTOR}
def VECTOR():
	#: #( [{DATUM}*]
	match_string = "#("
	match = True
	for i in range(len(match_string)):
		if(current != match_string[i]):
			match = False
			continue
	if(match):
		#[{DATUM}*]
		iterativeMatch = True
		previousIndex = currentIndex
		while(DATUM()):
			previousIndex = currentIndex
		currentIndex = previousIndex
		if(iterativeMatch):
			return True

	return False

#{VERTICAL_LINE}
def VERTICAL_LINE():
	#: [|]
	#[|]
	if(current == '|'):
		return True

	return False

#{WHITESPACE}
def WHITESPACE():
	#: {INTRALINE_WHITESPACE}
	if(INTRALINE_WHITESPACE()):
		return True

	#: {LINE_ENDING}
	if(LINE_ENDING()):
		return True

	return False


def EMPTY():
	return True

def EOF():
	return fileEnded 
