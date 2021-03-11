import cv2
import numpy as np
np.set_printoptions(threshold=np.inf,suppress=True) #Show all numbers , #None cienfitic notation
from cv2 import VideoWriter, VideoWriter_fourcc

def huerotateall(hsvimage,rotation):
    return (hsvimage[:,:,0]+rotation)%180

def huerotaterange(hsvimage,rotation,huetarget,sustain,decaycoefficient):
    hueimg = hsvimage[:,:,0]
    hueimg= hueimg.astype(np.float32)
    sensibility = np.zeros(hueimg.shape)
    
    RegionLeftHue = hueimg<huetarget-sustain
    RegionCenterHue = np.logical_and(hueimg>=huetarget-sustain, hueimg<=huetarget+sustain)
    RegionRightHue = hueimg>huetarget+sustain
    sensibility[RegionLeftHue]=np.exp(-np.power((hueimg[RegionLeftHue] -huetarget+sustain)/decaycoefficient, 2.))
    sensibility[RegionCenterHue]=1  
    sensibility[RegionRightHue]=np.exp( -np.square((hueimg[RegionRightHue]-sustain-huetarget)/decaycoefficient))
   
    secondhuetarget = huetarget+180(huetarget<90)-180(huetarget>90)
    #sensibility[Imagerighthue+secondhuetarget]=sensibility[Imagerighthue]
    #sensibility[Imagelefthue+secondhuetarget]=sensibility[Imagelefthue]
    #sensibility[Imagecenter+secondhuetarget]=sensibility[Imagecenter]


    return np.array((hueimg+rotation*sensibility)%180,np.uint8)  #Processed according sensibility

img = cv2.imread('frutas.jpg',cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

[height,width] = img[:,:,0].shape
FPS = 12
seconds = 5
totalrotation = 180

nowrotation = 0
rotationrate = totalrotation/(FPS*seconds)

fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./hueTransformation2.avi', fourcc, float(FPS), (width, height))


#print(hsv[:,:,0][1:10,1:1000])
for frame in range(FPS*seconds):
    nowrotation += rotationrate
    #print(nowrotation)
    hsvupdate = hsv.copy()
    hsvupdate[:,:,0]=huerotaterange(hsv,nowrotation,25,15,20)
    #hsvupdate[:,:,0]=huerotateall(hsv,nowrotation)
    #hsvupdate[:,:,0]=(hsv[:,:,0]+nowrotation)%180
    framergb = cv2.cvtColor(hsvupdate, cv2.COLOR_HSV2BGR)
    video.write(framergb)

video.release()



        





#cv2.imshow('Example - Show image in window',bgrimg )
#cv2.waitKey(0) # waits until a key is pressed
#cv2.destroyAllWindows() # destroys the window showing image