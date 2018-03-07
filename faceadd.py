import cv2
import os
import copy

def run_face_add():
    font = cv2.FONT_HERSHEY_DUPLEX
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, img = video_capture.read()
        live_img = copy.copy(img)
        cv2.putText(live_img, "Smile and hit ENTER when ready!", (20, 80), font, 2.0, (0, 0, 255), 2)
        
        cv2.namedWindow("Smile", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Smile", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Smile", live_img)

        key = cv2.waitKey(1)
        if key == 13:
            video_capture.release()
            cv2.destroyAllWindows()
            file_name = ""
            while len(file_name)== 0:
                file_name = input("Please enter a Name: ")
            cv2.imwrite(os.path.join('images', file_name + '.jpg'), img)
            break
        elif key == 27: #ESC
            break


    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_add()