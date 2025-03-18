import json
import ollama
# Author: DoanNgocThanh 
# Github: 
# OCRAnalyzer class for OCR tasks (Trích xuất thông tin từ văn bản OCR thành dữ liệu JSON)
# Learn more about Ollama at https://ollama.ai/

class dh_OCRAnalyzer:
    def __init__(self, model="llama3.2", num_ctx=512, num_predict=256):
        self.model = model
        self.num_ctx = num_ctx
        self.num_predict = num_predict

    def analyze_0(self, ocr_text):
        prompt = f"""
        Trích xuất thông tin từ văn bản sau và trả về JSON:
        Văn bản: "{ocr_text}"
        
        JSON:
        {{
            "full_name": "",
            "date_of_birth": "(dd/mm/yyyy)",
            "sex": "(Nam/Nữ)" ,
            "nationality": "",
            "place_of_origin": "",
            "place_of_residence": "",
            "id_number": "",
            "expiry_date": "(dd/mm/yyyy)"
        }}
        Vui lòng không giải thích gì thêm, chỉ trả về thông tin cần thiết.
        """

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={"num_ctx": self.num_ctx, "num_predict": self.num_predict, "stream": True}
        )

        # Xử lý kết quả JSON
        try:
            print("✅ Kết quả trả về:")
            print(response['message']['content'])
            result_json = json.loads(response['message']['content'])
            
            return result_json
        except (json.JSONDecodeError, KeyError):
            print("❌ Lỗi: Kết quả không phải JSON hợp lệ hoặc thiếu dữ liệu")
            return None
        

# === Chạy thử nghiệm ===

def main():
    ocr_text = """
    Họ và tên: Nguyễn Văn A
    Ngày sinh: 01/01/1990
    Giới tính: Nam
    Quốc tịch: Việt Nam
    Nơi sinh: Hà Nội
    Nơi ở hiện tại: TP. Hồ Chí Minh
    Số CMND: 123456789
    Ngày hết hạn: 01/01/2025
    """

    ocr_analyzer = dh_OCRAnalyzer()
    result_json = ocr_analyzer.analyze_0(ocr_text)
    if result_json:
        print("🔥 Kết quả JSON:")
        print(json.dumps(result_json, indent=4, ensure_ascii=False))
main()