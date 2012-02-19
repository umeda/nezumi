require  'rubygems'
require 'exifr'
require 'mini_exiftool'
require 'open-uri'
require 'RMagick'
include Magick


def met_f(latlon)
	llstrs = latlon.to_s.split(' ')
	sec = llstrs[3].chomp.to_f 
	puts "sec = " + sec.to_s
	min = llstrs[2].chomp.to_f
	puts "min = " + min.to_s
	deg = llstrs[0].chomp.to_f
	puts "deg = " + deg.to_s
	latlon_ref = llstrs[4] 
	puts "latlong_ref = " + latlon_ref
	if latlon_ref == 'N'
		puts "ref = North"
		ref = 1
	elsif latlon_ref == 'S'
		puts "ref = South"
		ref = -1
	elsif latlon_ref == 'E'
		puts "ref = East"
		ref = 1
	elsif latlon_ref == 'W'
		puts "ref = West"
		ref = -1
	else
		puts "Couldn't determine reference"
		ref = 0
	end
		(deg + min/60 + sec/3600)*ref
end	

### give a photo - get  coordinates
def get_latlon_coord(photo)
	puts "*** miniexiftool start ***"
        puts photo.GPSLatitude
        puts photo.GPSLongitude
        if !photo.GPSLatitude.nil? && !photo.GPSLongitude.nil?  
          puts "going to metf for LAT"
          lat = met_f(photo.GPSLatitude)
          puts "going to metf for LON"
          lon = met_f(photo.GPSLongitude)
	  puts "Latitude = " + lat.to_s
	  puts "Longitude = " + lon.to_s
	  puts photo.class
	  puts "*** miniexiftool end ***"
        else
	   puts "no geotag data"
           lat = nil
           lon = nil
        end		
	latlon_coord = [lat,lon]
end




puts "hello"
myPic = EXIFR::JPEG.new('bigben.jpg')
puts myPic.exposure_time.to_s

photo = MiniExiftool.new('bigben.jpg')

coord = get_latlon_coord(photo)
lat = coord[0]
lon = coord[1]
puts lat
puts lon
puts lat.class
latStr = sprintf("%0.6f",lat).to_s
lonStr = sprintf("%0.6f",lon).to_s
puts latStr
puts lonStr


#imageAddress = "http://maps.google.com/maps/api/staticmap?center=42.950827,-122.108974&zoom=14 &size=500x500&format=jpg&maptype=roadmap&sensor=false&"
  imageAddress = "http://maps.google.com/maps/api/staticmap?center=" + latStr + "," + lonStr + "&zoom=14&markers=" + latStr + "," + lonStr + "&size=640x640&format=jpg&sensor=false&"
#format type is needed because we spec the file name, 
#size needs to be spec'd but 640X640 is max
#maptype=roadmap is default

open(imageAddress) {|f|
   File.open('map.jpg','wb') do |file|
     file.puts f.read
   end
}

pic = ImageList.new('map.jpg')
pic = pic.rotate(90)
pic.write('map2.jpg') { self.quality = 90 }

