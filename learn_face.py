import face_recognition
import json
from picamera2 import Picamera2
import cv2
import os
import libcamera
import numpy as np


def LearnNewFace(image, name):
    with open("known_faces.json", "r") as read_json_file:
        try:
            data = json.load(read_json_file)
            existing_names = [item["name"] for item in data]
            if name in existing_names:
                print("Name already exists in the JSON file. Skipping addition.")
            else:
                print("Converting the image to encodings")
                loaded_image = face_recognition.load_image_file(image)
                image_encoding = face_recognition.face_encodings(loaded_image)[0]
                print("Image has been successfully converted to encodings")
                with open("known_faces.json", "w") as write_json_file:
                    data.append(
                        {"name": name, "encoding": list(image_encoding)})
                    json.dump(data, write_json_file, indent=4)
                    print("Encodings with the name is saved to the file")

        except json.JSONDecodeError:
            # Handle empty or invalid JSON file
            print("Existing JSON file is empty or invalid. Creating a new one.")
            data = []  # Initialize as an empty list

def StartCamera():
    pi_camera = Picamera2()    
    config = pi_camera.create_preview_configuration()
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    pi_camera.configure(config)
    pi_camera.start(show_preview=True)
    ran_once = False
    while ran_once == False:
        image = pi_camera.capture_image('main')
        image_array = np.array(image)
        rgb_image = cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        face_location = face_recognition.face_locations(rgb_image)
        print('Face Location:', face_location)
        if face_location:
            # Create output directory if it doesn't exist
            output_directory = "captured_faces"
            # To store the captured faces
            os.makedirs(output_directory, exist_ok=True)
            image_path = os.path.join(output_directory, f"detected_face_{len(os.listdir(output_directory)) + 1}.jpg")
            cv2.imwrite(image_path, image_array)
            
            name = input("Enter the name of the person: ")
            # Pass the image path to the RecognizeFace function
            LearnNewFace(image_path, name)
            ran_once = True

StartCamera()