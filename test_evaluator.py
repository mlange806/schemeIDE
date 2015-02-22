from evaluator import evaluate

def main():
	input_file = open("test_input.txt", "r")
	output_file = open("test_output.txt", "r")

	inputs = input_file.readlines()
	outputs = output_file.readlines()
	if(len(inputs) != len(outputs)):
		print("Mismatched test inputs and outputs, check the files")
	else:
		passedCases = 0
		failedCases = 0
		for index in range(len(inputs)):
			input = inputs[index].strip()
			output = outputs[index].strip()
			actual_output = str(evaluate(input))
			if(actual_output != output):
				failedCases += 1
				print("Input <{0}> produced <{1}> instead of <{2}>.".format(input, actual_output, output))
			else:
				passedCases += 1
		print("{0}/{1} test cases passed.".format(passedCases, passedCases + failedCases))
main()