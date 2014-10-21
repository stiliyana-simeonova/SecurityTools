#! /usr/bin/python
#
# The script performs partial deobfuscation of php code obfuscated with pipsomania obfuscator (http://www.pipsomania.com/best_php_obfuscator.do)
# It converts the file from shell version to more readable format by replacing "\xXX"-like sequences with their
# ascii representation and introduces new lines.
# TODO: deal with $_GLOBAL and other artificially introduced assignment
# 
# Author: ePsiLoN ( dev at epsilon - labs . com)
# Version: 0.1
# Date: 2014-10-12
# 
# The script is free to use and modify

import binascii, re
import argparse

def insertnewline(string):
	string=string.replace(";","; \n")
	return string

def asciirepl(match):
	s = match.group(1)  
	return binascii.unhexlify(s)

def reformat_content(data):
	p = re.compile(r'\\x(\w{2})')
	return p.sub(asciirepl, data)

def main():
	#set some default values 
	fname_source = 'source.php'
	fname_target = 'source-deobf.php'

	#check arguments
	parser = argparse.ArgumentParser(
			description = 'The scripts performs simple deobfuscation task by converting \\xXX shel like strings to their ASCII representation',
			epilog = 'author: ePsiLoN; dev at epsilon-labs dot com')
	parser.add_argument('-f','--file', required=True, default=fname_source, help='The file to be deobfuscated (default: %(default)s)')
	parser.add_argument('-o','--output', required=True, default=fname_target, help='Output file (default: %(default)s)')
	parser.add_argument('--version', action='version', version='1.0')
	args = parser.parse_args()	

	try:
		#open the output and input files
		file_source = open(args.file,'r')
		file_target = open(args.output,'w+')

		#do the job
		for line in file_source:
			line = reformat_content(line)
			line = insertnewline(line)
			file_target.write(line)

		file_source.close()
		file_target.close()

		#print a final message 
		print 'Done!'
	except Exception, ints:
		print 'Unexpected error! Try calling with --help and check if all expected parameters are filled out.'
	pass

if __name__ == "__main__":
	main()
	
