<template>
    <div class="edit-prompt">
      <div class="back-button-container">
        <router-link to="/chatbot" class="back-button">← Back</router-link>
      </div>
      <HistoricalCharacterForm />
      <div class="chatbot-container">
        <div class="instructions-display">
          <h3>Character</h3>
          <p>{{ decodeURIComponent($route.query.instructions) }}</p>
          <button @click="hidePrompt">Hide Prompt</button>
        </div>
        <div class="chatbot-messages">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.user ? 'user-message' : 'ai-message']">
            <div v-if="!message.user" class="clipBoard">
              <CopyToClipboardButton :text="message.text" />
            </div>
            {{ message.text }}
          </div>
        </div>
        <!-- <form class="chatbot-input-form" @submit.prevent="handleSubmit">
          <input type="text" v-model="input" placeholder="Type your message..." />
          <button type="submit">Send</button>
        </form> -->
      </div>
    </div>
  </template>
  
  <script>
  import HistoricalCharacterForm from '@/components/HistoricalCharacterForm.vue';
  import CopyToClipboardButton from '@/components/CopyToClipboardButton.vue';
  import { API_ENDPOINTS, BASE_URL } from '@/constants';
  
  export default {
    components: {
      HistoricalCharacterForm,
      CopyToClipboardButton
    },
    data() {
      return {
        input: '',
        messages: []
      };
    },
    methods: {
      async chatWithBot(userInput) {
        const urlParams = new URLSearchParams(this.$route.query);
        const apiEndpoint = `${BASE_URL}${API_ENDPOINTS.CHAT}`;
        const data = {
          message: userInput,
          model: urlParams.get('model'),
          character: urlParams.get('instructions'),
          grade: parseInt(urlParams.get('gradeLevel'))
        };
  
        try {
          const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
  
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
  
          const result = await response.json();
          return result.response;
        } catch (error) {
          console.error('Error communicating with the API:', error);
          return 'There was an error processing your request.';
        }
      },
      async handleSubmit() {
        if (!this.input.trim()) return;
        const userMessage = { text: this.input, user: true };
        this.messages.push(userMessage);
        const aiMessage = { text: '...', user: false };
        this.messages.push(aiMessage);
        const response = await this.chatWithBot(this.input);
        this.messages.splice(this.messages.length - 1, 1, { text: response, user: false });
        this.input = '';
      },
      hidePrompt() {
        this.$router.push({
          path: '/chatbot',
          query: {
            ...this.$route.query
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .edit-prompt {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 20px;
    
  }
  
  .back-button-container {
    margin-bottom: 20px;
  }
  
  .back-button {
    text-decoration: none;
    color: #000;
    font-weight: bold;
    font-size: 16px;
  }
  
  .chatbot-container {
    width: 100%;
    background-color: #f0f0f0;
    border-radius: 8px;
    border: 1px solid #ccc;
    padding: 20px;
    margin-top: 20px;
  }
  
  .instructions-display {
    margin-bottom: 20px;
  }
  
  .instructions-display h3 {
    font-weight: 700;
    margin-bottom: 5px;
  }
  
  .instructions-display button {
    margin-top: 10px;
    padding: 10px;
    background-color: #000;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
  }
  
  .instructions-display button:hover {
    background-color: #333;
  }
  
  .chatbot-messages {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
  }
  
  .message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
  }
  
  .user-message {
    background-color: #e0e0e0;
  }
  
  .ai-message {
    background-color: #fff;
  }
  
  .clipBoard {
    text-align: right;
    margin-bottom: 5px;
  }
  
  .chatbot-input-form {
    display: flex;
    width: 100%;
  }
  
  .chatbot-input-form input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 10px;
    font-size: 14px;
  }
  
  .chatbot-input-form button {
    padding: 10px 20px;
    background-color: #000;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
  }
  
  .chatbot-input-form button:hover {
    background-color: #333;
  }
  </style>