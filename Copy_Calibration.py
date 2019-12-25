def detector():
    import cv2
    import numpy as np
    import time

    focus = 816.2
    tomato_size=60

    net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
    classes = []
    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cap = cv2.VideoCapture(1)
    g=0

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0
    boxes = []
    class_ids = []
    mid_w = []
    GoNext = []
    while True:
        _, frame = cap.read()
        frame_id += 1
        numOfTomatoes=0

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        confidences = []
        if frame_id%10 == 0:
            boxes = []
            class_ids = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if class_id != 3:
                    confidence = scores[class_id]

                if confidence > 0.1 and frame_id%10 == 0:
                    # Object detected
                    numOfTomatoes=numOfTomatoes+1
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    if frame_id == 10:
                        mid_w.append(w)
                    else:
                        mid_w[numOfTomatoes-1] = (mid_w[numOfTomatoes-1] + w) // 2

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    distance = int(tomato_size*focus/mid_w[numOfTomatoes-1])

                    boxes.append([x, y, w, h, distance])
                    #print(boxes)
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        for i, box in enumerate(boxes):
            x, y, w, h, distance = box
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(distance), (x, y + 30), font, 2, color, 3)
            if frame_id == 50:
                GoNext.append([x,y,distance])
                print(GoNext)
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if frame_id==300:
            return
    cap.release()
    cv2.destroyAllWindows()
detector()
