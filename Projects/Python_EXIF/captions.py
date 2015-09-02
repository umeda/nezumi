import subprocess
from sys import argv
import os

#This program uses Exiftool to add a title and individual descriptions to photos
#Exiftool must be loaded and runnable from the command line.
#The captions file must contain a photo filename and a caption seperated by a pipe | 
#One photo/caption per line.
#img001|The Charles River flows right by MIT.
#img002|We love eating crab rolls!
#Run this as a last step before uploading.
#Darktable seems to overwrite the description field with the camera brand.
#exiftool -title="test test test" bigben.jpg
#http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html
#http://owl.phy.queensu.ca/~phil/exiftool/examples.html
if len(argv) < 3:
	print 'oops - you forgot to enter a file name and a title'
	exit('Sss...')

filename =  argv[1]

print filename

with open(filename, 'rU') as fn:
  for line in fn:
     photo_and_caption = line.split('|')
     #print photo_and_caption[0]
     #print photo_and_caption[1]
     cmd = 'exiftool -title="' + argv[2] + '" -description="' + photo_and_caption[1].rstrip('\n') + '" ' + photo_and_caption[0] 
     print cmd
     # Simple command
     subprocess.call([cmd, '-1'], shell=True)
