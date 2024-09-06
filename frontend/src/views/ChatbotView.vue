<template>
  <div class="app-container">
    <BackButton @click="goToCharacterChatbot" />
    <div class="content-wrapper" :class="{ 'blurred': showConfigurePanel }">
      <div v-if="showReaderAIPanel" class="reader-ai-panel">
        <button @click="closeReaderAIPanel" class="close-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <div class="panel-title-container">
          <AudioPronounce :definition="selectedText" class="pronounce-button" />
          <h2 class="panel-title"><strong>{{ selectedText.charAt(0).toUpperCase() + selectedText.slice(1) }}</strong>
          </h2>
        </div>
        <AudioPronounce :definition="selectedDefinition" hidden />
        <p class="meaning-text"><strong>{{ selectedDefinition }}</strong></p>
        <button @click="simplifyText" class="secondary-button">
          Simplify
        </button>
      </div>

      <div class="chatbot">
        <div class="chatbot-container">
          <div class="instructions-display">
            <h2 class="welcome-title">
              Welcome! You're talking to {{ displayCharacterName !== undefined ? displayCharacterName : '...' }}
            </h2>
            <button @click="editPrompt" class="edit-button" :disabled="isLoading">
              Configure
            </button>
          </div>
          <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
          </div>
          <div class="chatbot-messages" ref="messagesContainer">
            <div v-for="(message, index) in messages" :key="index"
              :class="['message', message.user ? 'user-message' : 'ai-message']">
              <div v-if="!message.user" class="clipBoard">
                <CopyToClipboardButton :text="message.text" />
                <AudioPronounce :definition="message.text" />
              </div>
              <div v-if="message.type === 'mcq'" class="mcq-container">
                <h2 class="mcq-question-number">Question {{ message.questionNumber }}</h2>
                <h3 class="mcq-question">{{ message.question }}</h3>
                <div class="mcq-options">
                  <button v-for="(option, optionIndex) in message.options" :key="optionIndex" class="mcq-option"
                    @click="selectMCQOption(option)">
                    {{ option }}
                  </button>
                </div>
              </div>
              <div v-else @mouseup="handleTextSelection($event, message.text)"
                :class="{ 'response-message': true, 'selectable-text': readerAIEnabled }">
                {{ message.text }}
              </div>
              <div v-if="!message.user && message.suggestions" class="suggestions-container">
                <div v-for="(suggestion, index) in message.suggestions" :key="index" class="suggestion-card"
                  @click="handleSuggestionClick(suggestion)">
                  {{ suggestion }}
                </div>
              </div>
            </div>
          </div>
          <div class="chatbot-input-wrapper">
            <div class="actions-menu">
              <button @click.prevent="toggleActionsMenu" class="actions-button">
                Actions
              </button>
              <div v-if="showActionsMenu" class="actions-dropdown">
                <div class="action-item" @click="generateQuiz">Quiz</div>
              </div>
            </div>
            <form class="chatbot-input-form" @submit.prevent="handleSubmit">
              <input type="text" :disabled="!isUserSent" v-model="input" placeholder="Send a message" />
              <div class="toggle-wrapper">
                <label class="switch">
                  <input type="checkbox" v-model="readerAIEnabled">
                  <span class="slider round"></span>
                </label>
                <span class="toggle-label">Highlight Text</span>
              </div>
              <button type="submit" :disabled="!isUserSent" class="send-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showFindMeaningPopup" class="find-meaning-popup" :style="popupStyle">
      <button @click="findMeaning" class="find-meaning-button">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
          <path
            d="M9.5 3a7.5 7.5 0 0 1 5.95 12.02l4.83 4.83a1 1 0 0 1-1.41 1.41l-4.83-4.83A7.5 7.5 0 1 1 9.5 3zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11z" />
        </svg>
        Find Meaning
      </button>
    </div>
    <div v-if="showConfigurePanel" class="modal-overlay" @click="closeConfigurePanel">
      <div class="modal-content" @click.stop>
        <button @click="closeConfigurePanel" class="close-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <HistoricalCharacterForm :initialFormData="chatConfig" @submit="handleConfigureSubmit"
          @close="closeConfigurePanel" />
      </div>
    </div>
  </div>
</template>

<!-- script code -->
<script>
import CopyToClipboardButton from '@/components/CopyToClipboardButton.vue';
import AudioPronounce from '@/components/AudioPronounce.vue';
import BackButton from '../components/BackButton.vue';
import HistoricalCharacterForm from '@/components/HistoricalCharacterForm.vue';
import { API_ENDPOINTS, BASE_URL } from '@/constants';

export default {
  name: 'ChatComponent',
  components: {
    CopyToClipboardButton,
    AudioPronounce,
    BackButton,
    HistoricalCharacterForm
  },
  data() {
    return {
      input: '',
      messages: [],
      readerAIEnabled: false,
      selectedText: '',
      selectedContext: '',
      showFindMeaningPopup: false,
      showReaderAIPanel: false,
      popupStyle: {
        top: '0px',
        left: '0px',
      },
      selectedDefinition: '',
      mcqQuestionCount: 0,
      isUserSent: true,
      showPrompt: false,
      characterName: '',
      showActionsMenu: false,
      showConfigurePanel: false,
      chatConfig: {
        gradeLevel: '',
        instructions: {},
        model: '',
        version: '',
        standard: ''
      },
      isLoading: false,
      isUpdatingCharacter: true
    };
  },
  computed: {
    displayCharacterName() {
      if (this.isUpdatingCharacter) {
        return '...';
      }
      return this.characterName || '...';
    }
  },
  mounted() {
    this.initializeChat();
    document.addEventListener('keydown', this.checkKey);
    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.checkKey);
    document.removeEventListener('click', this.handleOutsideClick);
  },
  methods: {
    initializeChat() {
      this.chatConfig = {
        gradeLevel: this.$route.query.gradeLevel,
        instructions: decodeURIComponent(this.$route.query.instructions || ''),
        model: this.$route.query.model,
        version: this.$route.query.version,
        standard: this.$route.query.standard,
        provider: this.$route.query.provider
      };

      this.updateCharacterName(this.chatConfig.instructions);

      this.messages = [];

      const initialMessageString = decodeURIComponent(this.$route.query.initialMessage || '{}');

      try {
        const initialMessage = JSON.parse(initialMessageString);
        if (initialMessage.character_message) {
          this.messages.push({
            text: initialMessage.character_message,
            user: false,
            suggestions: initialMessage.suggestions || []
          });
        }
      } catch (error) {
        console.error('Error parsing initial message:', error);
      }
      this.scrollToBottom();
    },
    updateCharacterName(instructions) {
      this.isUpdatingCharacter = true;
      this.characterName = instructions
        ? instructions.charAt(0).toUpperCase() + instructions.slice(1)
        : '';
      this.$nextTick(() => {
        this.isUpdatingCharacter = false;
      });
    },
    async chatWithBot(userInput) {
      const apiEndpoint = `${BASE_URL}${API_ENDPOINTS.CHAT}`;
      const data = {
        message: userInput,
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

        const jsonResponse = await response.json();

        this.isUserSent = true;
        return {
          text: jsonResponse.character_message,
          suggestions: jsonResponse.suggestions || []
        };
      } catch (error) {
        console.error('Error communicating with the API:', error);
        return {
          text: 'There was an error processing your request.',
          suggestions: []
        };
      }
    },
    closeReaderAIPanel() {
      this.showReaderAIPanel = false;
      this.selectedText = '';
      this.selectedDefinition = '';
    },
    checkKey(event) {
      if (event.key === 'Escape' || event.key === 'Esc') {
        this.showFindMeaningPopup = false;
        this.closeConfigurePanel();
      }
    },
    async handleSubmit() {
      if (!this.input.trim()) return;
      this.isUserSent = false;
      const userMessage = { text: this.input, user: true };
      this.scrollToBottom();
      this.messages.push(userMessage);
      const response = await this.chatWithBot(this.input);
      this.messages.push({ ...response, user: false });
      this.input = '';
      this.scrollToBottom();
    },
    editPrompt() {
      this.showConfigurePanel = true;
    },
    closeConfigurePanel() {
      this.showConfigurePanel = false;
    },
    async handleSuggestionClick(suggestion) {
      this.input = suggestion;
      await this.handleSubmit();
    },
    handleTextSelection(event, context) {
      if (!this.readerAIEnabled) return;

      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        this.selectedText = selectedText;
        this.selectedContext = context;
        this.showFindMeaningPopup = true;
        this.popupStyle = {
          top: `${event.clientY}px`,
          left: `${event.clientX}px`,
        };
      } else {
        this.showFindMeaningPopup = false;
      }
    },
    goToCharacterChatbot() {
      this.$router.push('/character-chatbot');
    },
    async findMeaning() {
      const apiEndpoint = `${BASE_URL}${API_ENDPOINTS.FIND_MEANING}`;
      const data = {
        selected_characters: this.selectedText,
        context: this.selectedContext,
        grade: this.chatConfig.gradeLevel
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
        this.selectedDefinition = result.meaning;
        this.showReaderAIPanel = true;
        this.showFindMeaningPopup = false;
      } catch (error) {
        console.error('Error finding meaning:', error);
        this.showFindMeaningPopup = false;
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    toggleActionsMenu() {
      this.showActionsMenu = !this.showActionsMenu;
    },
    async simplifyText() {
      const apiEndpoint = `${BASE_URL}${API_ENDPOINTS.SIMPLIFY_MEANING}`;
      const payload = {
        text: this.selectedText,
        context: this.selectedContext,
        grade: this.chatConfig.gradeLevel,
        generated_meaning: this.selectedDefinition
      };

      try {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        this.selectedDefinition = result.simplified_meaning;
      } catch (error) {
        console.error('Error simplifying meaning:', error);
      }
    },
    async generateQuiz() {
      this.showActionsMenu = false;
      const response = await this.chatWithBot('mcq');
      this.messages.push({ ...response, user: false });
      this.scrollToBottom();
    },
    handleOutsideClick(event) {
      const actionsMenu = this.$el.querySelector('.actions-menu');
      if (actionsMenu && !actionsMenu.contains(event.target)) {
        this.showActionsMenu = false;
      }
    },
    selectMCQOption(option) {
      console.log('Selected option:', option);
      // Add logic to handle the selected MCQ option
    },
    setLoading(value) {
      this.isLoading = value;
    },
    async handleConfigureSubmit(formData) {
      console.log('Received form data:', formData);
      this.setLoading(true);
      this.showConfigurePanel = false;
      this.isUpdatingCharacter = true;

      try {
        // Update the route
        await this.$router.replace({
          path: this.$route.path,
          query: {
            gradeLevel: formData.gradeLevel,
            instructions: encodeURIComponent(formData.instructions),
            model: formData.model,
            version: formData.version,
            standard: formData.standard,
            initialMessage: encodeURIComponent(JSON.stringify({})),
          }
        });

        // Update the chat configuration
        this.chatConfig = {
          gradeLevel: formData.gradeLevel,
          instructions: formData.instructions,
          model: formData.model,
          version: formData.version,
          standard: formData.standard
        };

        // Update the character name
        this.updateCharacterName(formData.instructions);

        // Clear existing messages
        this.messages = [];

        // Wait for the next tick to ensure DOM is updated
        await this.$nextTick();

        // Reinitialize the chat with new configuration
        this.initializeChat();

        // Send an initial message to the chatbot
        const response = await this.chatWithBot('Hello, who are you?');
        this.messages.push({
          text: response.text,
          user: false,
          suggestions: response.suggestions || []
        });

        // Scroll to bottom to show the new message
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('Error in handleConfigureSubmit:', error);
      } finally {
        this.setLoading(false);
        this.isUpdatingCharacter = false;
      }
    }
  },
  watch: {
    readerAIEnabled(newValue) {
      if (!newValue) {
        this.showReaderAIPanel = false;
        this.showFindMeaningPopup = false;
        this.selectedText = '';
        this.selectedDefinition = '';
      }
    },
    '$route': {
      handler: 'initializeChat',
      immediate: true
    }
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
  font-family: 'Inter', sans-serif;
  background-color: #f5f5f5;
  margin-top: 40px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: stretch;
  max-width: 1200px;
  width: 100%;
}

.content-wrapper.blurred {
  filter: blur(5px);
  pointer-events: none;
}

.reader-ai-panel {
  width: 300px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-right: 24px;
  overflow-y: auto;
  height: 600px;
  animation: fadeInFromLeft 0.3s ease-out;
  position: relative;
}

@keyframes fadeInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.panel-title-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.panel-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
  margin-right: 10px;
}

.pronounce-button {
  background-color: #d2dae9;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
  margin-right: 10px;
}

.pronounce-button:hover {
  background-color: rgb(203, 204, 205);
}

.pronounce-button svg {
  width: 18px;
  height: 18px;
  color: white;
}

.meaning-text {
  font-style: italic;
  color: #666;
  line-height: 1.5;
}

.chatbot {
  flex-grow: 1;
  max-width: 900px;
}

.chatbot-container {
  width: 100%;
  height: 650px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: ;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.instructions-display {
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.edit-button {
  padding: 8px;
  border-radius: 5px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  background-color: #438fe7;
}

.edit-button:hover {
  background-color: #103d4e;
  /* transform: translateY(-2px); */
}

.edit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading-overlay {
  position: absolute;
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
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.chatbot-messages {
  flex-grow: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #fff;
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
  display: flex;
  flex-direction: column;
}

.chatbot-messages::-webkit-scrollbar {
  width: 8px;
}

.chatbot-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chatbot-messages::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.chatbot-messages::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.message {
  position: relative;
  padding: 14px 18px 40px;
  border-radius: 18px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  line-height: 1.5;
  transition: all 0.3s ease;
  max-width: 80%;
}

.user-message {
  padding: 14px 18px 10px;
  background-color: #f3f3f3;
  color: #333;
  align-self: flex-end;
  text-align: right;
}

.ai-message {
  border: 1px solid #e0e0e0;
  align-self: flex-start;
}

.ai-message .response-message {
  background-color: #d2dae9;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.response-message {
  font-size: 14px;
}

.clipBoard {
  position: absolute;
  bottom: 10px;
  left: -40px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.clipBoard button {
  padding: 5px;
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.clipBoard button:hover {
  opacity: 1;
}

.clipBoard svg {
  width: 20px;
  height: 20px;
  fill: #333;
}

.chatbot-input-wrapper {
  padding: 12px 15px;
  background-color: #f9f9f9;
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}

.actions-menu {
  position: relative;
  margin-right: 16px;
}

.actions-button {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  background-color: #438fe7;
}

.actions-button:hover {
  background-color: #103d4e;
  /* transform: translateY(-2px); */
}

.actions-dropdown {
  position: absolute;
  z-index: 1000;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
  padding: 10px;
  bottom: 100%;
  margin-bottom: 10px;
}

.action-item {
  display: flex;
  align-items: center;
  background-color: #f3f3f3;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-item:hover {
  background-color: #e0e0e0;
  /* transform: translateY(-2px); */
}

.chatbot-input-form {
  display: flex;
  width: 100%;
  align-items: center;
}

.chatbot-input-form input {
  flex-grow: 1;
  padding: 10px 16px;
  border: 1px solid #ccc;
  border-radius: 20px;
  margin-right: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.chatbot-input-form input:focus {
  outline: none;
  border-color: #888;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.toggle-wrapper {
  display: flex;
  align-items: center;
  margin-right: 12px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked+.slider {
  background-color: #2196F3;
}

input:checked+.slider:before {
  transform: translateX(18px);
}

.toggle-label {
  position: relative;
  cursor: default;
  margin-left: 8px;
  font-size: 12px;
  color: #555;
}

.toggle-label:after {
  content: "Toggle the tool, select a word or phrase, and click on 'Find Meaning' to display the meaning of the selected text.";
  position: absolute;
  bottom: 80%;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  padding: 8px;
  background-color: #333;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  font-size: 12px;
  visibility: hidden;
  opacity: 0;
  transition: opacity .3s, visibility .3s;
  z-index: 1000;
  white-space: normal;
  word-wrap: break-word;
  margin-bottom: 10px;
}

.toggle-label:hover::after {
  visibility: visible;
  opacity: 1;
}

.send-button {
  padding: 8px;
  background-color: transparent;
  color: #000;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.send-button:hover {
  background-color: #e0e0e0;
  /* transform: translateY(-2px); */
}

.send-button svg {
  width: 20px;
  height: 20px;
}

.selectable-text {
  cursor: text;
  user-select: text;
}

.find-meaning-popup {
  position: fixed;
  z-index: 1000;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 10px;
}

.find-meaning-button {
  display: flex;
  align-items: center;
  background-color: #f3f3f3;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.find-meaning-button:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
}

.find-meaning-button svg {
  margin-right: 8px;
  width: 18px;
  height: 18px;
}

.suggestions-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  padding-bottom: 12px;
}

.suggestion-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #333;
  flex: 1 0 calc(50% - 4px);
  min-width: 150px;
  max-width: calc(50% - 4px);
  display: flex;
  align-items: center;
  box-sizing: border-box;
}

.suggestion-card:hover {
  background-color: #e8e8e8;
}

.suggestion-text {
  flex: 1;
  white-space: normal;
  word-wrap: break-word;
  line-height: 1.4;
}

.close-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  z-index: 10;
}

.close-button svg {
  width: 20px;
  height: 20px;
  color: #333;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  width: 100%;
  height: 100%;
}

.modal-content {
  background-color: white;
  padding: 24px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  max-width: 90%;
  max-height: 90%;
  width: 900px;
  margin-left: 10%;
  overflow-y: auto;
  position: relative;
  height: auto;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
    align-items: center;
  }

  .reader-ai-panel {
    width: 100%;
    max-width: 800px;
    margin-right: 0;
    margin-bottom: 24px;
    height: auto;
    max-height: 300px;
  }

  .chatbot {
    width: 100%;
  }
}

@media (max-width: 600px) {
  .suggestion-card {
    flex: 1 0 100%;
    max-width: 100%;
  }

  .welcome-title {
    font-size: 20px;
  }

  .edit-button {
    font-size: 14px;
    padding: 8px;
  }

  .chatbot-input-form input {
    font-size: 14px;
  }

  .toggle-label {
    display: inline-block;
  }

  .toggle-label::after {
    width: 150px;
    font-size: 10px;
  }
}
</style>