import face_recognition
import json
import numpy as np
import os
import libcamera
from picamera2 import Picamera2
import cv2
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import RPi.GPIO as GPIO
import time 
import speech_recognition as sr



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

def voice(text):
    tts = gTTS(text, lang='en', slow=True)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    play(audio)

def audio_to_text(filename):
    # initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        transcribed_text = r.recognize_google(audio_data)
        print(transcribed_text)

def record_audio():
    duration = 5 #Time to record audio
    fs = 48000  # Sample rate
    print('Recording Started')
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print('Recording Finished')
    wav.write('output.wav', fs, recording)  # Save the recorded audio to a WAV file
    print('Saving the File')
    audio_to_text('output.wav')
    

def GreetPerson(name):
    full_sentence = f'Hello{name}, nice to meet you!'
    tts = gTTS(text=full_sentence, lang='en', slow=True)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    play(audio)
    voice('What would you like me to do?')
    record_audio()

def RequestLearnPerson():
    tts = gTTS(text="I dont know you yet,I would like to know you!", lang='en')
    print("Run the learn_face.py script to teach the bot a new face.")
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    play(audio)
    pi_camera.stop_preview()
    pi_camera.close()
    check_distance()


def RecognizeFace(image):
    name_encoding_pairs = LoadKnownEncodings()
    print('All known encodings fetched')
    # Separate encodings and names
    known_face_names = [item["name"] for item in name_encoding_pairs]
    known_face_encodings = [np.array(item["encoding"])
                            for item in name_encoding_pairs]

    unknown_image = face_recognition.load_image_file(image)

    try:
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    except Exception as error:
        print("No face detected or :", error)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            GreetPerson(name)
        else:
            print("No matching encoding in the database")
            RequestLearnPerson()


def StartCamera():
    global pi_camera
    
    pi_camera = Picamera2()    
    config = pi_camera.create_preview_configuration()
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    pi_camera.configure(config)
    pi_camera.start(show_preview=True)
    start_time = time.time()  # Record the start time
    try: 
        while True:
            image = pi_camera.capture_image('main')
            image_array = np.array(image)
            rgb_image = cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
            face_location = face_recognition.face_locations(rgb_image)
            if face_location:
                # Reset the timer if a face is detected
                start_time = time.time()
                # Create output directory if it doesn't exist
                output_directory = "captured_faces"
                # To store the captured faces
                os.makedirs(output_directory, exist_ok=True)
                image_path = os.path.join(output_directory, f"detected_face_{len(os.listdir(output_directory)) + 1}.jpg")
                cv2.imwrite(image_path, image_array)
                
                # Pass the image path to the RecognizeFace function
                RecognizeFace(image_path)
            else :
                # Check if 5 seconds have elapsed without detecting a face
                if time.time() - start_time > 5:
                    print("No face detected for 5 seconds. Stopping the camera.")
                    pi_camera.stop_preview()
                    pi_camera.close()
                    check_distance()  # You might want to define this function or replace it with appropriate logic
                    break
    except KeyboardInterrupt:
        pi_camera.close()
 

def check_distance():
    UltraSonicTrig = 16
    UltraSonicEcho = 18

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(UltraSonicTrig, GPIO.OUT)
    GPIO.setup(UltraSonicEcho, GPIO.IN)
    
    while True:
        GPIO.output(UltraSonicTrig, True)
        time.sleep(0.00001)
        GPIO.output(UltraSonicTrig, False)

        pulse_start = time.time()
        pulse_end = time.time()

        while GPIO.input(UltraSonicEcho) == 0:
            pulse_start = time.time()

        while GPIO.input(UltraSonicEcho) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound is approximately 343 meters per second

        # print(f'Distance: {distance:.2f} cm')

        # Check if a person is within 20 cm
        if distance < 20:
            print('Person detected!')
            print('Starting Camera')
            StartCamera()
        else:
            print('No one near!')

        time.sleep(1)

check_distance()
# record_audio()
# StartCamera()