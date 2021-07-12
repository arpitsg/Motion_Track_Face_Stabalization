import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fps = cap.get(cv2.CAP_PROP_FPS)

wi = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
he = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('video_out_face.mp4',0x7634706d, fps, (wi, he))

xmin=0
ymin=0
fwidth=0
fheight=0

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    
    ret, img = cap.read()
    faces = face_detection.process(img)
    if xmin==0:
        xmin=img.shape[1]//4
        fwidth=img.shape[1]//2
    width=img.shape[0]*9/16

    
    try:
        nose_x=int((faces.detections[0].location_data.relative_keypoints[2].x)*img.shape[1])
        nose_y=int((faces.detections[0].location_data.relative_keypoints[2].y)*img.shape[0])

        xmin=int((faces.detections[0].location_data.relative_bounding_box.xmin)*img.shape[1])
        ymin=int((faces.detections[0].location_data.relative_bounding_box.ymin)*img.shape[0])
        fwidth=int((faces.detections[0].location_data.relative_bounding_box.width)*img.shape[1])
        fheight=int((faces.detections[0].location_data.relative_bounding_box.height)*img.shape[0])
    except:
        print('no face')
        

    x=img.shape[1]/4
   

    center=(xmin)+(fwidth)//2

    left=(center-width/2)
    if left < 0:
        left=0
    right=left+width

    if right > img.shape[1]:
        right=img.shape[1]
        left=right-width
    left=int(left)
    right=int(right)

    print(left , right)

    crop_img = img[0:img.shape[0], left:right]
    # img = cv2.circle(img, (nose_x,nose_y), 2, (0,0,0), 2)
    out.write(crop_img)


    cv2.imshow('video',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
print(4)
# Destroy all the windows
cv2.destroyAllWindows()
