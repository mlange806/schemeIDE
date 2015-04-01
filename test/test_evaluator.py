from evaluator import *

#@TODO:
#More tests for edge cases
#Separate test cases into different types: basic, different functionalities, errors, etc.
#\And have options to enable/disable different ones
#Handle errors and null outputs once those things are implemented in evaluator.py

def main():
	input_file = open("test_input.txt", "r")

	inputs = input_file.readlines()
	passedCases = 0
	failedCases = 0
	for line in inputs:
		input_output = line.split(":")
		input = input_output[0].strip()
		if(len(input_output) == 1):
			output = "None"
		else:
			output = input_output[1].strip()
		if(output == "" or output == " "):
			output = "None"
		if(input[0] == '!'):
			command = input[1:]
			if(command == "displayvars"):
				display_variables()
			elif(command == "displayfuncs"):
				display_functions()
		elif(not input[0] == '#'):
			try:
				actual_output = str(evaluate(input))
			except Exception as e:
				print(e)
			if(actual_output != output):
				failedCases += 1
				print("Test case #" + str(failedCases + passedCases) + " failed: Input <{0}> produced <{1}> instead of <{2}>.".format(input, actual_output, output))
			else:
				passedCases += 1
	print("{0}/{1} test cases passed.".format(passedCases, passedCases + failedCases))
main()
>>>>>>> 3f68f13e1288fa87e2855d98589ef2780e5c2406:test_evaluator.py
