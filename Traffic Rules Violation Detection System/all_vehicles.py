"""
 * Built using CHelper plug-in
 * Actual solution is at the top
 *
 * @author Rohit Sharma
 * Last Modified: Dec 12, 2019 11:42:14
"""
import cv2
import dlib
import time
import threading
import math
import helm
carCascade = cv2.CascadeClassifier('cars.xml')
bikeCascade = cv2.CascadeClassifier('motor-v4.xml')
video = cv2.VideoCapture('record.mkv')
# CHANGE VALUE OF LAG TO PRINT THE SPEED ONLY AT SPECIFIC INTERVALS
LAG=7
WIDTH = 1280
HEIGHT = 720
OPTIMISE= 7
"""
Note to reader,

It is not detecting helmet as of now but may be if we use high resolution cameras it will detect helmet
there is no question about yolo detector of helmet it is accurate, problem is in resolution
One proposed solution to overcome the result is to write GPU version of Yolo by myself and then run it 
but i am not sure how it will work along with dlib and haar cascades but it is certainly worth to try
"""
def estimateSpeed(location1, location2,fps):
	d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
	# ppm = location2[2] / carWidht
	ppm = 8.8
	d_meters = d_pixels / ppm
	if fps == 0.0:
		fps = 18
	#fps=18
	#print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
	#fps = 7
	speed = d_meters * fps * 3.6
	return speed
	

def trackMultipleObjects():
	rectangleColor = (0, 255, 0)
	frameCounter = 0
	currentCarID = 0
	currentBikeID=0
	fps = 0
	
	carTracker = {}
	bikeTracker = {}
	bikeNumbers = {}
	carNumbers = {}
	bikeLocation1 = {}
	carLocation1 = {}
	bikeLocation2 = {}
	carLocation2 = {}
	speed = [None] * 1000
	go =[False for i in range(1000)]
	identity = [0 for i in range(1000)]
	snaps = [False for i in range(1000)]
	types = ["cars" for i in range(1000)]
	Helmets = ["No Helmet Detected" for i in range(1000)]
	# Write output to video file
	out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))
	while True:
		start_time = time.time()
		rc, image = video.read()
		if type(image) == type(None):
			break
		
		image = cv2.resize(image, (WIDTH, HEIGHT))
		resultImage = image.copy()
		
		
		frameCounter = frameCounter + 1
		
		carIDtoDelete = []
		for carID in carTracker.keys():
			trackingQuality = carTracker[carID].update(image)
			
			if trackingQuality < 7:
				carIDtoDelete.append(carID)
				
		for carID in carIDtoDelete:
			print ('Removing carID ' + str(carID) + ' from list of trackers.')
			print ('Removing carID ' + str(carID) + ' previous location.')
			print ('Removing carID ' + str(carID) + ' current location.')
			carTracker.pop(carID, None)
			carLocation1.pop(carID, None)
			carLocation2.pop(carID, None)
		
		if not (frameCounter % 10):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
			bikes = bikeCascade.detectMultiScale(gray, 1.1 , 13, 18, (24,24))
			for (_x, _y, _w, _h) in cars:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)
			
				x_bar = x + 0.5 * w
				y_bar = y + 0.5 * h
				
				matchCarID = None
			
				for carID in carTracker.keys():
					trackedPosition = carTracker[carID].get_position()
					
					t_x = int(trackedPosition.left())
					t_y = int(trackedPosition.top())
					t_w = int(trackedPosition.width())
					t_h = int(trackedPosition.height())
					
					t_x_bar = t_x + 0.5 * t_w
					t_y_bar = t_y + 0.5 * t_h
				
					if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
						matchCarID = carID
				
				if matchCarID is None:
					print ('Creating new tracker ' + str(currentCarID))
					
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
					
					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]

					currentCarID = currentCarID + 1
			for (_x, _y, _w, _h) in bikes:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)
			
				x_bar = x + 0.5 * w
				y_bar = y + 0.5 * h
				
				matchCarID = None
			
				for carID in carTracker.keys():
					trackedPosition = carTracker[carID].get_position()
					
					t_x = int(trackedPosition.left())
					t_y = int(trackedPosition.top())
					t_w = int(trackedPosition.width())
					t_h = int(trackedPosition.height())
					
					t_x_bar = t_x + 0.5 * t_w
					t_y_bar = t_y + 0.5 * t_h
				
					if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
						matchCarID = carID
				
				if matchCarID is None:
					print ('Creating new tracker ' + str(currentCarID))
					
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
					
					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]
					types[currentCarID]= "bikes"
					currentCarID = currentCarID + 1
		
		#cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)


		for carID in carTracker.keys():
			trackedPosition = carTracker[carID].get_position()
					
			t_x = int(trackedPosition.left())
			t_y = int(trackedPosition.top())
			t_w = int(trackedPosition.width())
			t_h = int(trackedPosition.height())
			
			#cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)
			
			# speed estimation
			carLocation2[carID] = [t_x, t_y, t_w, t_h]
		
		end_time = time.time()
		fps=0.0
		
		#cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		fm=0
		for i in carLocation1.keys():	
			if frameCounter % 1 == 0:
				[x1, y1, w1, h1] = carLocation1[i]
				[x2, y2, w2, h2] = carLocation2[i]
				#print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
				carLocation1[i] = [x2, y2, w2, h2]

				# print 'new previous location: ' + str(carLocation1[i])
				if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
					#print("Going")
					
				#	if snaps[i] == False:
						#roi = resultImage[y2:y2+h2,x2:x2+w2]
				#		if types[i]=="bikes":
				#			roi = resultImage[y2:y2+h2,x2:x2+w2]
				#			result = helm.detect(roi)
				#		snaps[i]=True
				#		continue
					result = False
					roi = resultImage[y1:y1+h1,x1:x1+w1]
					if types[i]=="bikes" and Helmets[i] == "No Helmet Detected" and identity[i]< OPTIMISE:
				 		result = helm.detect(roi)
					if result==True:
						Helmets[i]= "Helmet Detected"

				#	if y1 >= 275 and y1 <= 285:
					if 7==7:	
						if not (end_time == start_time):
							fps = 1.0/(end_time - start_time)
						speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2],fps)
						#print(str(speed[i]))
					#if y1 > 275 and y1 < 285:
					if int(speed[i])>40:
						speed[i]= speed[i]%40
					if go[i] == True and int(speed[i])<10:
						speed[i]=speed[i]+15
					if int(speed[i])==0:
						continue
					if identity[i]%LAG==0:		
						if int(speed[i])>30:
							go[i]=True
						#if we want to find overspeeding speed just print speed[i]

							cv2.putText(resultImage, "OverSpeeding ALERT", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
						elif speed[i] != None and y1 >= 180 and speed[i]!=0:
							ans= str(int(speed[i])) + " km/hr "
							if types[i]=="bikes":
								ans= ans+ Helmets[i]
							cv2.putText(resultImage, ans, (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
					identity[i]+=1
					#print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

					#else:
					#	cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			fm+=1		

						#print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
		
		cv2.imshow('result', resultImage)
		# Write the frame into the file 'output.avi'
		#out.write(resultImage)
		#print(fm)

		if cv2.waitKey(33) == 27:
			break
	
	cv2.destroyAllWindows()

if __name__ == '__main__':
	trackMultipleObjects()
