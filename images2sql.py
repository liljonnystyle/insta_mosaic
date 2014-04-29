#!/usr/bin/python

import Image
from os import listdir
from os.path import isfile, join
from numpy import *
import MySQLdb as mdb
from optparse import OptionParser

def createmdb(table):
	con = mdb.connect('localhost','root','jonny5','testdb')

	with con:
		cur = con.cursor()
		dropcommand = "DROP TABLE IF EXISTS " + str(table)
		cur.execute(dropcommand)
		createcommand = "CREATE TABLE " + str(table) + "(File VARCHAR(100) PRIMARY KEY, "
		for i in xrange(100):
			createcommand = createcommand + "Pixel_" + str(i) + " VARCHAR(15)"
			if i != 99:
				createcommand = createcommand + ", "
			else:
				createcommand = createcommand + ")"
		cur.execute(createcommand)
	print 'created table for image filenames and pixel intensities'

def add2mdb(table,name,pixels):
	con = mdb.connect('localhost','root','jonny5','testdb')

	with con:
		cur = con.cursor()
		command = "INSERT INTO " + str(table) + " VALUES(\'" + str(name) + "\', \'"
		for i in xrange(100):
			command = command + str(pixels[i]) + "\'"
			if i != 99:
				command = command + ", \'"
			else:
				command = command + ")"
		cur.execute(command)

def main():
	p = OptionParser()
	p.add_option('-n',action="store",dest="nimages",
		type="int",default=0,
		help="number of images to store in database, 0 if unlimited")

	(options,args) = p.parse_args()

	nimages = int(options.nimages)

	if nimages == 0:
		table = "Images"
	else:
		table = "Images" + str(nimages)

	createmdb(table)

	#make dict of images in pics/
	#save dict to mySQL db for future runs
	#dict = {}
	count = 0
	#t = time.time()
	for file in listdir('pics'):
		if nimages != 0 and count > nimages: break
		filename = 'pics/' + file
		image = Image.open(filename)
		image = image.resize((10,10),Image.ANTIALIAS)
		pixels = list(image.getdata())
		add2mdb(table,filename,pixels)
		#dict[file] = pixels
		count += 1
	#	if count%100 == 0:
	#		print str(count) + ' images added to database'
	#		#elapsed = time.time() - t
	#		#t = time.time()
	#		#print elapsed
	print 'added images to database'

if __name__ == '__main__':
        main()

