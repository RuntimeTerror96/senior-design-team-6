import numpy as np
import cv2
import threading
import os
from flask import Flask, render_template, Response
from multiprocessing import Process, Manager
from picar import filedb
import time
import datetime



app = Flask(__name__)
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    while True:  

        frame = cv2.imencode('.jpg', Vilib.img_array[0])[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        

@app.route('/mjpg')
def video_feed():
    # from camera import Camera
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

def web_camera_start():
    app.run(host='0.0.0.0', port=8765,threaded=True)


class Vilib(object): 

    video_source = 0
    

    detect_obj_parameter = Manager().dict()
    img_array = Manager().list(range(2))
    rt_img = np.ones((320,240),np.uint8)     
    img_array[0] = rt_img

    @staticmethod
    def camera_start(web_func = True):
        from multiprocessing import Process
       
        worker_2 = Process(name='worker 2',target=Vilib.camera_clone)
        if web_func == True:
            worker_1 = Process(name='worker 1',target=web_camera_start)
            worker_1.start()
        worker_2.start()

    
    @staticmethod
    def camera_clone():
        Vilib.camera()     

    @staticmethod
    def camera():
        db_file = "/home/pi/SunFounder_PiCar-V/remote_control/remote_control/driver/config"
        db = filedb.fileDB(db_file)
        training_mode = int(db.get('training_status', default_value=0)) 

        if training_mode != 1:
            training_mode = 0
            
        camera = cv2.VideoCapture(Vilib.video_source)

        camera.set(3,320)
        camera.set(4,240)
        width = int(camera.get(3))
        height = int(camera.get(4))
        camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
        cv2.setUseOptimized(True)
        i = 0
        while camera.isOpened():
            _, img = camera.read()
            if training_mode == 1:

                usb_path = '/media/pi/ESD-USB/training_data/IMG_'
                fw_status = db.get('fw_status', default_value=0)
                bw_status = db.get('bw_status', default_value=0)
                cv2.imwrite('%s_%d_%s_%s.png' % (usb_path, i, fw_status, bw_status), img)
                i += 1

            Vilib.img_array[0] = img

if __name__ == "__main__":
    Vilib.camera_start()
    while True:
        pass
