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



def FindHomography(Matches, BaseImage_kp, SecImage_kp):
    if len(Matches) < 4:
        print("\nNot enough matches found between the images.\n")
        exit(0)

    BaseImage_pts = []
    SecImage_pts = []
    for Match in Matches:
        BaseImage_pts.append(BaseImage_kp[Match[0].queryIdx].pt)
        SecImage_pts.append(SecImage_kp[Match[0].trainIdx].pt)

    BaseImage_pts = np.float32(BaseImage_pts)
    SecImage_pts = np.float32(SecImage_pts)

    (HomographyMatrix, Status) = cv2.findHomography(SecImage_pts, BaseImage_pts, cv2.RANSAC, 4.0)

    return HomographyMatrix, Status

    
def GetNewFrameSizeAndMatrix(HomographyMatrix, ImageShape):
    (Height, Width) = ImageShape
    
    InitialMatrix = np.array([[0, Width - 1, Width - 1, 0],
                              [0, 0, Height - 1, Height - 1],
                              [1, 1, 1, 1]])
    
    FinalMatrix = np.dot(HomographyMatrix, InitialMatrix)

    [x, y, c] = FinalMatrix
    x = np.divide(x, c)
    y = np.divide(y, c)

    min_x, max_x = int(round(min(x))), int(round(max(x)))
    min_y, max_y = int(round(min(y))), int(round(max(y)))

    New_Width = max_x
    New_Height = max_y
    Correction = [0, 0]
    if min_x < 0:
        New_Width -= min_x
        Correction[0] = abs(min_x)
    if min_y < 0:
        New_Height -= min_y
        Correction[1] = abs(min_y)
    
    x = np.add(x, Correction[0])
    y = np.add(y, Correction[1])
    OldInitialPoints = np.float32([[0, 0],
                                   [Width - 1, 0],
                                   [Width - 1, Height - 1],
                                   [0, Height - 1]])
    NewFinalPonts = np.float32(np.array([x, y]).transpose())
    
    HomographyMatrix = cv2.getPerspectiveTransform(OldInitialPoints, NewFinalPonts)
    
    return [New_Height, New_Width], Correction, HomographyMatrix



def StitchImages(BaseImage, SecImage):
    Matches, BaseImage_kp, SecImage_kp = FindMatches(BaseImage, SecImage)
    
    HomographyMatrix, Status = FindHomography(Matches, BaseImage_kp, SecImage_kp)
    
    NewFrameSize, Correction, HomographyMatrix = GetNewFrameSizeAndMatrix(HomographyMatrix, SecImage.shape[:2])

    StitchedImage = cv2.warpPerspective(SecImage, HomographyMatrix, (SecImage.shape[1] + BaseImage.shape[1], SecImage.shape[0]))

    StitchedImage[0:BaseImage.shape[0], 0:BaseImage.shape[1]] = BaseImage

    return StitchedImage


if __name__ == "__main__":
    Images = ReadImage("InputImages/Sun")            # Reading all input images

    # Setting the first base image on which the other images will be overlaped
    BaseImage = Images[0]

    for i in range(1, len(Images)):
        StitchedImage = StitchImages(BaseImage, Images[i])

        BaseImage = StitchedImage.copy()