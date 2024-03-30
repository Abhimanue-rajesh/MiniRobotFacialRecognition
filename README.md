<h1 align="center">MiniRobotFacialRecognition</h1>


This mini robot capable of facial recognition and executing user commands. The robot utilizes various technologies such as face recognition, speech synthesis and recognition, audio recording and processing, and GPIO interfacing for distance sensing.

## Key Components

### Facial Recognition: 

- The robot can detect and recognize human faces using the face_recognition library. It compares detected faces with known face encodings stored in a JSON file (known_faces.json). If a match is found, it greets the person. If not, it prompts the user to teach the robot the new face.

### Speech Synthesis: 
- Utilizing the gTTS (Google Text-to-Speech) library, the robot can convert text messages into speech. It uses this capability to greet individuals and prompt user interactions.

### Speech Recognition: 
- The robot can transcribe spoken commands into text using the speech_recognition library. This functionality enables users to give commands to the robot verbally.

### Audio Recording and Processing: 
- The robot can record audio using the sounddevice library, save it as a WAV file, and transcribe it to text. This feature allows for verbal interactions and command input.

### Camera Interaction: 
- The robot employs a camera (Picamera2) to capture images for facial recognition. It continuously monitors for faces, capturing images when detected.

### GPIO Interfacing for Distance Sensing: 
- The robot utilizes GPIO pins on a Raspberry Pi to interface with an ultrasonic distance sensor. It measures distances to detect the presence of individuals nearby. When someone is detected within a certain range, it triggers the facial recognition and interaction processes.

## Code Structure

- The code is structured into functions, each responsible for specific tasks:

- LoadKnownEncodings: Loads known face encodings from a JSON file.
- voice: Converts text to speech and plays the audio.
- audio_to_text: Transcribes audio files to text using Google's speech recognition API.
- record_audio: Records audio for a specified duration and saves it to a WAV file.
- GreetPerson: Greets a recognized person and prompts for user interaction.
- RequestLearnPerson: Requests to learn a new face if an unrecognized person is detected.
- RecognizeFace: Performs facial recognition on captured images and triggers appropriate actions based on the result.
- StartCamera: Initializes the camera and continuously captures images for face detection and recognition.
- check_distance: Monitors distance using an ultrasonic sensor and initiates face recognition when someone is within range.
- The main functionality is triggered by calling check_distance, which initiates the robot's operation by monitoring for nearby - individuals. Once someone is detected within a specified range, the robot starts the facial recognition process.

## Interaction Flow

- The robot monitors for nearby individuals using the ultrasonic sensor.
- When someone is detected within range, the camera captures their image.
- Facial recognition is performed on the captured image.
- If the person is recognized, the robot greets them and awaits user commands.
- If the person is not recognized, the robot requests to learn the new face.
- Users can interact with the robot verbally by giving commands.
- The robot executes the commands and communicates with other components, potentially including an Arduino for further actions.