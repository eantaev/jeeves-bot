import time
from datetime import datetime

try:
    import picamera
except ImportError:
    pass


def take_photo():
    if picamera:
        with picamera.PiCamera() as cam:
            cam.vflip = True
            cam.hflip = True
            cam.start_preview()
            time.sleep(0)
            now = datetime.utcnow()
            image_file = './images/%s.jpg' % now.strftime('%Y%m%dT%H%M%S')
            cam.capture(image_file)
            cam.stop_preview()
            return image_file
    else:
        return None
