import sys, getopt
import re
import time

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

formats = {
	'h':1,
	'H':1,
	'b':0,
	'B':0
}

def translate(tokens):	
	
	instr_struct = {
			'opcode':3,
			'I':1,
			'a':2,
			'b':2,
			'Imm8':8
	}	
	# declare empty instruction code
	instruction = dict(zip(instr_struct.keys(),[None]*len(instr_struct.keys())))

	opcode = tokens[0]
	if opcode in opCodes.keys():

		instruction['opcode'] = opCodes[opcode][0]

		if opCodes[opcode][1] == 'I':
			# opcode has two inputs, Register a and operand (either immediate value or register b)
			Ra = tokens[1]
			# convert Ra to appropriate format
			if Ra in regList:
				Ra = Ra.replace('R','')
				instruction['a'] = int(Ra)
			else:
				raise Exception('Ra is not in reglist')

			operand = tokens[2]
			#check if operand is Immediate or not			
			if operand[0] == '#': 
				instruction['I'] = 0b1
				operand = operand.replace('#','')

				instruction['Imm8'] = int(operand)
				#set register b to 0
				instruction['b'] = 0b00
			# operand is register
			elif operand in regList or operand in ['['+x+']' for x in regList]:
				instruction['I'] = 0b0
				operand = operand.replace('R','')

				instruction['b'] = int(operand)
				#set Imm8 to zero
				instruction['Imm8'] = 0b00000000
		# JMP instructions only take immediate values as inputs 
		elif opCodes[opcode][1] in (0,1):
			imm8 = tokens[1]
			imm8 = imm8.replace('#','')

			instruction['Imm8'] = int(imm8)
			# set I bit
			instruction['I'] = opCodes[opcode][1]
			instruction['a'] = 0b00
			instruction['b'] = 0b00
		#construct final 16 bit instruction
		Binstruction = ''
		try:
			for key, val in instruction.items():
				# format to correctly sized binary numer
				instruction[key] = format(val,f"0{instr_struct[key]}b")
				Binstruction += instruction[key]
		except:
			print("formatting failed")

		return (instruction,Binstruction,format(int(Binstruction,2),"04X"))
	else:
		raise Exception("Unknown OPCODE")

def parseLine(line):
	line = line.replace(',','')
	re.sub('\s+',' ',line)
	return line.split()

def getArgs():
	argsOut = {
		'format':0,
		'inputfile':'',
		'outputfile':'',
		'verbose':0
	}
	argv = sys.argv[1:] #skipping first two
	try:
		opts, args = getopt.getopt(argv,"i:o:f:v")
	except getopt.GetoptError as e:
		print(e)
		sys.exit(2)

	for opt, arg in opts:
		if(opt == "-i"):
			argsOut['inputfile'] = arg
		elif (opt == "-o"):
			argsOut['outputfile'] = arg
		elif opt == '-f':
			if arg in formats.keys():
				argsOut['format'] = formats[arg]
			else:
				print("This format is not supported, supported formats are: ")
				print(*formats.keys(), sep = ', ')
				sys.exit(2)
		elif opt == '-v':
			argsOut['verbose'] = 1

	if argsOut['inputfile'] == '':
		print("Missing input file")
		sys.exit(2)
	return argsOut

if(__name__ == "__main__"):

	start = time.time()

	args = getArgs()

	outfileName = args['outputfile'] if args['outputfile'] != '' else args['inputfile'].replace('.txt','-asm.txt')

	with open(args["inputfile"],"r") as file:
		with open(outfileName,'w') as outfile:
			for line in file:
				try:
					tokens = parseLine(line)
					try:
						instruction = translate(tokens)
						#print('0b' + instruction[1] + ' , 0x' + instruction[2])
					except Exception as e:
						print(f"translation failed: {e}")
						sys.exit(2)
				except:
					print("tokeniser failed")
					sys.exit(2)
				finally:
					newline = instruction[args['format']+1]
					if args['verbose']:
						print(newline)
					outfile.write(newline)
	stop = time.time()
	print('Assembly completed succesfully!')
	print('Elapsed time: '+str((stop-start)*1000)+'ms')
			