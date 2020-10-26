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
        


def StitchImages(BaseImage, SecImage):
    
    
    return StitchedImage


if __name__ == "__main__":
    Images = ReadImage("InputImages/Field")            # Reading all input images

    # Setting the first base image on which the other images will be overlaped
    BaseImage = Images[0]

    for i in range(1, len(Images)):
        StitchedImage = StitchImages(BaseImage, Images[i])

        BaseImage = StitchedImage.copy()