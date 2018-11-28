import slmpy
import time
import numpy as np
slm = slmpy.SLMdisplay(isImageLock = True)
resX, resY = slm.getSize()
# We use images twice smaller than the resolution of the slm
ImgResX = resX//2
ImgResY = resY//2
X,Y = np.meshgrid(np.linspace(0,ImgResX,ImgResX),np.linspace(0,ImgResY,ImgResY))
for i in range(100):
   testIMG = np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50+1.0*i/10*np.pi))).astype('uint8')
   slm.updateArray(testIMG)
   time.sleep(0.05)
slm.close()