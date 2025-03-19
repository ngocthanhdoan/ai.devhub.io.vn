from dh_plugins.dh_OCRProcessor import dh_OCRProcessor
from dh_plugins.dh_OCRAnalyzer import dh_OCRAnalyzer
import json
# === Chạy thử nghiệm ===
def main():
    image_path = "/home/Code/Python/pyocr/Test14.png"
    try:
        with open(image_path, "rb") as f:
            file_content = f.read()

        ocr_processor = dh_OCRProcessor(use_gpu=False, vietocr_model="vgg_transformer")
        result_text = ocr_processor.process_image(file_content)

        print("🔥 Kết quả nhận dạng:", result_text)
        ocr_analyzer = dh_OCRAnalyzer()
        result_json = ocr_analyzer.analyze_0(result_text)
        if result_json:
         print("🔥 Kết quả JSON:")
         print(json.dumps(result_json, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file ảnh: {image_path}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
