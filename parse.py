#!/sbin/python3
from sexpdata import * 
import sys
import argparse
'''
LC      =       num
        |       id
        |       (lambda (id) LC)
        |       (LC LC)
        |       (+ LC LC)
        |       (* LC LC)
        |       (ifleq0 LC LC LC)
        |       (println LC)
'''

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('inFile', metavar='if',help='input file')
	parser.add_argument('-outFile', dest='of',help='output file')
	args = parser.parse_args()

	f = None
	try:
		f = open(args.inFile)
	except Exception: 
		print("Failed to open file: " + args.inFile)
		sys.exit(1)

	x = None
	try:
		sexp = f.read()
		x = "import sys;sys.setrecursionlimit(20000)" + transform(loads(sexp))
	except Exception: 
		print("Failed parsing")
		sys.exit(1)

	try:
		if args.of is not None:
			out = open(args.of,'w')
			out.write(x)
			out.close()
		else:
			print(x)
	except Exception: 
		print("Failed to write to file")

def test():	
	statements = [
	"(+ 1 2)",
	"(λ (x) (+ x 1))",
	"(* (+ 9 3) (- 4 5))",
	"(ifleq0 1 2 3)",
	"(println (+ 1 2))",
	"(λ (loop) ((loop loop) 1))",
	"((λ (x) (+ x 1)) 1)"]
	for state in statements:
		print (transform(loads(state)))

def transform(x):
	if type(x) is not list:
		if type(x) is Symbol:
			return x.tosexp()
		return str(x) 
	
	if type(x[0]) is list:
		return "(" + transform(x[0]) + "(" + transform(x[1]) + "))"
	
	if x[0].tosexp() in '+*':
		return "(" + transform(x[1]) + str(x[0].tosexp()) + transform(x[2]) + ")"

	if x[0].tosexp() == 'λ':
		return "(lambda " + x[1][0].tosexp() +":" + transform(x[2]) + ")"

	if x[0].tosexp() == 'ifleq0':
		return "(" + transform(x[2]) + " if " + transform(x[1]) + " <=0 else " + transform(x[3]) + ")"

	if x[0].tosexp() == 'println':
		return "(sys.stdout.write(str(" + transform(x[1])+") + '\\n'))"

	return "(" + transform(x[0]) + "(" + transform(x[1]) + "))"


if __name__ == '__main__':
	main()
