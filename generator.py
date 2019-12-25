def generate_gcode(position, tomato_massive, init):
	if init:
		gcode = ['G90;','G28;', 'G1 F3500 X0;']
	else:
		gcode = []
	tomato_massive.sort(key = lambda i: i[0])

	for tomato in tomato_massive:
		str_X= 'G1 X' + str(tomato[0])+';'
		str_Y = 'G1 Y' + str(tomato[1])+';'
		str_Z = 'G1 Z' + str(tomato[2])+';'
		gcode.append(str_Z);
		gcode.append(str_X);
		gcode.append(str_Y);
	print (gcode)
	return gcode
