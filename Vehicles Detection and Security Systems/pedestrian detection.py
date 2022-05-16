import cv2

pedestrian_tracker_file = 'haarcascade_fullbody.xml'
pedestrian_tracker = cv2.CascadeClassifier(pedestrian_tracker_file)
'''
webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    successful_frame_read, frame = webcam.read()
    grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_tracker.detectMultiScale(grayscaled_frame)
    for (x, y, w, h,) in pedestrians:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 255), 2)
    cv2.imshow('WEBCAM CARS + PEDESTRIAN', frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

webcam.release()
cv2.destroyAllWindows()
'''
img_file ='crosswalk-featured.png'
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
img = cv2.imread(img_file)
imS = cv2.resize(img, (960, 540))
pedestrian_tracker_file = 'haarcascade_fullbody.xml'
pedestrian_tracker = cv2.CascadeClassifier(pedestrian_tracker_file)


black_n_white = cv2.cvtColor(imS,cv2.COLOR_BGR2GRAY)

cars= pedestrian_tracker.detectMultiScale(black_n_white)
for (x,y,w,h,) in cars:
    cv2.rectangle(imS, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('2214 week one',imS)
cv2.waitKey()
