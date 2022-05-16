import cv2
import os
from PIL import Image, ImageStat
def Emergency():
    while True:

        print("Your system is facing an error")
        print("Choose one of the following options: stop self driving , keep self driving with flashes on ")
        import pyaudio
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=5)
            print("Recognizing...")
            # convert speech to text
            speech_output = r.recognize_google(audio_data)
            print(speech_output)
        if speech_output == 'stop self-driving' or speech_output == 'stop the car':
            import gtts
            from playsound import playsound
            tts = gtts.gTTS(f"you asked to {speech_output}")
            # tts.write_to_fp("hello.mp3")
            tts.save("hello.mp3")
            playsound("hello.mp3")
            break

        else:
           import gtts
           from playsound import playsound
           tts = gtts.gTTS(f" I did not understand that, I will stop the car ")
           tts.save("hello.mp3")
           playsound("hello.mp3")
           break

i = 0
#duplicate_files = []
pedestrian_tracker_file = 'haarcascade_fullbody.xml'
pedestrian_tracker = cv2.CascadeClassifier(pedestrian_tracker_file)

webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    successful_frame_read, frame = webcam.read()
    grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_tracker.detectMultiScale(grayscaled_frame)
    for (x, y, w, h,) in pedestrians:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 255), 2)
    cv2.imwrite('Frame' + str(i) + '.jpg', frame)
    i += 1
    cv2.imshow('WEBCAM CARS + PEDESTRIAN', frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
    image_folder = r'C:\Users\Lenovo\PycharmProjects\pythonProject\2214-Week 1'
    image_files = [_ for _ in os.listdir(image_folder) if _.endswith('jpg')]
    duplicate_files = []
    for file_org in image_files:
        if not file_org in duplicate_files:
            image_org = Image.open(os.path.join(image_folder, file_org))
            pix_mean1 = ImageStat.Stat(image_org).mean

            for file_check in image_files:
                if file_check != file_org:
                    image_check = Image.open(os.path.join(image_folder, file_check))
                    pix_mean2 = ImageStat.Stat(image_check).mean

                    if pix_mean1 == pix_mean2:
                        duplicate_files.append((file_org))
                        duplicate_files.append((file_check))
        #if not duplicate_files:
         #   print('Empty')
    if duplicate_files:
        print(list(dict.fromkeys(duplicate_files)))
        Emergency()
        break

print("Execution Done ")
webcam.release()
cv2.destroyAllWindows()

