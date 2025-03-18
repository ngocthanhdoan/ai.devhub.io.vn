import cv2
from qreader import QReader
from datetime import datetime
# Author: DoanNgocThanh 
# Github: 
# QRProcessor class for QR code tasks (Nhận diện và xử lý dữ liệu từ mã QR)
class dh_QRProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.qreader = QReader()

    def process_qr_code(self):
        # Get the image that contains the QR code
        image = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
        # Use the detect_and_decode function to get the decoded QR data
        return self.qreader.detect_and_decode(image=image)[0]
    def get_info_citizendid(self):
        decoded_text = self.process_qr_code()
        if decoded_text is None:
            return None
        fields = decoded_text.split('|')
        if len(fields) != 7:
            return None
        def format_date(date_str):
            try:
                return datetime.strptime(date_str, "%d%m%Y").strftime("%d/%m/%Y")
            except ValueError:
                return None
        return {
            "id": fields[0],
            "citizen_id": fields[1],
            "name": fields[2],
            "dob": format_date(fields[3]),
            "gender": fields[4],
            "address": fields[5],
            "expiry_date": format_date(fields[6])
        }
# Example usage
if __name__ == "__main__":
    processor = dh_QRProcessor("/home/Code/Python/ocr/img/Test6.png")
    decoded_text = processor.get_info_citizendid()
    print(decoded_text)