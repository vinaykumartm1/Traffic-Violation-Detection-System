import cv2
import numpy as np
import os
import imutils
from tensorflow.keras.models import load_model
import easyocr
import os 
import subprocess


def helmet_or_nohelmet(helmet_roi):
	try:
		helmet_roi = cv2.resize(helmet_roi, (224, 224))
		helmet_roi = np.array(helmet_roi,dtype='float32')
		helmet_roi = helmet_roi.reshape(1, 224, 224, 3)
		helmet_roi = helmet_roi/255.0
		return int(model.predict(helmet_roi)[0][0])
	except:
			pass


def detect_plates_v2(mode):
    cap = cv2.VideoCapture(mode)
    g = 0
    import time

    start_time = time.time()  # Get the current time
    duration = 10  # Duration for the loop to run, in seconds

    while time.time() - start_time < duration:
        g += 1
        ret, img = cap.read()
        if not ret:
             print("No Frame")
             break
        img = imutils.resize(img,height=500)
        
        height, width = img.shape[:2]

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        confidences = []
        boxes = []
        classIds = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)

                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    classIds.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x,y,w,h = boxes[i]
                color = [int(c) for c in COLORS[classIds[i]]]
                # green --> bike
                # red --> number plate
                if classIds[i]==0: #bike
                    helmet_roi = img[max(0,y):max(0,y)+max(0,h)//4,max(0,x):max(0,x)+max(0,w)]
                else: #number plate
                    x_h = x-60
                    y_h = y-350
                    w_h = w+100
                    h_h = h+100
                    crop_img = img[y:y+h, x:x+w]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 7)
                    # h_r = img[max(0,(y-330)):max(0,(y-330 + h+100)) , max(0,(x-80)):max(0,(x-80 + w+130))]
                    if y_h>0 and x_h>0:
                        h_r = img[y_h:y_h+h_h , x_h:x_h +w_h]
                        c = helmet_or_nohelmet(h_r)
                        cat = ['helmet','no-helmet'][c]
                        cv2.putText(img, cat,(x,y-100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                        person_crop = img[y_h: y_h+h_h, x_h:x_h+w_h]                
                        cv2.rectangle(img, (x_h, y_h), (x_h + w_h, y_h + h_h),(255,0,0), 10)
                        if cat=='no-helmet': print('yes')
                            
                            
                        if c!=0:
                            cv2.imwrite(os.path.join('./person', 'crop_{}.png'.format(g)), person_crop)
                            cv2.imwrite(os.path.join(img_dir, 'crop_{}.png'.format(g)), crop_img)
                            


        # writer.write(img)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    # writer.release()
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return True

def detect_plates(video_path, timeout_duration=30):
    print('starting........................................')
    command = [
        'python', './yolov5/detect_v2.py',
        '--weights', './yolov5/best.pt',
        '--img', '416',
        '--conf', '0.4',
        '--source', video_path,
        '--view-img'  # This enables live viewing
    ]

    process = subprocess.Popen(command)

    try:
        # Wait for the specified timeout duration
        process.wait(timeout=timeout_duration)
    except subprocess.TimeoutExpired:
        print(f"Detection stopped due to timeout of {timeout_duration} seconds.")
        process.terminate()  # Terminate the subprocess
        try:
            # Optionally, wait a bit for the process to terminate gracefully
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Subprocess did not terminate gracefully, forcing termination.")
            process.kill()  # Forcefully kill the process if it didn't terminate
        # Run the Streamlit app
        os.system('streamlit run app.py')
    except Exception as e:
        print(f"An error occurred: {e}")
        process.kill()


