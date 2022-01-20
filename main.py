from lib2to3.pgen2 import token
import sys, getopt
import re

opCodes = {
	'MOV': [0b000,'I'],
	'ADD': [0b001,'I'],
	'SUB': [0b010,'I'],
	'ADC': [0b011,'I'],
	'LDR': [0b100,'I'],
	'STR': [0b101,'I'],
	'JMP': [0b110, 0],
	'JNE': [0b110, 1],
	'JCS': [0b111, 0],
	'JMI': [0b111, 1],	
}

regList = ['R0','R1','R2','R3']

def translate(tokens):	
	# declare empty instruction code
	instr_struct = ['opcode','I','a','b','Imm8']	
	instruction = dict(zip(instr_struct,[None]*len(instr_struct)))

	opcode = tokens[0]
	if opcode in opCodes.keys():

		instruction['opcode'] = opCodes[opcode][0]

		if opCodes[opcode][1] == 'I':
			# opcode has two inputs, Register a and operand (either immediate value or register b)
			Ra = tokens[1]
			# convert Ra to appropriate format
			if Ra in regList:
				Ra = Ra.replace('R','')
				instruction['a'] = bin(int(Ra))
			else:
				raise Exception('Ra is not in reglist')

			operand = tokens[2]
			#check if operand is Immediate or not			
			if operand[0] == '#': 
				instruction['I'] = 0b0
				operand = operand.replace('#','')

				instruction['Imm8'] = bin(int(operand))
				#set register b to 0
				instruction['b'] = 0b00
			elif operand in regList:
				instruction['I'] = 0b1
				operand = operand.replace('R','')

				instruction['b'] = bin(int(operand))
				#set Imm8 to zero
				instruction['Imm8'] = 0b00000000
			elif opCodes[opcode][1] in (0,1):
				imm8 = tokens[1]
				imm8 = imm8.replace('#','')

				instruction['Imm8'] = bin(int(imm8))
				# set I bit
				instruction['I'] = opCodes[opcode][1]
		return instruction
	else:
		raise Exception("Unknown OPCODE")


def parseLine(line):
	line = line.replace(',','')
	re.sub('\s+',' ',line)
	return line.split()

def getArgs():
	outArgs = {
		"inputfile":"test",
		'outputfile':'',	
	}
	argv = sys.argv[1:] #skipping first two
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError as e:
		print(e)
		sys.exit(2)

	for opt, arg in opts:
		if(opt == "-i"):
			outArgs['inputfile'] = arg
		elif (opt == "-o"):
			outArgs['outputfile'] = arg
	return outArgs

if(__name__ == "__main__"):
	args = getArgs()

	with open(args["inputfile"],"r") as file:
		numlines = 0
		for line in file:
			print(numlines)
			numlines += 1
			try:
				tokens = parseLine(line)
				print(tokens)

				try:
					instruction = translate(tokens)
					print(instruction)
				except Exception as e:
					print(f"translation failed: {e}")

			except:
				print("tokenizer failed")
			