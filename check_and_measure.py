import cv2
import numpy as np
import pyqrcode
import math	

print('import tensorflow')
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.models import load_model
print('tensorflow imported\n')

model_path = './cp.ckpt'
print('load model')
model = load_model(model_path)
print('model loaded\n')

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
center_x = frame.shape[1]//2
center_y = frame.shape[0]//2

img_size = 224

x0 = center_x - img_size//2
x1 = center_x + img_size//2
y0 = center_y - img_size//2
y1 = center_y + img_size//2

ratio = 100

hsv_low = (0,0,0)
hsv_high = (25,255,255)

while(1):
	ret, frame = cap.read()
	
#	qrDetector  = cv2.QRCodeDetector()
#	data, bbox, rectifiedIimage = qrDetector.detectAndDecode(frame)
#	print(data)

	frame_with_rect = cv2.rectangle(frame.copy(),(x0,y0),(x1,y1),(0,255,0),1)
	cv2.imshow('frame', frame_with_rect)
	key = cv2.waitKey(5) & 0xFF
	if key == ord('q'):
		break

	elif key == ord('r'):
		img_trimmed = frame[y0:y1,x0:x1,:]

		img_data_rgb = cv2.cvtColor(img_trimmed,cv2.COLOR_BGR2RGB)
		img_processed = preprocess_input(np.expand_dims(img_data_rgb,axis=0))
		pre = model.predict(img_processed)

		print(pre)
		if pre[0][0] < 0.95:
			cv2.putText(frame, 'Takenoko',
						org=(100,100),
						fontFace=cv2.FONT_HERSHEY_SIMPLEX,
						fontScale=2.0,
						color=(0,0,255),
						thickness=2,
						lineType=cv2.LINE_4)
		else:
			cv2.putText(frame, 'Kinoko',
						org=(100,100),
						fontFace=cv2.FONT_HERSHEY_SIMPLEX,
						fontScale=2.0,
						color=(255,0,0),
						thickness=3,
						lineType=cv2.LINE_4)
			
		cv2.imshow('frame',frame)

		img_temp = frame[y0:y1,x0:x1,:]
		img_trimmed = img_temp.copy()
		img_data_hsv = cv2.cvtColor(img_trimmed,cv2.COLOR_BGR2HSV)

#		ret, img_data_thresh = cv2.threshold(img_data_hsv[:,:,1],0,255,cv2.THRESH_BINARY, cv2.THRESH_OTSU)
		img_data_thresh = cv2.inRange(img_data_hsv,hsv_low,hsv_high)

		img_data_med = cv2.medianBlur(img_data_thresh,5)
		img_data_object = cv2.cvtColor(img_data_med,cv2.COLOR_GRAY2BGR)
		img_data_object[:,:,1:2] = 0

		contours, hierarchy = cv2.findContours(img_data_med, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnt = contours[0]
		qrcode = contours[1]

		rect = cv2.minAreaRect(cnt)
		retval = cv2.contourArea(cnt) 

		qrsqr = cv2.contourArea(qrcode)
		l_unit = math.sqrt(qrsqr) / 0.8

		width = str(round(min(rect[1])/l_unit,1)) + 'cm'
		length = str(round(max(rect[1])/l_unit,1)) + 'cm'
		square = str(round(retval/qrsqr,1)) + 'cm^2'

		text1 = 'W: ' + width + ' L: ' + length
		text2 = 'S: ' + square
		
		print(text1)
		print(text2)

		cv2.putText(img_trimmed,
					text=text1,
					org=(10,30),
					fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=0.5,
					color=(255,255,0),	
					thickness=1,
					lineType=cv2.LINE_4)
			
		cv2.putText(img_trimmed,
					text=text2,
					org=(10,50),
					fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=0.5,
					color=(255,5,255),	
					thickness=1,
					lineType=cv2.LINE_4)
			
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(img_trimmed,[box],0,(255,0,0),1)
		img_measured = cv2.addWeighted(img_trimmed,0.8,img_data_object,0.3, gamma=0)

		cv2.imshow('subWindow',img_measured)
		key = cv2.waitKey(0) & 0xFF
		if key == ord('q'):
			break
		else:
			pass
	
cap.release()
cv2.destroyAllWindows()
