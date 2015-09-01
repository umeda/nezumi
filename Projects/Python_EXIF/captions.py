from sys import argv

if len(argv) < 2:
	print 'oops - you forgot to enter a file name'
	exit('Sss...')

filename =  argv[1]

print filename

with open(filename, 'rU') as fn:
  for line in fn:
     print line

#http://www.sno.phy.queensu.ca/~phil/exiftool/faq.html
#exiftool -title="test test test" bigben.jpg

