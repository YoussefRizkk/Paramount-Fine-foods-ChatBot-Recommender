import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt

cascade_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    actions = ['emotion']
    result = DeepFace.analyze(frame, actions)
    gray = cv2.cvtColor(frame, 0)
    detections = cascade_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Our operations on the frame come here
    for (x, y, w, h) in detections:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Setting the font type
        font = cv2.FONT_HERSHEY_DUPLEX

        cv2.putText(frame, result['dominant_emotion'], (75, 75), font, 3, (0, 0, 255), 2, cv2.LINE_4)

        # Display the resulting frame
        cv2.imshow('frame', frame)

    # Press Q to exit the Facial expression Detection
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()