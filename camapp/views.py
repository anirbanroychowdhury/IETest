from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from camapp.camera import *
from camapp.process import *
from django.views.decorators.csrf import csrf_exempt
import cv2 as cv2
import dlib
import base64
from scipy.spatial import distance as dist
import numpy as np
from PIL import Image
from threading import Thread
import time
from django.core.files.base import ContentFile
import io

camera = Camera(webopencv())


def index_view(request, *args, **kwargs):
    """Video streaming home page."""
 
    return render(request,'index.html',{'image':""})


def gen(camera):
    """Video streaming generator function."""

    # app.logger.info("starting to generate frames!")
    print("Starting to generate frames")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@csrf_exempt
def video_feed(request, *args, **kwargs):
    if request.method == 'POST':
        # print(request.body)
        _format, _data = str(request.body).split(';base64,')
        file = ContentFile( base64.b64decode(_data))
        img = Image.open(file)
        camera.enqueue_input(img)
        camera_frame = camera.get_frame()
        # frame = np.array(camera_frame)
        # grayFrame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2GRAY)
        # faces = detector(grayFrame,0)
        # for face in faces:
        #     shape = predictor(grayFrame,face)
        #     shape = shape_to_np(shape)
        #     #Extract left and right eye using defined coordinates
        #     leftEye = shape[lStart:lEnd]
        #     rightEye = shape[rStart:rEnd]
        #     #Get eye aspect ratio(EAR)
        #     leftEAR = eye_aspect_ratio(leftEye)
        #     rightEAR = eye_aspect_ratio(rightEye)
        #     #Get avg eye aspect ratio
        #     avgEAR = float((leftEAR+rightEAR)/2.0)
        #     #compute convex hull
        #     leftEyeHull = cv2.convexHull(leftEye)
        #     rightEyeHull = cv2.convexHull(rightEye)
        #     #Visualize each eye
        #     cv2.drawContours(frame,[leftEyeHull], -1, (0,255,0), 1)
        #     cv2.drawContours(frame,[rightEyeHull], -1, (0,255,0), 1)
        #     if avgEAR < EYE_AR_THRESH:
        #         COUNTER += 1
        #         if COUNTER >= EYE_AR_CONSEC_FRAMES:
        #             print(COUNTER)
        #             cv2.putText(frame,'ALERT!!!',(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1) 
        #     else:
        #         COUNTER = 0
        #     #Add text showing ratio
        #     cv2.putText(frame,"EAR: {:.2f}".format(avgEAR), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # ret, jpeg = cv2.imencode('.jpg',frame)
        # jpeg_b64 = base64.b64encode(jpeg)
        return HttpResponse(camera_frame)
        