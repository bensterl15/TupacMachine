import slmpy
import time
slm = slmpy.SLMdisplay(isImageLock = False)
resX, resY = slm.getSize()
testIMG = np.zeros([resY,resX]).astype('uint8')
t0 = time.time()
for i in range(100):
   slm.updateArray(testIMG)
   print time.time() - t0
slm.close()