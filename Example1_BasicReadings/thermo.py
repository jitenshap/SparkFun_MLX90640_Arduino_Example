import cv2 as cv
import numpy as np
import pandas as pd
import serial
import sys
import io

twidth = 32
theight = 24
width = 800
height = 600

i=0
j=0

picnum=0;

ser = serial.Serial('COM7',921600,timeout=2)
debug = ser.read(10000)
print (debug)

count=0
while True:
    img = np.zeros((height, width, 3), np.uint8)
    buffer = ""
    i=0
    ser.write("get;".encode('utf-8'))
    for i in range(theight+1):
        line = ser.readline()
        print (line)
        buffer = buffer + line.decode('utf-8')

    data = io.StringIO(buffer)
    temp = pd.read_csv(data, header=None)

    i=0
    j=0
    for i in range(twidth):
        for j in range(theight):
            xposf = i * width / twidth
            yposf = j * height / theight
            xpos = int(xposf)
            ypos = int(yposf)
            wf = i * width / twidth + width / twidth
            hf = j*height / theight + height / theight
            w = int(wf)
            h = int(hf)
            tempBuf = temp[i][j]
            rf = (tempBuf  / 40) * 255
            gf = (tempBuf / 40) * 255
            bf = (tempBuf / 40) * 255
            r = int(rf)
            g = int(gf)
            b = int(bf)
            img = cv.rectangle(img, (xpos, ypos), (w, h), (r, g, b), -1, cv.LINE_AA)
    img = cv.GaussianBlur(img,(33,33), 30)        
    for i in range(twidth):
        for j in range(theight):
            tempBuf = temp[i][j]
            textxf = (i * width / twidth) + (width / (twidth * 2)) - 12
            textyf = (j * height / theight) + (height / ( theight * 2 ) )
            textx = int(textxf)
            texty = int(textyf)
            cv.putText(img, "{0:.1f}".format(tempBuf), (textx, texty), cv.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv.LINE_AA)

    #cv.imwrite('thermo'+str(picnum)+'.jpg', img) 
    cv.imshow('result', img)
    cv.waitKey(1)
    picnum = picnum + 1

cv.destroyAllWindows()
ser.close()