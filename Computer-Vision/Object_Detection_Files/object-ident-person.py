import cv2
import numpy as np

'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate

'''
Computer vision
'''
thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        # print(len(classIds))
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    else:
        
        print("no person found")
    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    print("Successfull boot & script launch")

    while True:
        arrPersons = []
        for i in range(0,15):
            success, img = cap.read()
            result, objectInfo = getObjects(img,0.50,0.2, objects=['person'])
            #print(objectInfo)
            peopleCount = len(objectInfo)
            arrPersons.append(peopleCount)
            # print(peopleCount)
            # numPersons = "\nCurrent person count: "+ str(round(np.mean(arrPersons)))
            # UARTdata= bytes(numPersons, 'utf-8')
            # ser.write(UARTdata)
            # cv2.imshow("Output",img)
            cv2.waitKey(1)
        meanPersons = str(np.mean(arrPersons))
        UARTdata= bytes(meanPersons, 'utf-8')
        ser.write(UARTdata)

