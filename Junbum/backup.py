import wx
import numpy
import threading
import time

EVT_NEW_IMAGE = wx.PyEventBinder(wx.NewEventType(), 0)

class ImageWindow(wx.Window):
    def __init__(self, parent, id=-1, style=wx.FULL_REPAINT_ON_RESIZE):
        wx.Window.__init__(self, parent, id, style=style)

        self.timer = wx.Timer

        self.img = wx.EmptyImage(2,2)
        self.bmp = self.img.ConvertToBitmap()
        self.clientSize = self.GetClientSize()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        #For video support
        #------------------------------------------------------------
        self.Bind(EVT_NEW_IMAGE, self.OnNewImage)
        self.eventLock = None
        self.pause = False
        #------------------------------------------------------------

    def OnPaint(self, event):
        size = self.GetClientSize()
        if (size == self.clientSize):
            self.PaintBuffer()
        else:
            self.InitBuffer()

    def PaintBuffer(self):
        dc = wx.PaintDC(self)
        self.Draw(dc)

    def InitBuffer(self):
        self.clientSize = self.GetClientSize()
        self.bmp = self.img.Scale(self.clientSize[0], self.clientSize[1]).ConvertToBitmap()
        dc = wx.ClientDC(self)
        self.Draw(dc)

    def Draw(self,dc):
        dc.DrawBitmap(self.bmp,0,0)

    def UpdateImage(self, img):
        self.img = img
        self.InitBuffer()

    #For video support
    #------------------------------------------------------------
    def OnNewImage(self, event):
        #print sys._getframe().f_code.co_name

        """Update the image from event.img. The eventLock should be
        locked by the method calling the event. If the stream is not
        on pause, the eventLock is released for calling method so that
        new image events may be called.

        The method depends on the use of thread.allocate_lock. The
        event must have the attributes, eventLock and oldImageLock
        which are the lock objects."""

        self.eventLock = event.eventLock

        if not self.pause:
            self.UpdateImage(event.img)
            self.ReleaseEventLock()
        if event.oldImageLock:
            if event.oldImageLock.locked():
                event.oldImageLock.release()

    def ReleaseEventLock(self):
        if self.eventLock:
            if self.eventLock.locked():
                self.eventLock.release()

    def OnPause(self):
        self.pause = not self.pause
        #print "Pause State: " + str(self.pause)
        if not self.pause:
            self.ReleaseEventLock()
    #------------------------------------------------------------

#For video support
#----------------------------------------------------------------------
class ImageEvent(wx.PyCommandEvent):
    def __init__(self, eventType=EVT_NEW_IMAGE.evtType[0], id=0):
        wx.PyCommandEvent.__init__(self, eventType, id)
        self.img = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class ImageFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Image Frame",
                pos=(50,50),size=(640,480))
        self.window = ImageWindow(self)
        self.window.SetFocus()

class ImageIn:
    """Interface for sending images to the wx application."""
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        b = arr.copy()
        b.shape = h, w, 1
        bRGB = numpy.concatenate((b,b,b), axis=2)
        data = bRGB.tostring()

        img = wx.ImageFromBuffer(width=w, height=h, dataBuffer=data)

        #Create the event
        event = ImageEvent()
        event.img = img
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        self.parent.AddPendingEvent(event)

class videoThread(threading.Thread):
    """Run the MainLoop as a thread. Access the frame with self.frame."""
    def __init__(self, autoStart=True):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.start_orig = self.start
        self.start = self.start_local
        self.frame = None #to be defined in self.run
        self.lock = threading.Lock()
        self.lock.acquire() #lock until variables are set
        if autoStart:
            self.start() #automatically start thread on init
    def run(self):
        app = wx.PySimpleApp()
        frame = ImageFrame(None)
        frame.SetSize((800, 600))
        frame.Show(True)

        #define frame and release lock
        #The lock is used to make sure that SetData is defined.
        self.frame = frame
        self.lock.release()

        app.MainLoop()

    def start_local(self):
        self.start_orig()
        #After thread has started, wait until the lock is released
        #before returning so that functions get defined.
        self.lock.acquire()

def runVideoThread():
    """MainLoop run as a thread. SetData function is returned."""

    vt = videoThread() #run wx MainLoop as thread
    frame = vt.frame #access to wx Frame
    myImageIn = ImageIn(frame.window) #data interface for image updates
    return myImageIn.SetData

def runVideo(vidSeq):
    """The video sequence function, vidSeq, is run on a separate
    thread to update the GUI. The vidSeq should have one argument for
    SetData."""

    app = wx.PySimpleApp()
    frame = ImageFrame(None)
    frame.SetSize((800, 600))
    frame.Show(True)

    myImageIn = ImageIn(frame.window)
    t = threading.Thread(target=vidSeq, args=(myImageIn.SetData,))
    t.setDaemon(1)
    t.start()

    app.MainLoop()

def runVideoAsThread():
    """THIS FUNCTION WILL FAIL IF WX CHECKS TO SEE THAT IT IS RUN ON
    MAIN THREAD.  This runs the MainLoop in its own thread and returns
    a function SetData that allows write access to the databuffer."""

    app = wx.PySimpleApp()
    frame = ImageFrame(None)
    frame.SetSize((800, 600))
    frame.Show(True)

    myImageIn = ImageIn(frame.window)

    t = threading.Thread(target=app.MainLoop)
    t.setDaemon(1)
    t.start()

    return myImageIn.SetData

def vidSeq(SetData,loop=0):
    """This is a simple test of the video interface. A 16x16 image is
    created with a sweep of white pixels across each row."""

    w,h = 16,16
    arr = numpy.zeros((h,w), dtype=numpy.uint8)
    i = 0
    m = 0
    while m < loop or loop==0:
        print i
        arr[i/h,i%w] = 255
        h,w = arr.shape
        SetData(arr)
        time.sleep(0.1)
        i += 1
        if not (i < w*h):
            arr = numpy.zeros((h,w), dtype=numpy.uint8)
            i = 0
            m += 1

if __name__ == '__main__':

    if 1:
        #Method 1:
        runVideo(vidSeq)

    if 0:
        #Method 2:
        SetData = runVideoAsThread()
        vidSeq(SetData, loop=1)

    if 0:
        #Method 3:
        SetData = runVideoThread()
        vidSeq(SetData, loop=1)