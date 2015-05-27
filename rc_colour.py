#!/usr/bin/python

import binascii
import sys
import string
import re


class byteFile:

	def __init__(self, filename):

		self.filename = filename
		self.hexMode = False
		data = open(filename, "rb").read()

		regex = re.compile(r"@(\w+)\|(.*)\|$", re.IGNORECASE | re.MULTILINE)
		self.rcDict = dict(regex.findall(data))

	def setValue(self, key, value):
		self.rcDict[key] = value

	def keyExists(self, key):
		return key in self.rcDict

	def printContent(self):
		for key, value in self.rcDict.iteritems():
			print key, "\t", value

	def writeFile(self):
		#Cycle through the tags and write a new rc.file
		output = open(filename, 'wb')
		if(self.hexMode):
			for key,value in self.rcDict.iteritems():
				output.write(''.join(('@',key,'|',binascii.unhexlify(value),'|\n')))
		else:
			for key,value in self.rcDict.iteritems():
				output.write(''.join(('@',key,'|',value,'|\n')))

	def setHexMode(self):
		self.hexMode = True
		# Go through the dictionary and convert any values to hex
		for key, value in self.rcDict.iteritems():
			self.rcDict[key] = binascii.hexlify(value)

# Get the file name from the command line arguments
rcData = byteFile(sys.argv[1])
rcData.setHexMode();

# List the items
rcData.printContent();

keyName = raw_input('Which key do you want to edit? ')

if rcData.keyExists(keyName): 
	print "Current value of ", keyName, " is ", rcData.rcDict[keyName]
	newVal = raw_input('Enter new value: ')

	rcData.setValue(keyName, newVal)

	print 'Writing changes to file...'
	rcData.writeFile()
else:
	print "Can't find that tag."

