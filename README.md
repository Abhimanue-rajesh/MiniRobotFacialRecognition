# MiniRobotFacialRecognition

## 1. Installing Face Recognition

1. First we will need to build the wheel for the model 

- 1.1 Check the python version installed in your system 
    ```bash
    python --version 
    ```
- 1.2 Create a virtual environment 
    ```bash
    pip install virtualenv  
    ```
    ```bash
    virtualenv venv
    ```
    - Now you have created a virual environment named venv
- 1.3 If python version is the latest - 3.11
    - Download this repository from git hub
    - https://github.com/z-mahmud22/Dlib_Windows_Python3.x
    - Extract the files and copy this file - dlib-19.24.1-cp311-cp311-win_amd64.whl
    - Move the file to the root directory 
    - Run this command
    ```bash
    python -m pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
    ```
- 1.4 Then install the face recoginition 
    ```bash
    pip install face_recognition 
    ```
