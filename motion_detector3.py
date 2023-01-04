from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform
import cv2
import numpy as np
from time import sleep
import datetime

THRESHOLD = 1

picam2 = Picamera2()

#picam2.gain = 5
#picam2.exposure_speed = 200000000

#picam2.start_preview(Preview.NULL)

preview_config = picam2.create_preview_configuration(main={"format": 'XBGR8888', "size": (640, 480)})
capture_config = picam2.create_still_configuration(main={"format": 'XBGR8888'})

picam2.configure(capture_config)
#https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
#picam2.set_controls({"ExposureTime":200000000,"AnalogueGain":10})

#night mode:
picam2.set_controls({"ExposureTime":190000000,"AeEnable":False,"AwbEnable":True,"AwbMode":controls.AwbModeEnum.Auto,"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.Fast,"FrameDurationLimits":[1,200000000],"AnalogueGain":20})
THRESHOLD = 7800000

#day mode:
picam2.set_controls({"AeEnable":True,"AwbEnable":True,"AwbMode":controls.AwbModeEnum.Auto,"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.Fast,"AnalogueGain":1})
THRESHOLD = 2000000

#picam2.start()
#picam2.start_preview()

def detectMotion(frame1, frame2):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite('gray1.jpg', gray1)
    cv2.imwrite('gray2.jpg', gray2)

    diff = cv2.absdiff(gray1, gray2)

    now = datetime.datetime.now()
    filename = "pics/" + "prv" +  now.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
    #if(cv2.countNonZero(diff) > 0):
        #print("diff:",diff)

    print("differences:",cv2.countNonZero(diff))

    if(cv2.countNonZero(diff) > THRESHOLD):
        cv2.imwrite(filename, gray1)
        return True
    #else:
    #    print("haha nothing is detected")

    return False

print("should start")
sleep(4)
#picam2.start_preview(Preview.NULL)
#picam2.start()
sleep(4)
while True:
    # Capture a frame from the camera

    picam2.start_preview(Preview.NULL)
    picam2.start()
    #sleep(20)
    #frame1 = picam2.switch_mode_and_capture_array(preview_config, "main")
    frame1 = picam2.capture_array()
    picam2.stop_preview()
    picam2.stop()
    #print("image1 captured")


    #sleep(30)


    picam2.start_preview(Preview.NULL)
    picam2.start()
    #sleep(20)
    #frame2 = picam2.switch_mode_and_capture_array(preview_config, "main")
    frame2 = picam2.capture_array()
    picam2.stop_preview()
    picam2.stop()
    #print("image2 captured")

    f1mean = cv2.mean(frame1)[0]
    print("mean:",f1mean," int:",int(f1mean))
    
    if(f1mean < 4):
        picam2.set_controls({"ExposureTime":190000000,"AeEnable":False,"AwbEnable":True,"AwbMode":controls.AwbModeEnum.Auto,"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.Fast,"FrameDurationLimits":[1,200000000],"AnalogueGain":20})
        THRESHOLD = 7800000

    if(f1mean > 80):
        picam2.set_controls({"AeEnable":True,"AwbEnable":True,"AwbMode":controls.AwbModeEnum.Auto,"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.Fast,"AnalogueGain":1})
        THRESHOLD = 2000000

    # Check for motion
    if detectMotion(frame1, frame2):
        # Motion detected! Do something here (e.g. save the frame, send an email, etc.)
        print("MOTION DETECTED LOL")
        picam2.start_preview(Preview.NULL)
        picam2.start()
        frame = picam2.switch_mode_and_capture_array(capture_config, "main")
        picam2.stop_preview()
        picam2.stop()
        now = datetime.datetime.now()
        filename = "pics/" + "cap" +  now.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        cv2.imwrite(filename, frame)

    sleep(0)
    sleep(0.1)
