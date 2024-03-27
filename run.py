import cv2
import numpy as np
import playsound
import smtplib

def playaudio():
    playsound.playsound("alarm-sound.mp3", True)

def send_email_function():
    recepientemail = "Fire engine email address"
    recepientemail = recepientemail.lower()
    try:
        server = smtplib.SMTP('godavarthyram75@gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('jaswanthgodavarthy@gmail.com', 'Bannu@123$')
        server.sendmail('system_email', recepientemail, "Warning!!! A fire accident has been reported")
        print("sent to {}".format(recepientemail))
        server.close()
    except Exception as e:
        print(e)

Fire_Reported = 0
Alarm_Status = False
Email_status = False

# Read the image
image = cv2.imread('test1.jpg')

# Resize the image
image = cv2.resize(image, (1000, 1000))

# Applying blur to the image
blur = cv2.GaussianBlur(image, (15, 15), 0)

# Convert to HSV
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

# Pattern representing the color of the fire
lower = [18, 50, 50]
upper = [35, 255, 255]

lower = np.array(lower, dtype='uint8')
upper = np.array(upper, dtype='uint8')

# Creating the mask
mask = cv2.inRange(hsv, lower, upper)

output = cv2.bitwise_and(image, hsv, mask=mask)

number_of_total = cv2.countNonZero(mask)
# Measuring the size of the fire
if int(number_of_total) > 15000:
    # print("Fire detected")
    Fire_Reported = Fire_Reported + 1

    if Fire_Reported >= 1:
        if Alarm_Status == False:
            playaudio()
            Alarm_Status = True

        # for email
        if Email_status == False:
            send_email_function()
            Email_status = True

# Display the output
cv2.imshow("Output: ", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
