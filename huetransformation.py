import cv2
import numpy as np
import copy
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
    return np.array((hueimg+rotation*sensibility)%180,np.uint8)  #Processed according sensibility


    #secondhuetarget = huetarget+180(huetarget<90)-180(huetarget>90)
    #sensibility[Imagerighthue+secondhuetarget]=sensibility[Imagerighthue]
    #sensibility[Imagelefthue+secondhuetarget]=sensibility[Imagelefthue]
    #sensibility[Imagecenter+secondhuetarget]=sensibility[Imagecenter]
def maping(x,xmin,xmax,ymin,ymax):
    return (ymax-ymin)/(xmax-xmin)*(x-xmin)+ymin
def huelinear(rgbimage,rotation,huetarget,sustain,decay):
    #preparing image
    hsvimage = cv2.cvtColor(rgbimage, cv2.COLOR_BGR2HSV)
    #Key Points 
    Di = huetarget-sustain-decay #Decay init
    Si=huetarget-sustain#Sustain init
    Sf = huetarget+sustain
    Df = huetarget+sustain+decay
    #Image preparing 
    hueimg = hsvimage[:,:,0]
    hueimg = hueimg.astype(np.float32)
    #hueimg= hueimg.astype(np.float32)
    Blend= np.zeros(hueimg.shape, dtype=np.float32)
    #Take interest regions 
    RegionLeft = hueimg>=Di
    RegionCenterLeft = hueimg<=Si
    RegionCenterRight = hueimg>=Sf
    RegionRight = hueimg<=Df
    #Created range regions
    AffectedSpace = np.logical_and(RegionLeft,RegionRight)
    Sustain =  np.logical_and(hueimg>=Si,hueimg<=Sf)
    DecayLeftSpace = np.logical_and(RegionLeft,RegionCenterLeft)
    DecayRightSpace = np.logical_and(RegionCenterRight,RegionRight)
    #Created new image without smooth 
    hueImgNotSmooth = copy.deepcopy(hueimg)
    hueImgNotSmooth[AffectedSpace] = (hueImgNotSmooth[AffectedSpace]+rotation)%180
    #Created new image with smooth 
    Blend[DecayLeftSpace] = (hueimg[DecayLeftSpace]-Di)/(Si-Di)
    Blend[DecayRightSpace] = (hueimg[DecayRightSpace]-Df)/(Sf-Df)
    Blend[Sustain] = 1
   # hueImgNotSmooth = hueImgNotSmooth*Blend+hueimg*(1-Blend)
    hsvimage[:,:,0] = hueImgNotSmooth
    framergbNotSmooth = cv2.cvtColor(hsvimage, cv2.COLOR_HSV2BGR)
    framergbSmooth = np.zeros(rgbimage.shape, dtype=np.float32)
    framergbSmooth[:,:,0]=  framergbNotSmooth[:,:,0]*Blend+rgbimage[:,:,0]*(1-Blend)
    framergbSmooth[:,:,1]=  framergbNotSmooth[:,:,1]*Blend+rgbimage[:,:,1]*(1-Blend)
    framergbSmooth[:,:,2]=  framergbNotSmooth[:,:,2]*Blend+rgbimage[:,:,2]*(1-Blend)

    return np.array(framergbSmooth,np.uint8) 


img = cv2.imread('huespace.jpg',cv2.IMREAD_COLOR)

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
    framergb=huelinear(img,nowrotation,55,20,20)
    video.write(framergb)

video.release()



        





#cv2.imshow('Example - Show image in window',bgrimg )
#cv2.waitKey(0) # waits until a key is pressed
#cv2.destroyAllWindows() # destroys the window showing image