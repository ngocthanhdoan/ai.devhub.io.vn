<script>
export default {
    data() {
        return {
            apiKey: '',
            isLoading: false,
            imagePreview: null,
            selectedFile: null,
            ocrResult: null,
            interactionData: {} // Dữ liệu tương tác với khách hàng
        };
    },
    created() {
        // Kiểm tra nếu có dữ liệu trong sessionStorage và tải lại
        const storedData = sessionStorage.getItem('interactionData');
        if (storedData) {
            this.interactionData = JSON.parse(storedData);
            this.apiKey = this.interactionData.apiKey || '';
            this.imagePreview = this.interactionData.imagePreview || null;
            this.ocrResult = this.interactionData.ocrResult || null;
            this.selectedFile = this.interactionData.selectedFile || null;
        }
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.selectedFile = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.imagePreview = e.target.result;
                    // Cập nhật dữ liệu tương tác và lưu vào sessionStorage
                    this.updateInteractionData();
                };
                reader.readAsDataURL(file);
            }
        },
        async processImage() {
            if (!this.apiKey || !this.selectedFile) return;
            this.isLoading = true;
            try {
                const formData = new FormData();
                formData.append("file", this.selectedFile);
                const response = await fetch("http://localhost:5000/api/ocr", {
                    method: "POST",
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }

                const data = await response.json();
                if (data.text) {
                    this.ocrResult = data.text;
                    // Cập nhật dữ liệu tương tác và lưu vào sessionStorage
                    this.updateInteractionData();
                    this.showToast("Image processed successfully!");
                } else {
                    throw new Error("Invalid response format");
                }
            } catch (error) {
                console.error('Error processing image:', error);
            } finally {
                this.isLoading = false;
            }
        },
        // Hàm cập nhật đối tượng dữ liệu tương tác và lưu vào sessionStorage
        updateInteractionData() {
            this.interactionData = {
                apiKey: this.apiKey,
                imagePreview: this.imagePreview,
                selectedFile: this.selectedFile,
                ocrResult: this.ocrResult,
            };
            sessionStorage.setItem('interactionData', JSON.stringify(this.interactionData));
        },
        showToast(message) {
            const toast = document.createElement('div');
            toast.textContent = message;
            toast.className = 'toast toast-success';
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }
    },
};
</script>

<template>
    <div class="bg-gray-100 antialiased dark:bg-gray-900 py-16">
        <div class="mx-auto max-w-screen-md px-8">
            <!-- OCR Section -->
            <div class="bg-white rounded-lg shadow-md dark:bg-gray-800">

                <div class="p-6 space-y-6">
                    <!-- API Key Input -->
                    <div>
                        <label for="apiKeyInput" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            API Key
                        </label>
                        <input id="apiKeyInput" type="text" v-model="apiKey"
                            class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                            placeholder="Enter your API key" />
                    </div>

                    <!-- File Upload -->
                    <div>
                        <label for="fileInput" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Upload an Image
                        </label>
                        <input id="fileInput" type="file" 
                            class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                            @change="handleFileUpload" />
                    </div>

                    <!-- Image Preview -->
                    <div v-if="imagePreview" class="mt-4">
                        <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Image Preview:</h2>
                        <img :src="imagePreview" alt="Uploaded Image" class="mt-2 max-w-full rounded-lg shadow-md" />
                    </div>

                    <!-- Process Button -->
                    <button type="button"
                        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        @click.prevent="processImage" :disabled="isLoading || !apiKey || !selectedFile">
                        <span v-if="!isLoading">Process Image</span>
                        <span v-else class="flex items-center">
                            <svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg"
                                fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                            </svg>
                            Processing...
                        </span>
                    </button>

                    <!-- OCR Result -->
                    <div v-if="ocrResult"
                        class="p-4 bg-blue-50 border border-blue-200 rounded-lg dark:bg-gray-700 dark:border-gray-600">
                        <h2 class="text-sm font-semibold text-blue-800 dark:text-blue-400">OCR Result:</h2>
                        <p class="text-gray-700 dark:text-gray-300 mt-2">{{ ocrResult }}</p>
                    </div>
                    
                    <!-- Loading State -->
                    <div v-if="isLoading" class="text-center text-blue-600 dark:text-blue-400">
                        <p>Please wait while we process your image...</p>
                    </div>
                </div>
            </div>

            <!-- Request Log Section -->
            <div class="mt-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
                <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">Request Log</h2>
                <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th class="px-4 py-2">Key</th>
                            <th class="px-4 py-2">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="px-4 py-2">API Key</td>
                            <td class="px-4 py-2">{{ apiKey }}</td>
                        </tr>
                        <tr>
                            <td class="px-4 py-2">File Name</td>
                            <td class="px-4 py-2">{{ selectedFile?.name }}</td>
                        </tr>
                        <tr>
                            <td class="px-4 py-2">File Size</td>
                            <td class="px-4 py-2">{{ selectedFile?.size }} bytes</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Thêm style tùy chỉnh */
body {
    font-family: 'Inter', sans-serif;
}

input:focus, button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

button {
    transition: transform 0.2s ease, background-color 0.3s ease;
}

button:hover {
    transform: translateY(-2px);
}

.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: #38a169;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 16px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}
</style>
