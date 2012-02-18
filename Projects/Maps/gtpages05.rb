require 'rubygems'
require 'exifr'
require 'mini_exiftool'
require 'gengtpage05'
require 'resizeimg05'

def latlon_to_f( latlon, latlon_ref)
	puts "exifr calculations"
	puts "test"
	llstrs = latlon.to_s.split('/')
	sec = (llstrs[0][-4,4].to_f)/(llstrs[1].to_f)
	puts "sec = " + sec.to_s
	min = llstrs[0][-6,2].to_f
	puts "min = " + min.to_s
	deg = llstrs[0][0,llstrs[0].length-6].to_f
	puts "deg = " + deg.to_s

	puts "latlon_ref = " + latlon_ref.to_s
	if latlon_ref.to_s == 'N'
		puts "ref = North"
		ref = 1
	elsif latlon_ref.to_s == 'S'
		puts "ref = South"
		ref = -1
	elsif latlon_ref.to_s == 'E'
		puts "ref = East"
		ref = 1
	elsif latlon_ref.to_s == 'W'
		puts "ref = West"
		ref = -1
	else
		puts "Couldn't determine reference"
	end
		(deg + min/60 + sec/3600)*ref
end	

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

def to_zulu(td_ary)
    #probably no need for this!
end

def to_yyyymmdd(td_ary)
	puts td_ary[5] + " " + td_ary[1] + " " + td_ary[2]
	if td_ary[1] == "Jan"
		mo = "01"
	elsif td_ary[1] == "Feb"
		mo = "02"
	elsif td_ary[1] == "Mar"
		mo = "03"
	elsif td_ary[1] == "Apr"
		mo = "04"
	elsif td_ary[1] == "May"
		mo = "05"
	elsif td_ary[1] == "Jun"
		mo = "06"
	elsif td_ary[1] == "Jul"
		mo = "07"
	elsif td_ary[1] == "Aug"
		mo = "08"
	elsif td_ary[1] == "Sep"
		mo = "09"
	elsif td_ary[1] == "Oct"
		mo = "10"
	elsif td_ary[1] == "Nov"
		mo = "11"
	elsif td_ary[1] == "Dec"
		mo = "12"
	else
		mo = "00"
	end
	td_ary[5] + "-" + mo + "-" + td_ary[2]
end	


def gather_group_info()
	#create all array of all the lat/lons for scaling and making extra markers.
	#pass that array to gentpage03.rb
	#group[pic_file, lat, lon]
    	#mypix.each do |pic_file| 
		
	
end


### give a photo instead?
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


	#todo:
	#use mini exif tool for everything
	#check for existance of hash keys and handle errors
	#make option to skip resize
    if ARGV[1] == "resize"
    	system("rm *_web.jpg")
	puts "deleting web images"
    end	
      
    system("rm *.htm")
    allpix = Dir.glob("*.jpg")
    smallpix = Dir.glob("*_web.jpg")
    mypix = allpix-smallpix
    puts mypix.class
	
    puts "sort mypix by date"	
    puts "***Before***"
    puts mypix
    puts "***After***"
    #do something about images that don't have dates....
    puts "Number of images = " + mypix.size.to_s
    
    n=0
    mypix.each do |pic_file| 
	print "Time for " + pic_file.to_s  + " = "
	puts EXIFR::JPEG.new(mypix[n]).exif.to_hash[:date_time_original]
	n = n +1
    end

    mypix = mypix.sort_by { |a| EXIFR::JPEG.new(a).exif.to_hash[:date_time_original] }
    puts mypix
    #puts EXIFR::JPEG.new(mypix[0]).exif.to_hash[:date_time_original]
    #puts "wip"
    puts " "
    
    file_markers = Array.new
    mypix.each do |pic_file| 
	photo = MiniExiftool.new(pic_file)
	coord = get_latlon_coord(photo)
	file_markers.push([pic_file, coord[0], coord[1]])	
    end
    puts "file_markers:"
    puts file_markers.to_s

    mypix.each do |pic_file| 

    	puts "File name = " + pic_file
	exif_hash = EXIFR::JPEG.new(pic_file).exif.to_hash
	#print out all elements
	#exif_hash.each_pair do |k,v|
        #    puts "#{k.to_s.rjust(30)} : #{v}"
	#    puts k
	#    puts k.class
	#end
	#puts exif_hash.size
	#puts exif_hash.class
	#puts exif_hash[:gps_latitude].to_s + exif_hash[:gps_latitude_ref].to_s
	#lat = latlon_to_f(exif_hash[:gps_latitude], exif_hash[:gps_latitude_ref])
	#puts "Latitude = " + lat.to_s
	#puts exif_hash[:gps_longitude].to_s + exif_hash[:gps_longitude_ref].to_s
	#lon = latlon_to_f(exif_hash[:gps_longitude], exif_hash[:gps_longitude_ref])
	#puts "Longitude = " + lon.to_s
	#exif format
	#Fri May 30 13:54:53 -0700 2008
	#Wed May 28 19:03:38 -0700 2008
	#Wed Jun 04 10:37:45 -0700 2008
	#csv format
	#Date format: 2005-06-10
	#Time format: 17:11:00
	photo = MiniExiftool.new(pic_file)

	coord = get_latlon_coord(photo)
	lat = coord[0]
	lon = coord[1]
=begin
	puts "*** miniexiftool start ***"
	photo = MiniExiftool.new(pic_file)
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
=end
	img_ht = 360
	sigma = 0.5

        if ARGV[1] == "resize"
	    resize_img(pic_file.split('.')[0],img_ht,sigma,photo)
        end

	make_gtp(mypix,pic_file.split('.')[0], lat, lon, exif_hash, photo, ARGV[0],file_markers)

	ds_ary = exif_hash[:date_time_original].to_s.split(' ')	
	puts ds_ary
	
	orig_date = to_yyyymmdd(ds_ary)
	puts "original date " + orig_date
        
        #if !lat.nil? && !log.nil?  	
        if !photo.GPSLatitude.nil? && !photo.GPSLongitude.nil?  
            op_str = pic_file + "," + sprintf("%0.6f",lon).to_s + "," + sprintf("%0.6f",lat)
	else
            op_str = "no geotag data"
        end
	op_str += "," + orig_date + "," + ds_ary[3]
	puts op_str	
	end
    
