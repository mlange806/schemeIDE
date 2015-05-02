from evaluator import *


#The test method runs all the tests in test_input.txt and prints out the results
#Each line of test_input.txt is one of the following:
#-A test case with the format <scheme_code>( : <expected_output>)
##The code <scheme_code> is executed, then the actual expected_output is compared to the expected expected_output
##If the colon section is missing, the expected expected_output is assumed to be 'None'
##If <expected_output> is !, then the expected expected_output is a thrown exception
##If the expected_outputs match, the test case passes - otherwise, it fails
#-A blank line
#-A commented line, which begins with #
#-A script line, which begins with !
##Allowed commands:
##!begin <current_section_name> - begin keeping track of this new section
##!displayexceptions - begin showing any exceptions encountered
##!hideexceptions - stop showing exceptions

def test():
	input_file = open("test_input.txt", "r")
	separator = "-"*70 #This is the line of dashes printed to make a nice-looking chart
	display_exceptions = False #When this is true, any exception encountered will be printed out - can use this to make sure the right exceptions are being thrown
	inputs = input_file.readlines() #Split the input file up into lines
	passedCases = 0 #The overall number of cases that pass
	failedCases = 0 #The overall number of cases that fail
	numTabs = 3 #Controls the display spacing - 3 looks fine
	line_number = 0 #Keeps track of the actual line number in the input file to make it easier to locate test cases
	failedStrings = [] #If a test case fails, its expected_output is added to this list so it can be printed out in one block at the end
	
	#The input file is divided up into several sections, these variables keep track of stats individual to the local sections, as well as the section name
	section_passedCases = 0
	section_failedCases = 0
	current_section_name = ""
	
	#Display the header
	print("{0}Pass\tFail\tTotal".format((numTabs+2)*"\t"))
	print(separator)
	
	for line in inputs:
		line_number += 1 #Update the line number for every line, no matter what's on it
		if(len(line) < 2): #If the line consists of only a newline char, then it's blank - skip it
			continue
		input_output = line.split(":") #Input and expected expected_output are separated by a colon
		input = input_output[0].strip() #Trim the whitespace
		if(len(input_output) == 1): #If there's no colon, then expect an expected_output of 'None'
			expected_output = "None"
		else:
			expected_output = input_output[1].strip() #Otherwise the expected expected_output is whatever was after the colon
		if(expected_output == "" or expected_output == " "): #Unless it's blank, in which case the expected expected_output is 'None'
			expected_output = "None"
		if(input[0] == '!'): #This is a script line
			command = input[1:] #Everything after the ! is the command
			if(command == "displayexceptions"): #Start showing exceptions
				display_exceptions = True
			elif(command == "hideexceptions"): #Stop showing exceptions
				display_exceptions = False
			elif(command.startswith("begin")): #This is defining a new section
				if(current_section_name != ""): #If the current section is not blank (i.e. you're already in a named section), print out the stats for the section that's ending, then reset the stats for this new section
					print("Running {0} tests{4}{1}\t{2}\t{3}".format(current_section_name, section_passedCases, section_failedCases, section_passedCases + section_failedCases, numTabs*"\t"))
					section_passedCases = 0
					section_failedCases = 0
				current_section_name = command.split(" ")[1] #And update the name of the current section
		elif(not input[0] == '#'): #If the line begins with a #, it's a comment so just skip the whole thing
			actual_output = str(evaluate(input)) #Evaluate the input to get the actual expected_output
			if(actual_output.find("Error:") == 0): #This is the format of the string the evaluator returns when it encounters an exception
				if(expected_output == "!"): #If you encountered an exception and expected an exception, that counts as a pass
					section_passedCases += 1
					passedCases += 1
				else: #If you encountered an exception but didn't expect one, that's failure
					section_failedCases += 1
					failedCases += 1
					failedStrings.append("Test case #{3} on line {4} failed: Input <{0}> produced an exception '{1}' instead of <{2}>".format(input, actual_output, expected_output, str(failedCases + passedCases), line_number))
				if(display_exceptions): #If this flag is on, print any exception encountered - for tracking purposes
					failedStrings.append("Test case #{0} on line {1} - Exception: {2}".format(str(failedCases + passedCases), line_number, actual_output))
			else: #Otherwise, you got good expected_output from the evaluator
				if(actual_output != expected_output): #Compare the actual output to the expected - failure state
					section_failedCases += 1
					failedCases += 1
					failedStrings.append("Test case #{3} on line {4} failed: Input <{0}> produced <{1}> instead of <{2}>.".format(input, actual_output, expected_output, str(failedCases + passedCases), line_number))
				else: #Success state
					section_passedCases += 1
					passedCases += 1
	if(current_section_name != ""): #After all the tests are finished, if you're in a named section print out the stats for it
		print("Running {0} tests{1}{2}\t{3}\t{4}".format(current_section_name, (numTabs-1)*"\t", section_passedCases, section_failedCases, section_passedCases + section_failedCases))
		
	#Print the footer
	print(separator)
	print("Total:{0}{1}\t{2}\t{3}".format((numTabs+2)*"\t", passedCases, failedCases, passedCases + failedCases))
	print("{0}/{1} test cases passed.".format(passedCases, passedCases + failedCases))
	
	#Print the info of any tests that failed
	for failure in failedStrings:
		print(failure)
if(__name__ == "__main__"):
	test()
