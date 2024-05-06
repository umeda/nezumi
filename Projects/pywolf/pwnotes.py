'''

https://aprs-python.readthedocs.io/en/stable/parse_formats.html
https://en.wikipedia.org/wiki/KISS_(amateur_radio_protocol)
http://www.aprs.org/doc/APRS101.PDF

This is now KISS protocol.

(.venv) tester@b360:~/nezumi/Projects/pywolf$ pip3 install kiss
Collecting kiss
  Using cached kiss-7.0.0.tar.gz (7.9 kB)
    ERROR: Command errored out with exit status 1:
     command: /home/tester/nezumi/Projects/pywolf/.venv/bin/python3 -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-b6rgzvf9/kiss/setup.py'"'"'; __file__='"'"'/tmp/pip-install-b6rgzvf9/kiss/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-install-b6rgzvf9/kiss/pip-egg-info
         cwd: /tmp/pip-install-b6rgzvf9/kiss/
    Complete output (45 lines):
    WARNING: The wheel package is not available.
    WARNING: The wheel package is not available.
      ERROR: Command errored out with exit status 1:
       command: /home/tester/nezumi/Projects/pywolf/.venv/bin/python3 -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-wheel-rmu2a0tt/aprs/setup.py'"'"'; __file__='"'"'/tmp/pip-wheel-rmu2a0tt/aprs/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-wz2b9n2h
           cwd: /tmp/pip-wheel-rmu2a0tt/aprs/
      Complete output (6 lines):
      usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
         or: setup.py --help [cmd1 cmd2 ...]
         or: setup.py --help-commands
         or: setup.py cmd --help
    
      error: invalid command 'bdist_wheel'
      ----------------------------------------
      ERROR: Failed building wheel for aprs
    ERROR: Failed to build one or more wheels
    Traceback (most recent call last):
      File "/home/tester/nezumi/Projects/pywolf/.venv/lib/python3.8/site-packages/setuptools/installer.py", line 128, in fetch_build_egg
        subprocess.check_call(cmd)
      File "/usr/lib/python3.8/subprocess.py", line 364, in check_call
        raise CalledProcessError(retcode, cmd)
    subprocess.CalledProcessError: Command '['/home/tester/nezumi/Projects/pywolf/.venv/bin/python3', '-m', 'pip', '--disable-pip-version-check', 'wheel', '--no-deps', '-w', '/tmp/tmpbgvrxwuy', '--quiet', 'aprs>6.9']' returned non-zero exit status 1.

pip install wheel

https://github.com/ampledata/kiss/blob/master/examples/socket_read.py

=====================================================================================================






Digipeater KH6BFD-1 audio level = 62(28/25)   [NONE]   ||||||___
[0.2] KH7O-10>R1QWRU,KH6MP-1,KH6BFD-1*:`UL1mh$>/'"4P}corolla RTG FA|!"&('l|!w.F!|3

MIC-E, normal car (side view), Byonics TinyTrack3, In Service
N 21 17.2514, W 157 48.2141, 20 MPH, course 208, alt 187 ft
Seq=1, A1=462, A2=621
corolla RTG FA

Listening for client...
connecting to: ('localhost', 8001)
received = b'\xc0\x00\xa4b\xa2\xae\xa4\xaa`\x96\x90n\x9e@@t\x96\x90l\x9a\xa0@\xe2\x96\x90l\x84\x8c\x88\xe3\x03\xf0`UL1mh$>/\'"4P}corolla RTG FA|!"&(\'l|!w.F!|3\xc0'

=====================================================================================

Digipeater KH6BFD-1 audio level = 67(39/24)   [NONE]   _|||||___
[0.3] KH6JUZ-12>APDW17,KH6MP-1,KH6BFD-1*:!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA

Position, TX igate with path set to 1 h, DireWolf, WB2OSZ
N 21 35.5000, W 158 06.4400
 Haleiwa North Shore Oahu Hawaii USA
Whole AX.25 frame? 
Received =  b'\xc0\x00\x82\xa0\x88\xaebn\xe0\x96\x90l\x94\xaa\xb4\xf8\x96\x90l\x9a\xa0@\xe2\x96\x90l\x84\x8c\x88\xe3\x03\xf0!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA\xc0'
                                                                                                                                         

'''
import aprslib
import chardet
import kiss
import aprs

Received = b'\xc0\x00\x82\xa0\x88\xaebn\xe0\x96\x90l\x94\xaa\xb4\xf8\x96\x90l\x9a\xa0@\xe2\x96\x90l\x84\x8c\x88\xe3\x03\xf0!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA\xc0'
Received = b'\x00\x82\xa0\x88\xaebn\xe0\x96\x90l\x94\xaa\xb4\xf8\x96\x90l\x9a\xa0@\xe2\x96\x90l\x84\x8c\x88\xe3\x03\xf0!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA'
Received = b'\x82\xa0\x88\xaebn\xe0\x96\x90l\x94\xaa\xb4\xf8\x96\x90l\x9a\xa0@\xe2\x96\x90l\x84\x8c\x88\xe3\x03\xf0!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA'
Received = b'\x82\xa0\x82\xa8jb\xf2\x96\x90l\x84\x8c\x88r\x96\x90l\x84\x8c\x88\xe2\xae\x92\x88\x8ad@c\x03\xf0!1936.85N/15557.92Wv327/000/A=000485 KH6BFD'

# print(chardet.detect(Received))
# print(aprslib.parse(Received))

'''
pw
b'\xc0\x00\x82\xa0\x82\xa8jb\xf2\x96\x90l\x84\x8c\x88r\x96\x90l\x84\x8c\x88\xe2\xae\x92\x88\x8ad@c\x03\xf0!1936.85N/15557.92Wv327/000/A=000492 KH6BFD\xc0'
b'\x82\xa0\x82\xa8jb\xf2\x96\x90l\x84\x8c\x88r\x96\x90l\x84\x8c\x88\xe2\xae\x92\x88\x8ad@c\x03\xf0!1936.85N/15557.92Wv327/000/A=000492 KH6BFD\xc0'
pw2
b'\x82\xa0\x82\xa8jb\xf2\x96\x90l\x84\x8c\x88r\x96\x90l\x84\x8c\x88\xe2\xae\x92\x88\x8ad@c\x03\xf0!1936.85N/15557.92Wv327/000/A=000485 KH6BFD'
'''
# print(aprs.parse_callsign(Received))
# print(aprs.parse_callsign_ax25(Received))
# print(aprs.parse_frame(Received))
# print(aprs.parse_info_field(Received))

pos = 'KH6BFD-9>APAT51-9,KH6BFD-1*,WIDE2-1:!1936.85N/15557.92Wv327/000/A=000482 KH6BFD'
pos = str(aprs.parse_frame(Received))
print(pos)

#get rid of *
# pos = 'KH6JUZ-12*>APDW17*,KH6MP-1*,KH6BFD-1*:!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA'
# pos = 'KH6JUZ-12>APDW17,KH6MP-1,KH6BFD-1:!2135.50NT15806.44W& Haleiwa North Shore Oahu Hawaii USA'
print(aprslib.parse(pos))
# print(aprslib.parse(Received))

#reverse geocode!

'''
https://api.3geonames.org/21.591666666666665,-158.10733333333334
https://www.bigdatacloud.com/free-api/free-reverse-geocode-to-city-api
'''