#! /usr/bin/env python3

from PIL import Image
from imtools import *
import os

cwd = os.getcwd()

filelist = get_imlist(os.getcwd())

print(filelist)

for infile in filelist:
	outfile = os.path.splitext(infile)[0] + ".jpg"
	if infile != outfile:
		try:
			Image.open(infile).save(outfile)
		except IOError:
			print("cannot convert", infile)

