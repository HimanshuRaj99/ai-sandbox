<template>
  <div class="body-bg">
    <div>
      <BackButton />
    </div>
    <div class="synonym-swap">
      <div class="synonym-swap-container">
        <h1 class=" heading">Synonym Swap Generator</h1> 
        <form class="synonym-swap-form" @submit.prevent="generateSynonymSwap">
          <div class="input-group">
            <label for="topic">Lesson Topic or Paragraph:</label>
            <textarea v-model="topic" id="topic" required></textarea>
          </div>
          <div class="input-group">
            <label for="gradeLevel">Grade level</label>
            <select id="gradeLevel" v-model="gradeLevel" class="drop-down" required>
              <option disabled value="">Select Grade level</option>
              <option v-for="option in gradeLevelOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label for="model">Model</label>
            <select id="model" v-model="model" class="drop-down" required>
              <option disabled value="">Select Model</option>
              <option v-for="option in modelOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label for="standard">Educational Standards</label>
            <select id="standard" v-model="standard" class="drop-down" required>
              <option disabled value="">Select Educational Standards.</option>
              <option value="common_core">Common Core</option>
              <option value="ngss">NGSS</option>
              <option value="state_standards">State Standards</option>
              <option value="international_standards">International Standards</option>
            </select>
          </div>
          <div class="input-group">
            <label for="numQuestions">Number of Questions:</label>
            <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="5" required />
          </div>
          <div class="button-row">
            <button type="submit" class="submit-btn" :disabled="isLoading">Generate Quiz</button>
          </div>
        </form>
      </div>
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
      </div>
    </div>
  </div>
</template>

<script>
import BackButton from '../components/BackButton.vue';
import axios from 'axios';
import { API_ENDPOINTS, BASE_URL } from '@/constants';

export default {
  components: {
    BackButton
  },
  data() {
    return {
      topic: '',
      gradeLevel: '',
      model: '',
      standard: '',
      numQuestions: 1,
      gradeLevelOptions: [
        { value: 3, label: 'Grade 3' },
        { value: 4, label: 'Grade 4' },
        { value: 5, label: 'Grade 5' }
      ],
      modelOptions: [
        { value: 'llama-3.1-8b-instant', label: 'llama-3.1-8b-instant' },
        { value: "llama-3.1-70b-versatile", label: 'llama-3.1-70b-versatile' },
        { value: 'llama3-8b-8192', label: 'llama3-8b-8192' },
        { value: "llama3-70b-8192", label: 'llama3-70b-8192' },
        { value: "mixtral-8x7b-32768", label: 'mixtral-8x7b-32768' }
      ],
      isLoading: false
    };
  },
  methods: {
    async generateSynonymSwap() {
      this.isLoading = true;

      try {
        const response = await axios.post(`${BASE_URL}${API_ENDPOINTS.SYNONYM_SWAP}`, {
          topic: this.topic,
          gradeLevel: this.gradeLevel,
          model: this.model,
          standard: this.standard,
          num_questions: this.numQuestions
        });

        const parsedData = JSON.parse(response.data);
        console.log('Parsed API Response:', parsedData);
        const wordBank = JSON.stringify(parsedData.word_bank);
        const sentences = JSON.stringify(parsedData.sentences);

        this.$router.push({
          name: 'SynonymSwapActivity',
          query: { wordBank, sentences }
        });
        
        console.log(response.data);
        // Handle response data as needed
      } catch (error) {
        console.error('Error generating synonym swap:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.synonym-swap {
  display: flex;
  width: 60%;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #f5f5f5;
}

.synonym-swap-container {
  width: 100%;
  max-width: 500px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0px 20px 20px 20px;
}

.title {
  text-align: center;
  font-size: 18px;
  /* color: #888; */
  margin: 0 0 5px 0;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

textarea, select, input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  resize: vertical;
}

.button-row {
  text-align: center;
}

/* button {
  width: 100%;
  padding: 10px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
} */

/* button:hover {
  background-color: #333;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
} */

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #333;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 600px) {
  .synonym-swap-container {
    padding: 15px;
  }
  
  .title {
    font-size: 16px;
  }
  
  textarea, select, input, button {
    font-size: 14px;
  }
}
</style>
