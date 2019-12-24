import serial
import time
import argparse


parser = argparse.ArgumentParser(description='Best team POMIDORY')
parser.add_argument('-p','--port',help='Input USB port',required=True)
args = parser.parse_args()

def removeComment(string):
	if (string.find(';')==-1):
		return string
	else:
		return string[:string.index(';')]

def init_com():
	# Wake up 
	s.write("\r\n\r\n".encode()) # Hit enter a few times to wake the Printrbot
	time.sleep(2)   # Wait for Printrbot to initialize
	s.flushInput()  # Flush startup text in serial input
	print ('Sending gcode')

def massive_send(mass_gcode = ['G90;','G28;', 'G1 F600 X100;', 'G1 Y100;', 'G1 Z100;']):
	for element in mass_gcode :
		l = removeComment(element)
		l = l.strip() # Strip all EOL characters for streaming
		if  (l.isspace()==False and len(l)>0) :
			print ('Sending: ' + l)
			s.write((l + '\n').encode()) # Send g-code block
			grbl_out = s.readline() # Wait for response with carriage return
			print(grbl_out)

def check():
	mass_gcode = ['M114;']
	for element in mass_gcode :
		l = removeComment(element)
		l = l.strip() # Strip all EOL characters for streaming
		if  (l.isspace()==False and len(l)>0) :
			print ('Sending: ' + l)
			s.write((l + '\n').encode()) # Send g-code block
			grbl_out = s.readline() # Wait for response with carriage return
			print(grbl_out)
s = serial.Serial(args.port,115200)
init_com()
massive_send()
#time.sleep(2) 
#check();
s.close()