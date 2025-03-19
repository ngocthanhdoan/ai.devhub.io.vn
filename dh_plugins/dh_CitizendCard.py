import cv2

# Author: DoanNgocThanh 
# Github: 
# OCRAnalyzer class for OCR tasks (dự đoán thông tin trên CMND/CCCD)
# Learn more about OpenCV at https://opencv.org/
class dh_CitizendCard:
    #Phát hiện khuôn mặt trong ảnh
    def detectFace(self, image_path):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces) > 0
    #Phát hiện vân tay trong ảnh
    def detectFingerprint(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Adjust the threshold as needed
                return True
        return False
    def isFront(self, text):
        return True
    def isBack(self, text):
        return True
    def isCitizenCard(self, text):
        return True
    