import cv2
import numpy as np
import time

import Calibrate_new #находим фокусное расстояние
import ToXYZ #берем фокусное, находим координаты помидора в xyz, возвращаем их двумерным массивом
#import send_gcode #отправляем код arduino
import generator as gen

net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

focus, boxes = Calibrate_new.Calibrate()
arr=[]
for i in range(0, len(boxes)):
    gosha = ToXYZ.ToXYZ(boxes[i][0],boxes[i][1],boxes[i][2], 816.2)
    arr.append(gosha)
#send_gcode.generate_gcode(gosha)
print(arr)
gen.generate_gcode([0,0,0],arr, True)
