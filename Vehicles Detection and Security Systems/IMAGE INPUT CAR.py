import cv2
img_file = 'Car Image.png'
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
img = cv2.imread(img_file)
imS = cv2.resize(img, (960, 540))
classifier_file = 'cars.xml'
car_tracker = cv2.CascadeClassifier(classifier_file)
black_n_white = cv2.cvtColor(imS,cv2.COLOR_BGR2GRAY)

cars= car_tracker.detectMultiScale(black_n_white)
for (x,y,w,h,) in cars:
    cv2.rectangle(imS, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('2214 week one',imS)
cv2.waitKey()



print('process finished')
