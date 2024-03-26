import cv2
import numpy as np
import playsound
import smtplib

def playaudio():
    playsound.playsound("alarm-sound.mp3",True)

def send_email_function():
    recepientemail = "Fire engine email address"
    recepientemail = recepientemail.lower()
    try:
        server = smtplib.SMTP('godavarthyram75@gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login('jaswanthgodavarthy@gmail.com','Bannu@123$')
        server.sendmail('system_email',recepientemail, "Warning!!! A fire accident has been reported")
        print("sent to {}".format(recepientemail))
        server.close()
    except Exception as e:
        print(e)

Fire_Reported = 0
Alarm_Status = False
Email_status = False

#if you want to turn on your webcam
#video = cv2.VideoCapture(0)

#if you want to give the inbuilt video as input
video = cv2.VideoCapture(0)

#Frame analyzation
while True:
    ret, frame = video.read()

    #resize the output frame
    frame = cv2.resize(frame,(1000,1000))

    #applying blur  to the video
    blur = cv2.GaussianBlur(frame,(15,15),0)

    #convert to hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #pattern representing the color of the fire
    lower = [18,50,50]
    upper = [35,255,255]

    lower = np.array(lower,dtype = 'uint8')
    upper = np.array(upper,dtype = 'uint8')

    #creating the mask
    mask = cv2.inRange(hsv,lower,upper)

    output = cv2.bitwise_and(frame,hsv,mask = mask)

    number_of_total = cv2.countNonZero(mask)
    #measuring the size of the fire
    if int(number_of_total) > 15000:
        #print("Fire detected")
        Fire_Reported = Fire_Reported + 1

        if Fire_Reported >=1:
            if Alarm_Status == False:
                playaudio()
                Alarm_Status = True

            #for email
            if Email_status == False:
                send_email_function()
                Email_status = True


    #if video ends break the sys
    if ret == False:
        break

    #cv2.imshow("Output: ",frame)

    #to outptut the blur
    cv2.imshow("Output: ",output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
video.release()
