import time
import argparse
import serial
import cv2
import numpy as np

import ToXYZ
import Calibrate_new

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

net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

def init_com():
	# Wake up
	s.write("\r\n\r\n".encode()) # Hit enter a few times to wake the Printrbot
	time.sleep(2)   # Wait for Printrbot to initialize
	s.flushInput()  # Flush startup text in serial input
	print ('Sending gcode')

def massive_send(mass_gcode):
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

def generate_gcode(position = [0,0,0], tomato_massive = [[385, 585, 113]], init = True):
	if init:
		gcode = ['G90;','G28;', 'G1 F3500 X0;']
	else:
		gcode = []
	tomato_massive.sort(key = lambda i: i[0])

	for tomato in tomato_massive:
		str_X= 'G1 X' + str(tomato[0])+';'
		str_Y = 'G1 Y' + str(tomato[1])+';'
		str_Z = 'G1 Z' + str(tomato[2])+';'
		str_end = 'G1 Y350;'
		gcode.append(str_Z);
		gcode.append(str_X);
		gcode.append(str_Y);
		gcode.append(str_end);
		gcode.append('')
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

focus, boxes = Calibrate_new.Calibrate()
arr=[]
for i in range(0, len(boxes)):
    gosha = ToXYZ.ToXYZ(boxes[i][0],boxes[i][1],boxes[i][2], 816.2)
    arr.append(gosha)
print(arr)
s = serial.Serial(args.port,115200)
init_com()
gcode = generate_gcode([0,0,0],arr, True)
print(gcode)
massive_send(gcode)
check()
s.close()
