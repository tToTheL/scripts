#!/usr/bin/python2.7

# The goal of this is to take a tab seperated file from libreoffice and get a 
# fixed width file but using tabs instead of spaces, which libreoffice doesn't offer.

# Some text editors display tabs defferently, I tested this in vim

import sys
import math
import csv

inFile = str(sys.argv[1])

if not "/" in inFile:
	inFile = "./%s" % (inFile)

rows = [] 	# store the rows of the data
maxTWidths = [] # holds the max size of a cell for each column in the number of tabs
tWidth = 7 	# tab width starting from 0

# a function to determine how wide a cell is, in tab units
def getTabs(cell):
	tabs = int(math.ceil((len(cell)/float(tWidth))))
	if len(cell) == 0:
		tabs += 1
	return tabs

# open the file, read it in, find out the max widths of the columms
with open(inFile, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t') #, quotechar='|')
	for row in csvreader:
		rows.append(row)
		for key, cell in enumerate(row):
			cell = str(cell).strip()
			tabs = getTabs(cell)
			try:
				# if bigger than the biggest make note
				if tabs > maxTWidths[key]:
					maxTWidths[key] = tabs
			except:
				# it is our first time dealing with this column
				maxTWidths.append(tabs)

# output the data, nicely formatted
for row in rows:
	for col, cell in enumerate(row):
		tabs = getTabs(cell)
		sys.stdout.write(str(cell))
		sys.stdout.write('\t')
		# print the extra tabs needed to make up for the size difference between
		# rows with small content and rows with big content in the same column
		for i in range(0, (maxTWidths[col] - tabs)):
			sys.stdout.write('\t')
	sys.stdout.write('\n')
				
				
				
