import cv2
import numpy as np
import time

import Calibrate #находим фокусное расстояние
import GetCoordinates #берем фокусное, находим координаты помидора в xyz, возвращаем их двумерным массивом
import FindBestWay #берем этот массив и находим точки передвижения массивом
import TransformToGcode #берем массив точек и переводим в Gcode
#import send_gcode #отправляем код arduino

net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

GetCoordinates.detector()
