# Raspberry Pi Motion Detection Sentry
A very basic Python program that uses the raspberry pi camera , the picamera2 library, libcamera and opencv2 to detect motion and capture images of possible intruders.

Also includes a night mode that switches on and off automatically.

Usage: 

- install opencv using your preferred method

- install the picamera2 library

- run program

- tweak thresholds and exposure settings if needed (may differ based on your camera module and lighting conditions)

if it detects motion it will capture an image of the intruder and save it in a folder called "pics" (if it throws an error you might have to create the folder manually, next to the python file)

!check console for threshold values and exposure values!
