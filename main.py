import sys, getopt

if(__name__ == "__main__"):
	inputfile = ''
	outputfile = ''
	argv = sys.argv[1:] #skipping first one
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError as e:
		print(e)
		sys.exit(2)

	for opt, arg in opts:
		print(f"{opt} {arg}")