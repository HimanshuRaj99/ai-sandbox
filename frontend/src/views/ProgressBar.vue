<template>
    <div class="progress-bar">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      progress: {
        type: Number,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .progress-bar {
    width: 80%;
    height: 20px;
    background-color: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
    margin-right: 2%;
  }
  
  .progress {
    height: 100%;
    background-color: #28a745;
    border-radius: 10px;
    transition: width 0.3s ease-in-out;
  }
  </style>
  