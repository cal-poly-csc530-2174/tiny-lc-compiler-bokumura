# tiny-lc-compiler-bokumura

Team: 
	Brandon Okumura
	Sam Hsu

Description: 
	LC -> Python parser
	Takes an LC and transforms it into Python code (using Lambda expressions).  

	It will print the lambda expression to stdout if no output file is specified. 

Notes: 
	We needed 'sys.setrecursionlimit(20000)' for the 10k test (because python :/)

To Run: 
	$python3 parse.py <inputFile> [-h] [-outFile <outputFile>]