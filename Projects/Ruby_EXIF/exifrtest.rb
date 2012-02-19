require  'rubygems'
require 'exifr'
puts "hello"
puts EXIFR::JPEG.new('bigben.jpg').exposure_time.to_s