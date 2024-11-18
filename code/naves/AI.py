from naves.config import *

class webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()

    def inicio(self):
        t= Thread(target=self.update,args=())
        t.daemon=True
        t.start()
        return self
    
    def update(self):
        
        if self.stream is None:
            if self.os_name == "Windows":
                self.stream = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            elif self.os_name == 'Darwin':
                self.stream = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else:
                self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)
        while True:
            if self.stopped:
                return
            (resultado,imagen)= self.stream.read()
            if not resultado:
                self.stop()
                return
            self.lastFrame = imagen

    def read(self):
        return self.lastFrame

    def stop(self):
        self.stopped = True
           
    def ancho(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    def alto(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def ready(self):
        return self.lastFrame is not None