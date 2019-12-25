import serial
import time
import argparse


parser = argparse.ArgumentParser(description='Best team POMIDORY')
parser.add_argument('-p','--port',help='Input USB port',required=True)
args = parser.parse_args()
X = 0
Y = 0
Z = 0
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

def massive_send(mass_gcode = ['G90;','G28;', 'G1 F3500 X345;', 'G1 Y50;','G1 Z20;', 'G1 X200;', 'G1 Y367;', 'G1 Z705;', 'G1 X42;']):
	global X
	global Y
	global Z
	for element in mass_gcode :
		if 'G1' in element:
			if element.find('X')!=-1:
				X =int(element[1+element.find('X'):-1])
			if element.find('Y')!=-1:
				Y =int(element[1+element.find('Y'):-1])
			if element.find('Z')!=-1:
				Z =int(element[1+element.find('Z'):-1])
		print(X)
		print(Y)
		print(Z)


		l = removeComment(element)
		l = l.strip() # Strip all EOL characters for streaming
		if  (l.isspace()==False and len(l)>0) :
			print ('Sending: ' + l)
			s.write((l + '\n').encode()) # Send g-code block
			grbl_out = s.readline() # Wait for response with carriage return
			print(grbl_out)

def generate_gcode(position = [0,0,0], tomato_massive = [[100, 200, 300],[200, 210, 350]], init = True):
	if init:
		gcode = ['G90;','G28;', 'G1 F3500 X0;']
	else:
		gcode = []
	tomato_massive.sort(key = lambda i: i[0])
	
	for tomato in tomato_massive:
		for i, coordinate in enumerate(tomato): 
			if i==0:
				str1 = 'G1 X' + str(coordinate)+';'
			if i==1:
				str1 = 'G1 Y' + str(coordinate)+';'
			if i==2:
				str1 = 'G1 Z' + str(coordinate)+';'
			gcode.append(str1);
	print (gcode)
	return gcode

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
gcode = generate_gcode()
massive_send(gcode)
check();
#massive_send(mass_gcode = ['G1 F3500 X545;','G1 Y1100;','G1 Z70;'])
s.close()