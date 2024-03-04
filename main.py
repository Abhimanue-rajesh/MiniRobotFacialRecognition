import face_recognition
import json
import numpy as np
from PIL import Image, ImageDraw
import cv2
import os


def LearnNewFace(image, name):
    print("Converting the image to encodings")

    loaded_image = face_recognition.load_image_file(image)
    image_encoding = face_recognition.face_encodings(loaded_image)[0]

    print("Image has been successfully converted to encodings")

    with open("known_faces.json", "r") as read_json_file:
        try:
            data = json.load(read_json_file)
            existing_names = [item["name"] for item in data]
            if name in existing_names:
                print("Name already exists in the JSON file. Skipping addition.")
            else:
                with open("known_faces.json", "w") as write_json_file:
                    data.append(
                        {"name": name, "encoding": list(image_encoding)})
                    json.dump(data, write_json_file, indent=4)
                    print("Encodings with the name is saved to the file")

        except json.JSONDecodeError:
            # Handle empty or invalid JSON file
            print("Existing JSON file is empty or invalid. Creating a new one.")
            data = []  # Initialize as an empty list


def LoadKnownEncodings():
    print("Fetching all the known face encodings from json file")
    # Open the file in read mode
    with open("known_faces.json", "r") as f:
        try:
            data = json.load(f)
            # Return a list of all name-encoding pairs
            return [item for item in data]
        except json.JSONDecodeError:
            print("Error reading JSON file. Returning empty list.")
            return []  # Handle errors by returning an empty list


def RecognizeFace(image):
    name_encoding_pairs = LoadKnownEncodings()

    # Separate encodings and names
    known_face_names = [item["name"] for item in name_encoding_pairs]
    known_face_encodings = [np.array(item["encoding"])
                            for item in name_encoding_pairs]

    # print('Encodings: ',encodings)
    # print('name',names)

    unknown_image = face_recognition.load_image_file(image)

    try:
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(
            unknown_image, face_locations)
    except Exception as error:
        print("No face detected or :", error)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)

        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding
        )
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print("Matching Name", name)
            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        else:
            name = input('Please Enter your Name:')
            LearnNewFace(image, name)


def StartCamera():
    # Define desired window size
    desired_width = 640
    desired_height = 480

    # Define window name
    window_name = "Robot Eyes"

    # Create output directory if it doesn't exist
    output_directory = "captured_faces"
    # To store the captured faces
    os.makedirs(output_directory, exist_ok=True)

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:  # Handle frame read errors
            print("Error reading frame.")
            break

        # Resize the frame (optional, if you want to resize before detection)
        frame = cv2.resize(frame, (desired_width, desired_height))

        # Create or resize the window
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, desired_width, desired_height)

        # Convert the frame from BGR to RGB (as face_recognition uses RGB)
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        image_path = os.path.join(output_directory, f"detected_face_{len(os.listdir(output_directory)) + 1}.jpg")

        if face_locations:
            print("Face Detected at Location:", face_locations)
            for (top, right, bottom, left) in face_locations:
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Extract the face region
                face_image = frame[top:bottom, left:right]
                # Save the detected face image
                cv2.imwrite(image_path, face_image)
                #To recognize the face in the image
                RecognizeFace(image_path)
        
        # Show the resized frame
        cv2.imshow(window_name, frame)

        # Handle key press for quitting
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


StartCamera()
