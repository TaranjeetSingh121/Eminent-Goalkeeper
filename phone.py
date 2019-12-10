from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math
import requests
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2
import numpy as np

url = "http://192.168.1.2:8080/shot.jpg"
count = 0
# keep looping
while True:
	url_response = requests.get(url)
	img_array = np.array(bytearray(url_response.content)	, dtype=np.uint8)
	img = cv2.imdecode(img_array, -1)
	cv2.imshow('URL Image', img)
	# cv2.waitKey()
	if cv2.waitKey(1) == "27":
		break