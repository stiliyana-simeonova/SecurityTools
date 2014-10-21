#!/usr/local/bin/python2.7


#
# The script was developed on the fly to meet my urgent need to convert BurpsuitePro history logs into flat files
# The functionality is very basic and probably can be improved a lot. At some point I could decide to add some more options
# Sept 2012
# ePsiLoN
# dev at epsilon-labs.com
#


import sys
import argparse
from xml.etree import ElementTree as ET
from base64 import b64decode

def main():
	#set defaults
	inputFile = 'burplog.xml'
	outputFile = 'burpflat.log'

	#check arguments
	parser = argparse.ArgumentParser(
		description = 'The program converts BurpSuitePro proxy history logs to flat logs',
		epilog = 'author: ePsiLoN; dev at epsilon-labs.com')
	parser.add_argument('-f','--file', default=inputFile, help='BurpSuitePro log file you want to convert (default: %(default)s)')
	parser.add_argument('-o','--output', default=outputFile, help='Output flat file (default: %(default)s)')
	parser.add_argument('--version', action='version', version='1.0')
	args = parser.parse_args()	

	try:
		#open the output file
		out = open(args.output, 'w+')

		#parse the burp history log
		xmlLog = ET.parse(args.file)
		rootElement = xmlLog.getroot()
		burpItemsList = rootElement.findall('item')
		if burpItemsList!=None:
			for item in burpItemsList:
				#todo: check if the request and response strings are Base64 encoded
				request = item.find('request').text
				response = item.find('response').text
				#decode
				request = b64decode (request)
				response = b64decode (response)
				#write in the output file
				out.write(request)
				out.write(response)
			
			#close the output file
			out.close()
			#print a message with number of log items parsed 
			print 'End! Total number of log items parsed: %s ' %(len(burpItemsList))

	except Exception, inst:
		print 'Unexpected error!'
	pass


if __name__ == "__main__":
	main()
