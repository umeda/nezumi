from sys import argv
import os

if len(argv) < 2:
	print 'oops - you forgot to enter a file name'
	exit('Sss...')

filename =  argv[1]

print filename

with open(filename, 'rU') as fn:
  for line in fn:
     photo_and_caption = line.split('|')
     print photo_and_caption[0]
     print photo_and_caption[1]

#http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html
#exiftool -title="test test test" bigben.jpg

print os.path.basename(filename)
path, fn = os.path.split(filename)
print path
