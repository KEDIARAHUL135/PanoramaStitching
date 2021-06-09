# PanoramaStitching

This project aims to stitch two images together in the form of a panorama. Code is available in Python and C++.

You can find complete explaination of the logic and documentation of the code [here](https://www.scribd.com/document/510892500/Panorama-Stitching). 


### Installation

Clone this repository and follow the steps below to run the code.

##### Python
* Install the following dependencies.
    * `opencv-python`
    * `numpy`
    * `matplotlib`
* Set the path of the two input images in the file `main.py` at lines 128-129.
* Run the code using terminal
    * Navigate to the cwd.
    * Run: `$ python main.py`
    
#### C++
* Make sure you have OpenCV binaries installed.
* Set the path of the two input images in the file `main.cpp` at lines 172-173.
* Run the file `main.cpp`. For CMake users, `CMakeLists.txt` is also created.
