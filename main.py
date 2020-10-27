import os
import cv2
import numpy as np
from matplotlib import pyplot as plt



def ReadImage(InputImagePath):
    Images = []                     # Input Images will be stored in this list.
    
	# If path is of a folder contaning images.
    if os.path.isdir(InputImagePath):
		# Getting the number of images present.
        NumOfImgs = len(os.listdir(InputImagePath))

        if NumOfImgs < 2:
            print("\nSufficient number of images not found.\nProvide atleast 2 images.\n")
            exit()

        # Getting file extention (All image files must have same extention)
        ext = os.path.splitext(os.listdir(InputImagePath)[0])[1]

        for i in range(1, NumOfImgs+1):
			# Reading images one by one.
            InputImage = cv2.imread(InputImagePath + "/" + str(i) + ext)
			
            Images.append(InputImage)							# Storing images.
        
    # If it is not a folder.
    else:
        print("\nEnter valid Image Folder Path.\n")
        exit()

    return Images
        

def FindMatches(BaseImage, SecImage):
    Sift = cv2.SIFT_create()
    BaseImage_kp, BaseImage_des = Sift.detectAndCompute(cv2.cvtColor(BaseImage, cv2.COLOR_BGR2GRAY), None)
    SecImage_kp, SecImage_des = Sift.detectAndCompute(cv2.cvtColor(SecImage, cv2.COLOR_BGR2GRAY), None)

    BF_Matcher = cv2.BFMatcher()
    InitialMatches = BF_Matcher.knnMatch(BaseImage_des, SecImage_des, k=2)

    GoodMatches = []
    for m, n in InitialMatches:
        if m.distance < 0.75 * n.distance:
            GoodMatches.append([m])

    return GoodMatches, BaseImage_kp, SecImage_kp


   
def StitchImages(BaseImage, SecImage):
    Matches, BaseImage_kp, SecImage_kp = FindMatches(BaseImage, SecImage)


    return StitchedImage


if __name__ == "__main__":
    Images = ReadImage("InputImages/Sun")            # Reading all input images

    # Setting the first base image on which the other images will be overlaped
    BaseImage = Images[0]

    for i in range(1, len(Images)):
        StitchedImage = StitchImages(BaseImage, Images[i])

        BaseImage = StitchedImage.copy()