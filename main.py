#main.py input.jpg output.jpg sample_count

import cv2
import os
import sys
import numpy as np

filepath = sys.argv[1]
image = cv2.imread(filepath, 3)

imageHeight, imageWidth, _ = image.shape

xChunkProp, yChunkProp = (50, 50)

sampleHeight, sampleWidth = (int(round(imageHeight/yChunkProp)), int(round(imageWidth/xChunkProp)))

def mean_color(sample):
    hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
    channels = np.array_split(hsv, 3, 2)
    hsv = tuple(np.mean(i) for i in channels)
    hsv = [hsv[0], hsv[1]*100/255, hsv[2]*100/255]
    return hsv

samples = []

sampleDir = "samples"
sampleNames = os.listdir(sampleDir)[:int(sys.argv[3])]
for index, i in enumerate(sampleNames):
    try:
        sample = cv2.imread(sampleDir+"/"+i, 3)
        sample = cv2.resize(sample,(sampleWidth,sampleHeight))
        color = mean_color(sample)
        print(index, len(sampleNames))
        samples.append([color, sample])
    except:
        pass

print(len(samples))

height, width, _ = image.shape
strips = np.array_split(image, yChunkProp)
result = None
for strip in strips:
    row = None
    chunks = np.array_split(strip, xChunkProp, 1)
    for chunk in chunks:
        closestMatch = None
        color = mean_color(chunk)
        minDiff = -1
        for i in samples:
            sampleColor, sample = i
            diff = sum((sampleColor[j]-color[j])**2 for j in range(3))
            if closestMatch is None or diff < minDiff:
                minDiff = diff
                closestMatch = sample
        if row is None:
            row = closestMatch
        else:
            row = np.concatenate((row, closestMatch), 1)
    if result is None:
        result = row
    else:
        result = np.concatenate((result, row), 0)

cv2.imwrite(sys.argv[2], result)
