import cv2
import numpy as np
from paddleocr import PaddleOCR
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
from pdf2image import convert_from_bytes
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

class dh_OCRProcessorMutifile:
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
    
    def preprocess_image(self, file_content, file_type):
        """Chuyển đổi file ảnh thành dạng có thể xử lý bằng OpenCV."""
        try:
            images = []
            if file_type == 'pdf':
                images = convert_from_bytes(file_content)
            elif file_type == 'tiff':
                pil_images = Image.open(file_content)
                for i in range(pil_images.n_frames):
                    pil_images.seek(i)
                    images.append(pil_images.copy())
            else:
                file_bytes = np.frombuffer(file_content, np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                if img is not None:
                    images.append(img)
            
            processed_images = []
            for img in images:
                if isinstance(img, Image.Image):
                    img = np.array(img)
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                if img is None:
                    raise ValueError("Không thể đọc ảnh")
                img = cv2.resize(img, (800, 800))  # Resize để tăng tốc xử lý
                processed_images.append(img)
            return processed_images
        except Exception as e:
            print(f"Lỗi tiền xử lý ảnh: {e}")
            return []

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

    def process_image(self, file_content, file_type):
        """Quy trình đầy đủ: Tiền xử lý -> Nhận diện vùng chữ -> OCR."""
        images = self.preprocess_image(file_content, file_type)
        if not images:
            return ""
        
        all_texts = []
        for img in images:
            regions = self.detect_text_regions(img)
            text = self.recognize_text(img, regions)
            all_texts.append(text)
        
        return "\n".join(all_texts)

# === Chạy thử nghiệm ===
def main():
    image_path = "/root/ai.devhub.io.vn/Test.pdf"
    file_type = image_path.split('.')[-1].lower()
    try:
        with open(image_path, "rb") as f:
            file_content = f.read()

        ocr_processor = dh_OCRProcessorMutifile(use_gpu=False, vietocr_model="vgg_seq2seq")
        result_text = ocr_processor.process_image(file_content, file_type)

        print("🔥 Kết quả nhận dạng:", result_text)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file ảnh: {image_path}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
