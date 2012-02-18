require 'open-uri'


#imageAddress = "http://maps.google.com/maps/api/staticmap?center=42.950827,-122.108974&zoom=12&size=500x500&format=jpg&maptype=roadmap&sensor=false&"
  imageAddress = "http://maps.google.com/maps/api/staticmap?center=42.950827,-122.108974&zoom=12&size=640x640&format=jpg&sensor=false&"
#format type is needed because we spec the file name, 
#size needs to be spec'd but 640X640 is max
#maptype=roadmap is default
open(imageAddress) {|f|
   File.open('map.jpg','wb') do |file|
     file.puts f.read
   end
}