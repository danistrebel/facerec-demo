import face_recognition
import cv2
import os
import glob
import logging


logging.basicConfig(level=logging.INFO)

# Facerecognition based on example:
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py

def run_face_recognition():

    known_face_encodings = []
    known_face_names = []

    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    initial_files = glob.glob(images_dir + "/*.jpg")

    for initial_file in initial_files:
        image_name = " ".join(os.path.splitext(os.path.basename(initial_file))[0].split("_"))
        logging.info('Adding: ' + image_name)
        image = face_recognition.load_image_file(initial_file)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(image_name)

    # Standard webcam input
    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            frame_color = (255, 0, 0) if name.startswith("TEAM") else (0, 0, 255)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), frame_color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), frame_color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.namedWindow("Face Recognizer", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Face Recognizer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Face Recognizer", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_recognition()