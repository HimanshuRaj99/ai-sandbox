<template>
  <div class="body-bg">
    <div>
      <BackButton />
    </div> 
  <div class="synonym-swap-activity-container">
    <div class="synonym-swap-activity">
      <div class="form-header">
        <h2 class="heading">Synonym Swap</h2>
      </div>
      <p>Drag and drop the word from Word Bank that matches the <b><span class="highlight">highlighted</span></b> word in each sentence.</p>
      <div class="synonym-swap-container">
        <div class="word-bank">
          <h3>Word Bank</h3>
          <ul>
            <li v-for="word in wordBank" :key="word" class="word" draggable="true" @dragstart="dragStart(word)">
              {{ word }}
            </li>
          </ul>
        </div>

        <div class="sentences">
          <div v-for="(sentence, index) in formattedSentences" :key="index" class="sentence" @dragover.prevent @drop="dropWord(index)">
            <p v-html="highlightUnderlinedWord(sentence.text)"></p>
            <div class="drop-area" :class="{ filled: sentence.answer !== '' }">
              <span v-if="!sentence.answer">Drop here</span>
              <span v-else>{{ sentence.answer }}</span>
            </div>
            <button @click="showHint(index)" class="hint-button" :disabled="sentence.hintUsed || hintsLeft === 0">
              Hint
            </button>
            <span class="feedback" :class="{ correct: sentence.isCorrect, incorrect: !sentence.isCorrect && sentence.isAnswered }">
              {{ sentence.feedbackMessage }}
            </span>
            <span v-if="sentence.isCorrect" class="success-icon">🌟</span>
            <span v-if="sentence.hintUsed" class="hint-message">{{ sentence.hint }}</span>
          </div>
        </div>

        <div class="progress-bar-container">
          <progress-bar :progress="progress"></progress-bar>
          <span>{{ completedSentences }}/{{ formattedSentences.length }} Completed</span>
        </div>

        <div class="button-container">
          <button @click="submitAnswers" class="submit-btn" :disabled="!allAnswered">Submit</button>
          <button @click="resetActivity" class="reset-btn">Reset</button>
        </div>
      </div>

      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
      </div>

      <!-- Modal for CompletionScreen -->
      <div v-if="showCompletionScreen" class="modal-overlay">
        <div class="modal-content">
          <completion-screen 
            :correctAnswers="correctSentences" 
            :totalSentences="formattedSentences.length" 
            :timeTaken="timeTaken" 
            :starsEarned="starsEarned"
            @close="closeCompletionScreen"
          ></completion-screen>
        </div>
      </div>
     </div>
    </div>
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue';
import CompletionScreen from './CompletionScreen.vue';
import BackButton from '../components/BackButton.vue';

export default {
  components: {
    ProgressBar,
    CompletionScreen,
    BackButton
  },
  data() {
    return {
      wordBank: [],
      sentences: [],
      hintsLeft: 3,
      completedSentences: 0,
      correctSentences: 0,
      starsEarned: 0,
      startTime: null,
      timeTaken: 0,
      showCompletionScreen: false,
      draggedWord: null,
      isLoading: false,
    };
  },
  computed: {
    formattedSentences() {
      return this.sentences.map(sentence => ({
        text: sentence.original.replace(new RegExp(`(<b>(${sentence.originalWord})</b>)`, 'gi'), `<b class="synonym-word" style="text-decoration: underline; color: brown;">${sentence.originalWord}</b>`),
        underlinedWord: sentence.originalWord,
        answer: '',
        isCorrect: false,
        isAnswered: false,
        hintUsed: false,
        hint: `Think of a word that means "${sentence.originalWord}".`,
        feedbackMessage: ''
      }));
    },
    progress() {
      return (this.completedSentences / this.formattedSentences.length) * 100;
    },
    allAnswered() {
      return this.completedSentences === this.formattedSentences.length;
    },
  },
   mounted() {
    // Set a timer to close the completion screen after 15 seconds
    setTimeout(() => {
      this.closeCompletionScreen();
    }, 15000);
  },
  methods: {
    highlightUnderlinedWord(text) {
      console.log(text);
      return text.replace(/<b class="highlight synonym-word">(.*?)<\/b>/g, (match, p1) => `<span class="highlight synonym-word">${p1}</span>`);
    },
    dragStart(word) {
      this.draggedWord = word;
    },
    dropWord(index) {
      const sentence = this.formattedSentences[index];
      if (!sentence.isAnswered && this.draggedWord) {
        sentence.answer = this.draggedWord;
        this.validateAnswer(index, sentence.answer);
        this.draggedWord = null;
      }
    },
    validateAnswer(index, answer) {
      const sentence = this.formattedSentences[index];
      
      if (!sentence.isAnswered) {
        sentence.isAnswered = true;

        // Fetch the correct synonym from the sentences array
        const correctSynonym = this.sentences[index].synonym;

        // Compare the answer with the correct synonym
        if (answer && answer.toLowerCase() === correctSynonym.toLowerCase()) {
          sentence.isCorrect = true;
          sentence.feedbackMessage = "Correct!";
          this.correctSentences++;
          this.starsEarned++;
        } else {
          sentence.isCorrect = false;
          sentence.feedbackMessage = "Incorrect!";
        }
        this.completedSentences++;

        this.updateProgress();
      }
    },
    showHint(index) {
      if (this.hintsLeft > 0) {
        this.formattedSentences[index].hintUsed = true;
        this.hintsLeft--;
      }
    },
    updateProgress() {
      this.$forceUpdate(); // Update UI to reflect progress
    },
    submitAnswers() {
      // this.isLoading = true;
      console.log('Answers submitted');
      if (this.allAnswered) {
        this.timeTaken = Math.round((Date.now() - this.startTime) / 1000); // Calculate time in seconds
        this.showCompletionScreen = true;
      } else {
        alert('Please complete all sentences before submitting.');
      }
    },
    closeCompletionScreen() {
      this.showCompletionScreen = false;
    },
    resetActivity() {
      this.hintsLeft = 3;
      this.completedSentences = 0;
      this.correctSentences = 0;
      this.starsEarned = 0;
      this.timeTaken = 0;
      this.showCompletionScreen = false;
      this.draggedWord = null;
      this.sentences = this.sentences.map(sentence => ({
        ...sentence,
        answer: '',
        isCorrect: false,
        isAnswered: false,
        hintUsed: false,
        feedbackMessage: ''
      }));
      this.startTime = Date.now();
      this.$forceUpdate(); // Update UI to reflect the reset state
    }
  },
  created() {
    const queryParams = this.$route.query;
    if (queryParams.wordBank && queryParams.sentences) {
      try {
        this.wordBank = JSON.parse(queryParams.wordBank);
        this.sentences = JSON.parse(queryParams.sentences);
        this.startTime = Date.now();
      } catch (e) {
        console.error('Error parsing query parameters:', e);
      }
    }
  },
};
</script>

<style scoped>

.synonym-swap-activity-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.synonym-swap-activity {
  width: 100%;
  max-width: 800px;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-header {
  margin-bottom: 20px;
}

.site-title {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin: 0 0 5px 0;
}
button {
  width: 20%;
  margin-right: 6px;
}
/* .button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
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

.synonym-swap-container {
  width: 100%;
}

.word-bank {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.word-bank h3 {
  margin-bottom: 10px;
}

.word-bank ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.word-bank li {
  background-color: #e0e0e0;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.sentences .sentence {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sentence p {
  margin-bottom: 10px;
}

.drop-area {
  width: 100%;
  padding: 10px;
  border: 2px dashed #ccc;
  border-radius: 4px;
  text-align: center;
  background-color: #f8f8f8;
  margin-bottom: 10px;
  min-height: 40px;
}

.drop-area.filled {
  background-color: #e0f7fa;
}

.highlight {
  color: brown;
  font-weight: bold;
}

.hint-button {
  background-color: #ffa500;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  display: none;
}

.hint-button:disabled {
  background-color: #ddd;
}

.feedback {
  margin-top: 10px;
}

.correct {
  color: green;
}

.incorrect {
  color: red;
}

.success-icon {
  margin-left: 10px;
}

.hint-message {
  margin-top: 10px;
  color: #ffa500;
}

.progress-bar-container {
  width: 100%;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

/* .submit-button {
  background-color: #5a5a5ab4;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:disabled {
  background-color: #5a5a5ab4;
}

.submit-button:hover {
  background-color: #000;
}

.reset-button {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
  margin-left: 20px;
}

.reset-button:hover {
  background-color: #c82333;
} */

.submit-button,
.reset-button {
  width: 100%;
  max-width: 200px;
  padding: 10px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.submit-button:hover,
.reset-button:hover {
  background-color: #333;
}

.submit-button:disabled,
.reset-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.synonym-word {
  color: green;
  font-weight: bold;
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
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
}

</style>
