<template>
  <div class="body-bg">
    <div>
      <BackButton />
    </div>
    <div class="feedback" >
      <div class="request-feature">
        <h1 class="heading">Feedback</h1>
        <form @submit.prevent="submitFeature">
          <div class="form-group">
            <textarea id="suggestions" v-model="suggestions" required></textarea>
          </div>
          <div v-if="!loading" class="btn-container">
            <button  class="submit-btn" type="submit">Submit</button>
          </div>
          <div v-if="loading" class="loading-container" >
            <div class="loading-spinner"></div>
          </div>
        </form>
        <p v-if="message" class="message">{{ responseData }}</p>
      </div>
    </div>
  </div>

</template>

<script>
import { API_ENDPOINTS, BASE_URL } from '@/constants';
import BackButton from '../components/BackButton.vue';
export default {
  name: 'FeedbackView',
  components: {
    BackButton
  },
  data() {
    return {
      suggestions: '',
      message: '',
      responseData: '',
      loading: false,
    };
  },
  methods: {
    async submitFeature() {
      try {
        console.log("suggestion:", this.suggestions);
        this.loading = true;
        fetch(`${BASE_URL}${API_ENDPOINTS.SEND_EMAIL}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: this.suggestions })
        })
        .then(response => response.json())
        .then(data => {
          this.message = data.message;
          this.loading = false;
          this.responseData = "Thank you for sharing your feedback with us!";
          this.response = data;  // Save the entire response data
          setTimeout(() => {
          this.clearForm();
        }, 4000); // Wait for 4000 milliseconds (3 seconds)
        })
        .catch(error => {
          console.error('Error:', error);
        });
      } catch (error) {
        this.message = 'An error occurred while submitting your request.';
        console.error(error);
      }
    },
    clearForm() {
      this.suggestions = '';
      this.message = '';
      
    }
  }
};
</script>

<style scoped>
.feedback{
  display: flex;
    justify-content: center;
    align-items: flex-start;
    background-color: #f5f5f5;
    height: 100%; /* Adjust as needed */
}
.request-feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 600px;
  margin: 60px auto 0;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.title {
  text-align: center;
  margin: 20px 0;
  font-size: 40px;
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
}

textarea {
  width: 400px;
  height: 100px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #ffffff;
  resize: vertical;
}

.btn-container {
  display: flex;
  justify-content: center;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px; 
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #333;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  z-index: 1000;
  margin: 5px 100px 15px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
/* button {
  background-color: black;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #707070;
} */

.message {
  margin-top: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
  font-style: italic;
  text-align: center;
}

/* Mimic the active-item style from sidebarView */
.active-item {
  background-color: #f0f0f0;
}
</style>
