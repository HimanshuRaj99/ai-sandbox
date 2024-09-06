<template>
  <div class="body-bg">
  <div>
    <BackButton />
  </div>
  <div class="reveal">
    <div class="reveal-container">
      <h2 class="heading">Search to Reveal</h2>
      <form class="reveal-input-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="gradeLevel">Grade level</label>
              <select id="gradeLevel" class="drop-down" v-model="formData.gradeLevel" required>
                <option disabled value="">Select Grade</option>
                <option v-for="option in gradeLevelOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
          <label for="model">Model</label>
              <select id="modelLevel" class="drop-down" v-model="formData.model"  required>
                <option disabled value="">Select model</option>
                <option v-for="option in modelOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
          <label for="model">Type a word</label>
          <input type="text" v-model="input" />
        <!-- <label for="gradeLevel">Grade level</label> -->
        </div>
        <div v-if="!loading" class="button-row">
          <button type="submit" class="submit-btn">Submit</button>
        </div>
      </form>
       <div v-if="loading" class="loading-container" >
          <div class="loading-spinner"></div>
       </div>
      <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
      </div>
      <!-- Display API Response -->
      <div v-if="apiResponse" class="response-card">
        <h3>
          {{ apiResponse.word }}
          <span class="part-of-speech" v-if="apiResponse.morphology.part_of_speech">({{ apiResponse.morphology?.part_of_speech || '' }})</span>
          <!-- <span class="audio-icon" @click="handleSpeak(apiResponse.word)">🔊</span> -->
          <AudioPronounce :definition="apiResponse.word" />
        </h3>
        <p><strong>Meaning:</strong> {{ apiResponse.details.meaning || '' }} <AudioPronounce :definition="apiResponse.details.meaning" /> </p>
        <p><strong>Synonyms:</strong> {{ apiResponse.details.synonyms?.join(', ') || '' }}</p>
        <p><strong>Antonyms:</strong> {{ apiResponse.details.antonyms?.join(', ') || '' }}</p>
        <div>
        <h4 v-if="apiResponse.morphology ">{{'Morphology' || ''}}</h4>
        <div class="morphology">
        <p v-if="apiResponse.morphology.root"><strong>root:</strong> {{ apiResponse.morphology?.root || '' }}</p>
        <p v-if="apiResponse.morphology.prefix"><strong>prefix:</strong> {{ apiResponse.morphology?.prefix || '' }}</p>
        <p v-if="apiResponse.morphology.suffix"><strong>suffix:</strong> {{ apiResponse.morphology?.suffix || '' }}</p>
      </div>
      </div>
      </div>
    </div>
  </div>
</div>
  </template>
  
  <script>
  import BackButton from '../components/BackButton.vue';
  import AudioPronounce from '../components/AudioPronounce.vue';
  import { API_ENDPOINTS, BASE_URL } from '@/constants';

  export default {
    components :{
       BackButton,
       AudioPronounce
    },
    data() {
      return {
        input: '',
        formData: {
          gradeLevel: '',
          model: '',
        },
        errorMessage: '',
        loading: false,
        gradeLevelOptions: [
        { value: 3, label: 'Grade 3' },
        { value: 4, label: 'Grade 4' },
        { value: 5, label: 'Grade 5' }
      ],
      modelOptions: [
        { value: 'llama-3.1-8b-instant', label: 'llama-3.1-8b-instant' },
        { value: "llama-3.1-70b-versatile", label: 'llama-3.1-70b-versatile' },
      ],
        apiResponse: null,
        usEnglishVoice: null
      };
    },
    mounted() {
      this.fetchVoices();
      if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = this.fetchVoices;
      }
    },
    methods: {
      async fetchVoices() {
        if ('speechSynthesis' in window) {
          const voices = window.speechSynthesis.getVoices();
          const usEnglishVoice = voices.find(voice => voice.lang === 'en-US');
          this.usEnglishVoice = usEnglishVoice;
        }
      },
      async handleSubmit() {
        if (!this.input.trim()) return;
        const payload = {
        word: this.input,
        grade: parseInt(this.formData.gradeLevel),
        model:this.formData.model
        };
        console.log(payload);
        this.apiResponse = null;  // Reset the response
        this.errorMessage = '';   // Reset the error message
        this.loading = true;
        try {
          const response = await fetch(`${BASE_URL}${API_ENDPOINTS.CLICK_TO_REVEAL}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          });
          if (!response.ok) {  // Check if response is not OK
            throw new Error(`HTTP error! Status: ${response.status}`);
         }
          const data = await response.json();
          this.apiResponse = data;
        } catch (error) {
          console.error('Error calling the API:', error);
          this.errorMessage = 'An error occurred while fetching data. Please try again later.';
        } finally {
            this.loading = false;  // Set loading to false
        }
        // this.input = '';
      },
      handleSpeak(text) {
        if ('speechSynthesis' in window) {
          const utterance = new SpeechSynthesisUtterance(text);
          if (this.usEnglishVoice) {
            utterance.voice = this.usEnglishVoice;
          }
          window.speechSynthesis.speak(utterance);
        } else {
          console.warn('Speech synthesis not supported in this browser.');
        }
      }
    }
  };
  </script>
  
<style scoped>

.title{
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: 18px;
  /* color: #888; */
  margin: 0 0 5px 0;
  margin-bottom: 20px;
}
h3{
    text-transform: capitalize;
}
.part-of-speech{
  padding-left: 1%;
  padding-right: 1%;
  font-size: 14px;
  text-transform: lowercase; 
}

.reveal {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60%; /* Adjust width as needed */
  margin-bottom: 20px; /* Adjust margin-bottom as needed */
  /* background-color: #f5f5f5; */
  border-radius: 8px;
  /* box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); */
  /* Remove any unnecessary properties like max-height, margin-left, flex-direction, height, padding-bottom, border */
}

.reveal-container {
  width: 90%;
  height: auto;
  margin-top:20px;
  overflow: hidden;
  padding-bottom: 8px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.reveal-input-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 6px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  align-items: center;
  width: 60%;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 700;
}

.form-group select{
  width: 100%;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  background-color: #fff; 
}
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  background-color: #fff; 
}
.reveal-input-form::after {
  content: "Get meaning and morphology of word.";
  position: absolute;
  top:210px;
  left: 50px;
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: #666;
  opacity: 0;
  transition: opacity 0.3s ease;
  display: none;
}

.reveal-input-form:hover::after {
  opacity: 1;
}

input {
  width: 100%;
  padding: 10px;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #ffffff;
}
.button-row {
  width: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* button {
  background-color: #5a5a5ab4;
  color: #fff;
  width: 100%;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 5px 0 15px;
} */
/* button:hover{
background-color: black;
} */
.response-card {
  background-color: #d2dae9;
  margin: 20px 30px 10px;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  max-width: 100%;
  box-sizing: border-box;
}

h3 {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  
}

.audio-icon {
  margin-left: 10px;
  cursor: pointer;
  font-size: .9em;
}

h4 {
  margin-top: 15px; 
}
.morphology{
  margin-left: 20px;
}
p {
  margin: 5px 0;
}

.title {
  margin-top: 20px;
  margin-bottom: 20px;
}

section {
  display: flex;
  align-items: center;
}

.emoji-icon {
  margin-right: 14px;
  width: 24px;
  height: 24px;
}

.drop-down {
  display: flex;
  align-items: center;
  padding: 2px ;
  cursor: pointer;
  width: 96px;
  height: 40px;
  margin-right: 10px;
  font-size: small;
  padding-left: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #ffffff;
}
select option:disabled {
  color: #999;
  font-style: italic;
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

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  margin-top : 10px;
}

/* Spinner animation */
.spinner div {
  display: inline-block;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #333;
  animation: spinner 1.2s infinite ease-in-out;
}

/* Spinner animation */
.spinner div:nth-child(1) {
  animation-delay: -0.24s;
}
.spinner div:nth-child(2) {
  animation-delay: -0.12s;
}
.spinner div:nth-child(3) {
  animation-delay: 0;
}

@keyframes spinner {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}
</style>