import cv2 
import os
import numpy as np 

cap = cv2.VideoCapture(0)
coins = cv2.imread("coin.jpg")
while(True):
	ret , frame = cap.read()
	#動画読み込みをして2値変換
	frame_gs = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	frame_gs_blur = cv2.GaussianBlur(frame_gs,(25,25),0)
	_, frame_binary = cv2.threshold(frame_gs_blur,130,255,cv2.THRESH_BINARY)
	frame_binary = cv2.bitwise_not(frame_binary)
	

	#境界線を見つける
	_, weight_contours , _ = cv2.findContours(frame_binary, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
	weights_and_contours = np.copy(frame)

	max_weight_area = 100000
	min_weight_area = 300
	weight_area = [cnt for cnt in weight_contours if min_weight_area < cv2.contourArea(cnt) and cv2.contourArea(cnt) < max_weight_area]

	cv2.drawContours(weights_and_contours,weight_area,-1,(0,0,255))
	bounding_img = np.copy(weights_and_contours)

	for contour in weight_area:
		x,y,w,h = cv2.boundingRect(contour)
		cv2.rectangle(bounding_img,(x,y),(x+w,y+h),(0,255,0),10)

 

	cv2.imshow("furiko",bounding_img)

	k = cv2.waitKey(100)
	if k == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()