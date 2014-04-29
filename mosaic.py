#!/usr/bin/python

import Image
from os import listdir
from os.path import isfile, join
import math
from numpy import *
import re
import MySQLdb as mdb
import time
from optparse import OptionParser

def main():
	p = OptionParser()
	p.add_option('-n',action="store",dest="nimages",
		type="int",default=0,
		help="number of images to store in database, 0 if unlimited")
	p.add_option('-s',action="store",dest="subimgsize",
		type="int",default=40,
		help="number of pixels s x s for sub-image")

	(options,args) = p.parse_args()

	nimages = int(options.nimages)
	subimgsize = int(options.subimgsize)

	table = "Images"

	#open target image and resize
	target = Image.open('target.jpg')
	(tarw,tarh) = target.size
	newtarw = int(tarw/subimgsize)*subimgsize
	newtarh = int(tarh/subimgsize)*subimgsize
	target = target.resize((newtarw,newtarh), Image.ANTIALIAS)

	#loop thru target image
	nx = newtarw/subimgsize
	ny = newtarh/subimgsize
	nboxes = nx*ny
	#best_dict = {}

	con = mdb.connect('localhost','root','jonny5','testdb')

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		if nimages == 0:
			command = "SELECT * FROM " + str(table)
		else:
			command = "SELECT * FROM " + str(table) + " LIMIT " + str(nimages)
		cur.execute(command)
		rows = cur.fetchall()

	dict = {}
	for row in rows:
		values = []
		for i in xrange(100):
			column = "Pixel_" + str(i)
			pixstr = re.split(', |\(|\)',row[column])
			pix1 = int(pixstr[1])
			pix2 = int(pixstr[2])
			pix3 = int(pixstr[3])
			pixeli = (pix1, pix2, pix3)
			values.append(pixeli)
		dict[row["File"]] = values

	#open blank image
	img = Image.new("RGB",(newtarw,newtarh),(0,0,0))

	for i in xrange(nboxes):
		xi = i%nx
		yi = int(math.floor(i/nx))
		left = xi*subimgsize
		upper = yi*subimgsize
		right = left+subimgsize
		lower = upper+subimgsize
		box = (left,upper,right,lower)
		subimg = target.crop(box).resize((10,10), Image.ANTIALIAS)
		pixels = list(subimg.getdata())
		pix1 = subtract(divide(pixels[:],(128.,128.,128.)),(1.,1.,1.))

		#find best match image
		hiscore = -1
		bestkey = ''
		dummy_dict = dict.copy()
		dummy_dict.update((x, subtract(divide(y[:],(128.,128.,128.)),(1.,1.,1.))) for (x, y) in dummy_dict.items())
		dummy_dict.update((x, pix1*y) for (x, y) in dummy_dict.items())
		for (x, y) in dummy_dict.iteritems():
			#pix2 = numpy.subtract(numpy.divide(value[:],(128.,128.,128.)),(1.,1.,1.))
			#score = sum(sum(pix1*pix2))/300
			score = sum(sum(y[:]))/300
			if score > hiscore:
				hiscore = score
				bestkey = x
		#best_dict[i] = bestkey

		#populate image with sub-image
		#file = best_dict[i]
		file = bestkey
		im0 = Image.open(file)
		im0 = im0.resize((subimgsize,subimgsize),Image.ANTIALIAS)
		img.paste(im0,box)
		if i%25 == 0:
			if i == 0:
				print str(i) + '/' + str(nboxes) + ' subimages processed, time: ' + str(time.time())
			else:
				elapsed = time.time() - t
				print str(i) + '/' + str(nboxes) + ' subimages processed, time elapsed for last 25: ' + str(elapsed)
			t = time.time()
			#img.show()
		if i%1000 == 0:
			img.save('image.png','PNG')

	
	saveas = 'image' + str(nimages) + 'images_' + str(subimgsize) + 'pixelsize.png'
	img.save(saveas,'PNG')

if __name__ == '__main__':
        main()
