def  make_gtp(mypix,pic_name, lat, lon, exif_hash, photo, group_title,file_markers)



	fpl = File.new(pic_name + ".htm", "w")
	#put these in a table element below.
	#fpl.puts '<a href="' + my_pg_name + (pg_cnt - 1).to_s + '.htm">Previous</a>'
	#fpl.puts 'File Name:&nbsp;' + pic_name + '<br>' 
	#fpl.puts 'File Latitude:&nbsp;' + lat.to_s + '<br>'
	#fpl.puts 'File Longitude:&nbsp;' + lon.to_s + '<br>' 
	#fpl.puts '<a href="' + my_pg_name + (pg_cnt + 1).to_s + '.htm">Next</a>'
	#fpl.puts '<br>'
	#fpl.puts '<img src="' + pic_name + "_web.jpg" +'">'

	puts "generating web page for " + pic_name + "."
	puts mypix 
	currIndex = mypix.index(pic_name + ".jpg")		
	prevIndex = currIndex-1
	nextIndex = currIndex+1
	if nextIndex == mypix.size
		nextIndex = 0
	end
	puts "prev index = " + prevIndex.to_s + "."
	puts "curr index = " + currIndex.to_s + "."
	puts currIndex.class	
	puts "next index = " + nextIndex.to_s + "."
		


	fpl.puts '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
    	fpl.puts '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
	fpl.puts '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml">'
  	fpl.puts '<head>'
    	fpl.puts '<meta http-equiv="content-type" content="text/html; charset=utf-8"/>'
    	fpl.puts '<title>' + group_title + ': ' + pic_name + '</title>'
	fpl.puts '<SCRIPT type=text/javascript SRC = "polyline.js"></SCRIPT> '
#	fpl.puts '<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAzr2EBOXUKnm_jVnk0OJI7xSosDVG8KKPE1-m51RBrvYughuyMxQ-i1QfUnH94QxWIa6N4U6MouMmBA" type="text/javascript"></script> '
	fpl.puts '<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAACqNaecpWrsGd9TjoLgfjPRRBvFCGnRM7qA_wzbnbqTd76m92FhSmHTq2wVQ9Qn5GWfn8WBn9Ax_Gkw" type="text/javascript"></script> '
    	fpl.puts '<script type="text/javascript">'
    	fpl.puts 'function initialize() {'
      	fpl.puts '    if (GBrowserIsCompatible()) {'
	fpl.puts '    var latlonbounds = new GLatLngBounds()// set new bounds'
	fpl.puts '        var map = new GMap2(document.getElementById("map_canvas"));'
	fpl.puts '        var photoLoc = new GLatLng(' + lat.to_s + ',' + lon.to_s + ');'        
        fpl.puts '        geocoder = new GClientGeocoder(); // new for reverse geocoding'
	fpl.puts '        geocoder.getLocations(photoLoc, function(response) {'
	fpl.puts '        	place = response.Placemark[0];'
	#start foolishness - try saving strings to variables in ruby first.
#	fpl.write 'document.getElementById("rgc").innerHTML +=  "<img src=\"globe.png\" height=\"40\" width=\"40\" onmouseover=\"Tip(\'";'
#	fpl.write 'document.getElementById("rgc").innerHTML += "Location: " + place.address + "<br>";'
#	fpl.puts 'document.getElementById("rgc").innerHTML += "\',  FADEIN, 500, FADEOUT, 500)\" onmouseout=\"UnTip()\">\'";'
	#end foolishness

#     this works       
	fpl.puts '        	document.getElementById("rgc").innerHTML += "Location: " + place.address + "<br>";'
#     this works	
	
	fpl.puts '         });'


	#fpl.write '<img src="globe.png" height="40" width="40" onmouseover="Tip(\''
	#put globe info here	
	#fpl.write '<pre>'
	#if !photo.FocalLength.nil?
	#fpl.write 'Location + ' + place.address.to_s
	#fpl.write '<br>'
	#end
	#fpl.write 'hello'	
	#fpl.write '</pre>'
	#fpl.puts  '\',  FADEIN, 500, FADEOUT, 500)" onmouseout="UnTip()">'




	file_markers.each do |snap_shot|  
		puts snap_shot.to_s
		
		fpl.puts '        var cameraIcon = new GIcon(G_DEFAULT_ICON);'
		#fpl.puts '        cameraIcon.image="icon46.png";'    
		fpl.puts '        cameraIcon.image="icon38.png";'    
		#fpl.puts '        cameraIcon.shadow="clear.gif";'    
		fpl.puts '        cameraIcon.iconSize = new GSize(30,30)'
		fpl.puts '        cameraIcon.shadowSize = new GSize(0,0)'
		fpl.puts '        cameraIcon.iconAnchor = new GPoint(15,15)'
		fpl.puts '        var otherMarker = new GMarker(new GLatLng(' + snap_shot[1].to_s + ',' + snap_shot[2].to_s + '),{icon:cameraIcon});'
		fpl.puts '        latlonbounds.extend(new GLatLng(' + snap_shot[1].to_s + ',' + snap_shot[2].to_s + '));'
		fpl.puts'         GEvent.addListener(otherMarker, "click", function() {'
		fpl.puts'           window.location = "' + snap_shot[0].to_s.chop.chop.chop.chop  + '.htm";'
		fpl.puts'         });'
		fpl.puts '        map.addOverlay(otherMarker);'
		
	end
	
	
	
	fpl.puts '        //map.setCenter(photoLoc, 17);'
	fpl.puts '        map.setCenter(latlonbounds.getCenter(), map.getBoundsZoomLevel(latlonbounds));'
	
	fpl.puts '        var cameraIcon = new GIcon(G_DEFAULT_ICON);'
	#fpl.puts '        cameraIcon.image="icon38.png";'    
	#fpl.puts '        cameraIcon.iconSize = new GSize(30,30)'
        #fpl.puts '        var photoMarker = new GMarker(photoLoc,{icon:cameraIcon});'

	#putting the encoded polyline in a separate js file because ruby escapes the backslash char
	#skip the next lines if polyline.js doesn't exist.
	
	if File.exist? "polyline.js"
		fpl.puts'	   var polyline1_2 = getPolyline();'
		fpl.puts'    map.addOverlay(polyline1_2);'
		fpl.puts '    var photoMarker = new GMarker(photoLoc);'
		fpl.puts '   map.addOverlay(photoMarker);'
	end


	fpl.puts '        map.addControl(new GSmallMapControl());'
	fpl.puts '        map.addControl(new GMapTypeControl());'
	fpl.puts '        map.setMapType(G_HYBRID_MAP);'
      	fpl.puts '    }'
    	fpl.puts '}'
    	fpl.puts '</script>'
  	fpl.puts '</head>'

  	fpl.puts '  <body onload="initialize()" onunload="GUnload()">'
	fpl.puts '<a href="'+ mypix[prevIndex].chop.chop.chop.chop + '.htm">Previous</a>&nbsp;Image ' + (currIndex + 1).to_s + ' of ' + mypix.size.to_s + '&nbsp;<a href="'+ mypix[nextIndex].chop.chop.chop.chop + '.htm">Next</a>'
	fpl.puts '<br>'
	fpl.puts '<table border="1">'
	fpl.puts '<tr>'
	fpl.puts '<td>'
	      	fpl.puts '<div id="map_canvas" style="width: 480px; height: 360px"></div>'
	fpl.puts '</td>'
	fpl.puts '<td>'
	      	fpl.puts '<img src="' + pic_name + '_web.jpg" height="360" />'
	fpl.puts '</td>'
	fpl.puts '</tr>'
	fpl.puts '</table>' 



	fpl.puts '<table border="0">'
	fpl.puts '<tr>'
	fpl.puts '<td>'

	#start exif stuff
	fpl.puts '<script type="text/javascript" src="wz_tooltip.js">'
	fpl.puts '</script>'
	#fpl.puts '<a href="javascript:void(0)" onmouseover="Tip(\'Mouse over icons to <br>view photo information.\')" onmouseout="UnTip()">Info:</a>'
	fpl.write '<img src="camera.png" height="40" width="40" onmouseover="Tip(\''
	#put camera info here	
	fpl.write '<pre>'
	if !photo.Model.nil?
		fpl.write 'Camera = ' + photo.Model.to_s
		fpl.write '<br>'
	end
	fpl.write '</pre>'
	fpl.puts  '\',  FADEIN, 500, FADEOUT, 500)" onmouseout="UnTip()">'

	fpl.write '<img src="aperture.png" height="40" width="40" onmouseover="Tip(\''
	#put esposure settngs here	
	fpl.write '<pre>'
	if !photo.MeasuredEV.nil?
		fpl.write 'EV = ' + photo.MeasuredEV.to_s
		fpl.write '<br>'
	end
	if !photo.ExposureTime.nil?
		fpl.write 'Exposure Time = ' + photo.ExposureTime.to_s
		fpl.write '<br>'
	end
	if !photo.AutoISO.nil?
		fpl.write 'Auto ISO = ' + photo.AutoISO.to_s
		fpl.write '<br>'
	end
	if !photo.BaseISO.nil?
		fpl.write 'Base ISO = ' + photo.BaseISO.to_s
		fpl.write '<br>'
	end
	if !photo.ShutterSpeedValue.nil?
		fpl.write 'Shutter Speed = ' + photo.ShutterSpeedValue.to_s
		fpl.write '<br>'
	end
	if !photo.ApertureValue.nil?
		fpl.write 'Aperture = ' + photo.ApertureValue.to_s
		fpl.write '<br>'
	end
	fpl.write '</pre>'
	fpl.puts  '\',  FADEIN, 500, FADEOUT, 500)" onmouseout="UnTip()">'

	fpl.write '<img src="lens.png" height="40" width="40" onmouseover="Tip(\''
	#put lens info here	
	fpl.write '<pre>'
	if !photo.FocalLength.nil?
		fpl.write 'Focal Length = ' + photo.FocalLength.to_s
		fpl.write '<br>'
	end
	fpl.write '</pre>'
	fpl.puts  '\',  FADEIN, 500, FADEOUT, 500)" onmouseout="UnTip()">'

	fpl.write '<img src="calendar.png" height="40" width="40" onmouseover="Tip(\''
	#put time and date info here	
	fpl.write '<pre>'
	if !photo.DateTimeOriginal.nil?
		fpl.write 'Orignal Date = ' + photo.DateTimeOriginal.to_s
		fpl.write '<br>'
	end
	if !photo.CreateDate.nil?
		fpl.write 'Create Date = ' + photo.CreateDate.to_s
		fpl.write '<br>'
	end
	fpl.write '</pre>'
	fpl.puts  '\',  FADEIN, 500, FADEOUT, 500)" onmouseout="UnTip()">'

       #end exif stuff

	fpl.puts '</td>'
	fpl.puts '<td>'

	fpl.puts '<div id=''rgc''></div>' 

	fpl.puts '</td>'
	fpl.puts '</tr>'
	fpl.puts '</table>' 

    	fpl.puts '</body>'
  	fpl.puts '</html>'
	fpl.close
end

