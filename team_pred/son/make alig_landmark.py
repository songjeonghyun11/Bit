import numpy as np
import dlib
import cv2

RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
MOUTH = list(range(42, 68))
NOSE = list(range(27, 36))
EYEBROWS = list(range(17, 27))
JAWLINE = list(range(17, 27))
ALL = list(range(0, 68))
EYES = list(range(36, 48))

predictor_file = 'son_file/model/shape_predictor_68_face_landmarks.dat' 
dataset_paths = ['son_file/image/tedy-front/', 'son_file/image/kang-front/', 'son_file/image/unknown-front/']
output_paths = ['son_file/image/tedy-test/', 'son_file/image/kang-test/', 'son_file/image/unknown-test/']
MARGIN_RATIO = 1 #랜드마크 사이즈
OUTPUT_SIZE = (400, 400)
number_images = 20
image_type = '.jpg'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file)


def getFaceDimension(rect):
    return (rect.left(), rect.top(), rect.right() - rect.left(), rect.bottom() - rect.top())

def getCropDimension(rect, center):
    width = (rect.right() - rect.left())
    width = width + int(50)
    half_width = width // 2
    (centerX, centerY) = center
    startX = centerX - half_width
    endX = centerX + half_width
    startY = rect.top() - 30
    endY = rect.bottom() + 30
    return (startX, endX, startY, endY) 

for (i, dataset_path) in enumerate(dataset_paths):
    output_path = output_paths[i]
    
    for idx in range(number_images):
        input_file = dataset_path + str(idx+1) + image_type

        # get RGB image from BGR, OpenCV format
        image = cv2.imread(input_file)
        image_origin = image.copy()

        (image_height, image_width) = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 1)
        for (i, rect) in enumerate(rects):
            (x, y, w, h) = getFaceDimension(rect)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            points = np.matrix([[p.x, p.y] for p in predictor(gray, rect).parts()])
            show_parts = points[EYES]
            
            right_eye_center = np.mean(points[RIGHT_EYE], axis = 0).astype("int")
            left_eye_center = np.mean(points[LEFT_EYE], axis = 0).astype("int")
            print(right_eye_center, left_eye_center)
            
            
            cv2.circle(image, (right_eye_center[0,0], right_eye_center[0,1]), 5, (0, 0, 255), -1)
            cv2.circle(image, (left_eye_center[0,0], left_eye_center[0,1]), 5, (0, 0, 255), -1)
            
            cv2.circle(image, (left_eye_center[0,0], right_eye_center[0,1]), 5, (0, 255, 0), -1)
            cv2.line(image, (right_eye_center[0,0], right_eye_center[0,1]),
            (left_eye_center[0,0], left_eye_center[0,1]), (0, 255, 0), 2)
            cv2.line(image, (right_eye_center[0,0], right_eye_center[0,1]),
            (left_eye_center[0,0], right_eye_center[0,1]), (0, 255, 0), 1)
            cv2.line(image, (left_eye_center[0,0], right_eye_center[0,1]),
            (left_eye_center[0,0], left_eye_center[0,1]), (0, 255, 0), 1)
            
            eye_delta_x = right_eye_center[0,0] - left_eye_center[0,0]
            eye_delta_y = right_eye_center[0,1] - left_eye_center[0,1]
            degree = np.degrees(np.arctan2(eye_delta_y,eye_delta_x)) - 180
            
            eye_distance = np.sqrt((eye_delta_x ** 2) + (eye_delta_y ** 2))
            aligned_eye_distance = left_eye_center[0,0] - right_eye_center[0,0]
            scale = aligned_eye_distance / eye_distance # 사진을 돌리는 비율
            
            eyes_center = ((left_eye_center[0,0] + right_eye_center[0,0]) // 2,
            (left_eye_center[0,1] + right_eye_center[0,1]) // 2)
            cv2.circle(image, eyes_center, 5, (255, 0, 0), -1)
            
            metrix = cv2.getRotationMatrix2D(eyes_center, degree, scale) #센터지점과 각도와 스케일을 함수를 사용하여 돌린다.
            cv2.putText(image, "{:.5f}".format(degree), (right_eye_center[0,0], right_eye_center[0,1] + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            warped = cv2.warpAffine(image_origin, metrix, (image_width, image_height),
            flags=cv2.INTER_CUBIC) # 이미지 회전
            
            cv2.imshow("warpAffine", warped)
            (startX, endX, startY, endY) = getCropDimension(rect, eyes_center) #사진을 자르는 함수 getCrop
            croped = warped[startY:endY, startX:endX]
            output = cv2.resize(croped, OUTPUT_SIZE)
            cv2.imshow("output", output)
            
            for (i, point) in enumerate(show_parts): #눈의 점을 찍어주는 부분 앞에들어가도된다.
                x = point[0,0]
                y = point[0,1]
                cv2.circle(image, (x, y), 1, (0, 255, 255), -1)
                
                gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 1)
                
            for(i, rect) in enumerate(rects):
                points = np.matrix([[p.x, p.y] for p in predictor(gray, rect).parts()])
                show_parts = points[ALL]
                print(show_parts)
                
            for (i, point) in enumerate(show_parts):
                x = point[0, 0]
                y = point[0, 1] #flatten과 같다 
                cv2.circle(output, (x, y), 1, (0, 255, 255), -1)
                cv2.putText(output, "{}".format(i + 1), (x, y - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                
            cv2.imshow("output:", output)
            output_file = output_path + str(idx+1) + image_type
            cv2.imshow(output_file, output)
            cv2.imwrite(output_file, output)
    

# cv2.imshow("Face Alignment", image)
cv2.waitKey(0)   
cv2.destroyAllWindows()