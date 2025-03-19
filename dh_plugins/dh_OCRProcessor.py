import cv2
import numpy as np
from paddleocr import PaddleOCR
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
# Author: DoanNgocThanh 
# Github: 
# OCRProcessor class for OCR tasks (Nhận diện vùng chữ và nhận dạng ký tự từ ảnh)
# Learn more about Ollama at https://ollama.ai/
# Additional resources:
# - https://github.com/pbcquoc/vietocr
# - https://github.com/PaddlePaddle/PaddleOCR
class dh_OCRProcessor:
    def __init__(self, use_gpu=False, vietocr_model="vgg_seq2seq"):
        self.use_gpu = use_gpu
        self.vietocr_model = vietocr_model
        self.detector = self.load_paddleocr()
        self.recognitor = self.load_vietocr()
    
    @lru_cache(maxsize=1)
    def load_paddleocr(self):
        """Khởi tạo PaddleOCR với cache để tăng tốc khởi động."""
        return PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=self.use_gpu, det_db_box_thresh=0.3)
    
    @lru_cache(maxsize=1)
    def load_vietocr(self):
        """Khởi tạo VietOCR với cache để nhận dạng ký tự nhanh hơn."""
        config = Cfg.load_config_from_name(self.vietocr_model)
        config['cnn']['pretrained'] = False  # Tắt pretrained để giảm thời gian load
        config['predictor']['beamsearch'] = False
        config['device'] = 'cuda' if self.use_gpu else 'cpu'
        return Predictor(config)
    
    def preprocess_image(self, file_content):
        """Chuyển đổi file ảnh thành dạng có thể xử lý bằng OpenCV."""
        try:
            file_bytes = np.frombuffer(file_content, np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Không thể đọc ảnh")
            img = cv2.resize(img, (800, 800))  # Resize để tăng tốc xử lý
            return img
        except Exception as e:
            print(f"Lỗi tiền xử lý ảnh: {e}")
            return None

    def detect_text_regions(self, img, padding=4):
        """Nhận diện vùng chữ bằng PaddleOCR."""
        try:
            result = self.detector.ocr(img, cls=False, det=True, rec=False)
            if not result or len(result[0]) == 0:
                return []

            regions = []
            for line in result[0]:
                box = np.array(line, dtype=np.float32)
                x_min, y_min = max(0, int(min(box[:, 0]) - padding)), max(0, int(min(box[:, 1]) - padding))
                x_max, y_max = min(img.shape[1], int(max(box[:, 0]) + padding)), min(img.shape[0], int(max(box[:, 1]) + padding))
                regions.append((x_min, y_min, x_max, y_max))

            return regions
        except Exception as e:
            print(f"Lỗi phát hiện vùng chữ: {e}")
            return []

    def recognize_text(self, img, regions):
        """Nhận dạng văn bản từ các vùng chữ bằng VietOCR."""
        try:
            detected_texts = []
            with ThreadPoolExecutor() as executor:
                futures = []
                for (x_min, y_min, x_max, y_max) in reversed(regions):
                    cropped_img = img[y_min:y_max, x_min:x_max]
                    gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                    pil_image = Image.fromarray(gray_image)
                    futures.append(executor.submit(self.recognitor.predict, pil_image))
                
                for future in futures:
                    detected_texts.append(future.result())

            return " ".join(detected_texts)
        except Exception as e:
            print(f"Lỗi nhận dạng ký tự: {e}")
            return ""

    def process_image(self, file_content):
        """Quy trình đầy đủ: Tiền xử lý -> Nhận diện vùng chữ -> OCR."""
        img = self.preprocess_image(file_content)
        if img is None:
            return ""
        regions = self.detect_text_regions(img)
        return self.recognize_text(img, regions)

# === Chạy thử nghiệm ===
def main():
    image_path = "/home/Code/Python/pyocr/Test14.png"
    try:
        with open(image_path, "rb") as f:
            file_content = f.read()

        ocr_processor = dh_OCRProcessor(use_gpu=False, vietocr_model="vgg_transformer")
        result_text = ocr_processor.process_image(file_content)

        print("🔥 Kết quả nhận dạng:", result_text)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file ảnh: {image_path}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
