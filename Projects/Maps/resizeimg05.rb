require 'rubygems'
require 'RMagick'
include Magick

def resize_img(pic_name, img_ht,my_sigma,exifData)

	puts "setting " + pic_name + " to " + img_ht.to_s + " pixels high."
	pic = ImageList.new(pic_name + ".jpg")
	if exifData.has_key?("Orientation")
	if exifData.Orientation.include? "90"
		pic=pic.rotate(90)
		puts "rotation 90 degrees."
	elsif exifData.Orientation.include? "180"
		pic=pic.rotate(180)
		puts "rotation 180 degrees."	
	elsif exifData.Orientation.include? "270"
		pic=pic.rotate(270)
		puts "rotation 270 degrees."
	else
		puts "no rotation."
	end
        end
	pic.change_geometry!('x' + img_ht.to_s) { |cols, rows, img|
		img.resize!(cols, rows)
		}
	puts "sharpening " + pic_name + " with sigma =  " + my_sigma.to_s + "."
	pic = pic.unsharp_mask(radius=0.0, my_sigma.to_f, amount=1.0, threshold=0.05)
	pic.write(pic_name+ '_web.jpg') { self.quality = 90 }

end

