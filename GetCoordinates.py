def detector(v):
    import cv2
    import numpy as np
    import time

    tomato_size=63

    net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
    classes = []
    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    FinalBox = []
    cap = cv2.VideoCapture(0)
    g=0

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0
    ticker=0
    while ticker<10:
        ticker+=1
        print(ticker)
        _, frame = cap.read()
        frame_id += 1

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if class_id != 3:
                    confidence = scores[class_id]

                if confidence > 0.1:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    g=g+1
                    print(boxes)
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        if ticker == 10:
            ThisBox=boxes
        for i, box in enumerate(boxes):
            x, y, w, h = box
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            confidence = confidences[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)

            FinalBox.append(boxes)

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print(ThisBox)
    for sch in range(0, g-1):
        print(sch)
        x=ThisBox[0][sch]+ThisBox[2][sch]//2
        y=ThisBox[sch][1]
        z=int((tomato_size*v)/ThisBox[sch][2])
        print(x,y,z)
