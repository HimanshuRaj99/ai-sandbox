<template>
    <div class="card-container">
      <div class="card">
        <div class="card-content">
          <div class="icon">🔐</div>
          <div class="text">
            <h3>Enter Passcode</h3>
            <form @submit.prevent="submitPasscode">
              <input v-model="passcode" type="password" placeholder="Enter passcode" required>
              <button type="submit">Submit</button>
            </form>
            <p v-if="error" class="error">{{ error }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { HTTP_STATUS, API_ENDPOINTS, LOCAL_STORAGE_KEYS, BASE_URL } from '@/constants';
  
  export default {
    data() {
      return {
        passcode: '',
        error: ''
      }
    },
    methods: {
      async submitPasscode() {
        console.log('Attempting to submit passcode');

        try {
          const response = await axios.post(`${BASE_URL}${API_ENDPOINTS.VERIFY_PASSCODE}`, null, {
            headers: {
              'Content-Type': 'application/json',
              'X-Passcode': this.passcode
            }
          });
  
          console.log('Passcode verification API call successful');
  
          if (response.status === HTTP_STATUS.OK && response.data.status === 'success') {
            console.log('Passcode verified successfully');
            localStorage.setItem(LOCAL_STORAGE_KEYS.IS_AUTHENTICATED, 'true');
            this.$router.push('/home');
          } else {
            console.log('Unexpected response from server');
            this.error = 'An unexpected error occurred. Please try again.';
          }
        } catch (error) {
          console.error('Error verifying passcode', error);
          if (error.response && error.response.status === HTTP_STATUS.FORBIDDEN) {
            this.error = 'Invalid passcode. Please try again.';
          } else {
            this.error = 'An error occurred. Please try again.';
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .card-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px;
    background-color: #f0f0f0;
    min-height: 100vh;
    align-items: center;
    justify-content: center;
  }
  
  .card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 16px;
    display: flex;
    justify-content: space-between;
    max-width: 400px;
    margin: 0 auto;
  }
  
  .card-content {
    display: flex;
    align-items: center;
    width: 100%;
  }
  
  .icon {
    margin-right: 16px;
    width: 40px;
    height: 40px;
    font-size: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .text {
    flex-grow: 1;
  }
  
  .text h3 {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 16px;
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  input {
    margin-bottom: 8px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .error {
    margin: 8px 0 0;
    font-size: 14px;
    color: #ff3860;
  }
  </style>