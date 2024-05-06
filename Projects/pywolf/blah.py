import re

regex = re.compile('[^a-zA-Z] ')
#First parameter is the replacement, second parameter is your input string
print(regex.sub('', 'Kona District'))
#Out: 'abdE'
