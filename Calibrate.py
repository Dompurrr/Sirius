def Calibrate():
    import cv2
    import numpy as np
    import time
    marker_width=38
    distance_to_marker=120

    net = cv2.dnn.readNet("weights/yolov3-tiny_obj_last.weights", "cfg/yolov3-tiny_obj.cfg")
    classes = []
    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cap = cv2.VideoCapture(0)

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    _, frame = cap.read()

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
                confidences.append(float(confidence))
                class_ids.append(class_id)
    for i, box in enumerate(boxes):
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        color = colors[class_ids[i]]
        confidence = confidences[i]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)

    elapsed_time = time.time() - starting_time
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)

    focus=(boxes[0][2]*distance_to_marker)/marker_width
    cap.release()
    cv2.destroyAllWindows()

    return focus
