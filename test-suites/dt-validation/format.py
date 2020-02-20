import re
import sys
from collections import defaultdict

### BEFORE YOU RUN THIS SCRIPT, READ THE BELOW LINES
### This script will look at a file that has the output of dt_binding_check (preferably all of the output. meaning stdout AND stderr) 
### To have both stdout and stderr be printed into one file, you must run the following command: dt_binding_check &> dtvout
### On line 27, the file that will be read is selected, please be sure that the name of the file that you intend to analyze is the first argument of the "open" command

"""
My Notes
Things to make this script print: 
	Status of a file (pass/fail/warning)
		Right now, Trying to test the status of every line begining with "CHKDT" 
			Done. Seems to be no problems
		Warnings (line 1904 of dtvout) 
			separated

Things To Do:
	General printing of the files that passed and failed

Things Done: 
	Separated Files with Errors or warnings from the rest

"""

# if len(sys.argv) == 1: #we need an argument to identify the name of the file
# 	print("no arguments")
# 	exit()

dtoutput = open("dtvout", "r")# the second argument (aka argv[1]) will be the file that we look at ## sys.argv[1]
lines = dtoutput.readlines()

"""
#Checking lines that begin with "CHKDT" for errors
	it does this by recording the name of the file on the "CHKDT" line and seing if it is in any line after 
	it is first seen. If it is seen later, the later line gets printed

for i,line in enumerate(lines):
	linereg = re.search("CHKDT +(\w+/.+$)",line)
	if linereg != None: 
		filename = linereg.group(1)
		for j in range(i+1, len(lines)): 
			innerReg = re.search(filename, lines[j])
			if innerReg != None: 
				print(filename)
"""

#separating the lines with warnings and errors
elist = {}; wlist = {}
for i,line in enumerate(lines):
	linereg = re.search("^ +(DTC|CHECK|CHKDT|SCHEMA)",line)
	if linereg == None: 
		warningreg = re.search("^(.*): *(Warning.*)$", line)
		if warningreg != None:
			wlist[warningreg.group(1)] = warningreg.group(2)
		else:
			ereg = re.search("^(.*yaml): *(.*)$", line)
			print(line)
			print(ereg.group(1))
			elist[ereg.group(1)] = ereg.group(2)

for i, line in enumerate(lines):
	linereg = re.search("^ *(CHECK|CHKDT|SCHEMA) +(.*)$",line)
	if linereg != None: 
		currname = linereg.group(2)
		if linereg.group(1) == "CHECK":
			failed = False
			for name in elist.keys(): 
				if currname in name: #checking if currname is in the key of elist because the elist key is shows the directory path from root
					failed = True
					print("\"", currname.replace('.', '_').replace(',', '_').replace('/', '.'), ".check\" : ", "\"FAIL\"",sep='')
					break
			if(not(failed) and not(currname in wlist) ):
				print("\"", currname.replace('.', '_').replace(',', '_').replace('/', '.'), ".check\" : ", "\"PASS\"",sep='')
		elif linereg.group(1) == "CHKDT":
			print("\"", currname.replace('.', '_').replace(',', '_').replace('/', '.'), ".chkdt\" : ", "\"PASS\"",sep='')#I am making the assumption that lines beginning with "CHKDT" have passing files based on previous testing
		elif linereg.group(1) == "SCHEMA":
			print("\"", currname.replace('.', '_').replace(',', '_').replace('/', '.'), ".schema\" : ", "\"PASS\"",sep='')#Assuming lines beginning with "Schema" have passing files

print("\nWarnings: ")
for name, warning in wlist.items(): 
	print("Filename: ", name, " ", warning)

print("\nErrors: ")
for name, error in elist.items(): 
	print("Filename: ", name, " Error: ", error)

print("\nWarning Count: ", len(wlist))
print("\nError Count: ", len(elist))
