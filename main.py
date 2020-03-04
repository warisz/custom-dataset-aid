import numpy as np
import cv2, datetime
import shutil
import os

try:
    shutil.rmtree('./dataset')
    shutil.rmtree('./dataset_train')
except:
    print("No such folder")

os.mkdir('./dataset')
os.mkdir('./dataset_train')

point = [0, 0]
vertical = 100
horizontal = 100

def mouse(event, x, y, flags, param):
    # grab references to the global variables
    global point

    if event == cv2.EVENT_LBUTTONDOWN:
        point = [x, y]

def makeVideo(filename, crop):
    global vertical, horizontal
    '''
    Records video by opening video and accessing webcam.
    Parameters
    ----------
    filename : string
      name of file that the video should be saved as
    crop: boolean
      tells if there should be a rectangle created for image selection
    Returns
    -------
    none
    '''

    # triggering webcam -> 0 is built in camera
    video = cv2.VideoCapture(0)

    # cv2.VideoWriter.open(filename, fourcc, fps, frameSize[, isColor])
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # XVID format is .avi
    out = cv2.VideoWriter('./' + filename + '.avi', fourcc, 20.0, (640, 480))

    counter = 0

    while True:

        # check is a bool telling if it's possible to open cam, frame is a numpy array (FIRST img video captures)
        check, frame = video.read()
        #create rectangle depending on click - adjustment of 2 due to 2px borders
        frame = cv2.rectangle(frame, (point[0]-horizontal-2, point[1]-vertical-2), (point[0]+horizontal+2, point[1]+vertical+2), (255, 0, 0), 2)

        #printing to screen
        cv2.imshow("Video", frame)
        cv2.setMouseCallback("Video", mouse)

        # static until users presses key
        key = cv2.waitKey(1)

        # writing to video
        out.write(frame)
        if key == ord('q'):
            break;

        # SCREEN SIZE
        if key == ord('d'):
            horizontal += 2
        elif key == ord('a'):
            horizontal -= 2
        elif key == ord('w'):
            vertical += 2
        elif key == ord('s'):
            vertical -= 2


        if key == ord('p'):
            croppedImage = frame[(point[1]-vertical):(point[1]+vertical), (point[0]-horizontal):(point[0]+horizontal)] #[y:y+h, x:x+w
            name = "./dataset/" + str(datetime.datetime.now()) + '.jpg'

            cv2.imwrite(name, croppedImage)

            image = cv2.imread(name)
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
            name2 = "./dataset_train/" + str(datetime.datetime.now()) + '.jpg'
            cv2.imwrite(name2, blackAndWhiteImage)



    # close video in some milliseconds
    video.release()
    out.release()
    cv2.destroyAllWindows()


# ----------------SPLITTING VIDEO INTO FRAMES---------------#

def splitVideo(filename):
    '''
    Splits inputted video into frames (images)
    Parameters
    ----------
    filename : string
      name of file that the video should read and split
    Returns
    -------
    none
    '''
    recorded = cv2.VideoCapture('./' + filename + '.avi')

    currentFrame = 0
    while True:
        check, frame = recorded.read()
        name = "./dataset/" + str(datetime.datetime.now()) + '.jpg'

        if check:
            # saving the frame image with filename, frame itself
            cv2.imwrite(name, frame)

            currentFrame += 1
        else:
            break;

    recorded.release()
    cv2.destroyAllWindows()



makeVideo('output1', True)
