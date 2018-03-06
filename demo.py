from faceadd import run_face_add
from facerec import run_face_recognition

while True:
    print('Face recognition demo:')
    print('run - Run face recognition for known faces')
    print('add - Add new face')
    print('exit - Leave demo')

    answer = input("Please enter an option: ")

    if answer == 'run':
        run_face_recognition()
    elif answer == 'add':
        run_face_add()
    elif answer == 'exit':
        break