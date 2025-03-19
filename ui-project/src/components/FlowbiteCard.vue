<template>
    <div
      :class="[
        'shadow-lg rounded-lg p-6 hover:scale-105 transform transition-all duration-300',
        `bg-gradient-${color}-600`, // Tạo class CSS động
        `text-${color}-100`         // Tạo class CSS động cho text
      ]">
      <div class="flex items-center justify-between mb-4">
        <div class="text-4xl font-bold">{{ value }}</div>
        <div class="text-3xl text-white opacity-60">
          <i :class="icon"></i>
        </div>
      </div>
      <h2 class="text-lg font-semibold">{{ title }}</h2>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: String,
      value: Number,
      icon: String,
      color: String
    }
  };
  </script>
  
  <style scoped>
  /* Định nghĩa các class CSS theo màu sắc */
  .bg-gradient-blue-600 {
    background: linear-gradient(to right, #3b82f6, #2563eb);
  }
  
  .bg-gradient-green-600 {
    background: linear-gradient(to right, #10b981, #16a34a);
  }
  
  .bg-gradient-red-600 {
    background: linear-gradient(to right, #ef4444, #dc2626);
  }
  
  .text-blue-100 {
    color: #e0f7fa;
  }
  
  .text-green-100 {
    color: #a7f3d0;
  }
  
  .text-red-100 {
    color: #fecaca;
  }
  </style>
  