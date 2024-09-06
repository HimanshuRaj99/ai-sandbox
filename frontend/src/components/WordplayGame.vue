<template>
  <div class="wordplay-container">
    <div v-if="loading" class="loading-screen">
      <div class="loader"></div>
    </div>
    <template v-else>
      <div class="wordplay-game">
        <p>Select a word from each column to make a real word. Let's Play!</p>
        <div class="word-grid">
          <div class="cube-column" v-for="(cubeArray, type) in { prefix: shuffledPrefixes, root: shuffledRoots, suffix: shuffledSuffixes }" :key="type">
            <div
              v-for="cube in cubeArray"
              :key="cube.uniqueId"
              @click="toggleCube(cube)"
              :class="['cube', `${type}-cube`, { 'selected': selectedCubes.includes(cube), 'disabled': cube.disabled, 'incorrect': cube.incorrect, 'correct': cube.correct }]"
            >
              {{ cube.value }}
            </div>
          </div>
        </div>
        <div class="feedback" v-if="feedback">
          {{ feedback }}
        </div>
      </div>
      <div class="wordplay-results">
        <h3>Word</h3>
        <div class="canvas" v-if="correctWord">
          <div class="correct-word">
            <div class="word-cube">{{ correctWord.word }}</div>
          </div>
          <p class="word-meaning"><strong>Amazing! You built a real word. It means:</strong></p>
          <p class="word-definition">{{ correctWord.meaning }}</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from 'axios';
import { API_ENDPOINTS, BASE_URL } from '@/constants';

export default {
  name: 'WordplayGame',
  props: {
    initialContent: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      wordplayData: null,
      shuffledPrefixes: [],
      shuffledRoots: [],
      shuffledSuffixes: [],
      selectedCubes: [],
      correctWord: null,
      feedback: '',
      counter: 0,
    };
  },
  mounted() {
    this.fetchWordplayData();
  },
  methods: {
    async fetchWordplayData() {
      try {
        const response = await axios.post(`${BASE_URL}${API_ENDPOINTS.ACTIVITIES}`, {
          type: 'wordplay',
          content: this.initialContent
        });

        this.wordplayData = response.data.filter(word => word.prefix && word.root && word.suffix);
        this.prepareWordplayGame();
        this.loading = false;
      } catch (error) {
        console.error('Error fetching wordplay data:', error);
        this.feedback = 'Failed to load wordplay activity. Please try again.';
        this.loading = false;
      }
    },
    prepareWordplayGame() {
      const prefixes = this.wordplayData.map((wordData, index) => ({
        value: wordData.prefix,
        type: 'prefix',
        disabled: false,
        incorrect: false,
        correct: false,
        wordId: wordData.id || index,
        uniqueId: `prefix-${index}-${wordData.id || index}`
      }));
      const roots = this.wordplayData.map((wordData, index) => ({
        value: wordData.root,
        type: 'root',
        disabled: false,
        incorrect: false,
        correct: false,
        wordId: wordData.id || index,
        uniqueId: `root-${index}-${wordData.id || index}`
      }));
      const suffixes = this.wordplayData.map((wordData, index) => ({
        value: wordData.suffix,
        type: 'suffix',
        disabled: false,
        incorrect: false,
        correct: false,
        wordId: wordData.id || index,
        uniqueId: `suffix-${index}-${wordData.id || index}`
      }));

      this.shuffledPrefixes = this.shuffleArray(prefixes);
      this.shuffledRoots = this.shuffleArray(roots);
      this.shuffledSuffixes = this.shuffleArray(suffixes);
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    toggleCube(cube) {
      if (cube.disabled || cube.correct) return;

      const selectedPrefix = this.selectedCubes.find(c => c.type === 'prefix');
      const selectedRoot = this.selectedCubes.find(c => c.type === 'root');

      if (cube.type === 'root' && !selectedPrefix) {
        this.feedback = "Please select a prefix first.";
        return;
      }

      if (cube.type === 'suffix' && !selectedRoot) {
        this.feedback = "Please select a root first.";
        return;
      }

      const index = this.selectedCubes.findIndex(c => c.uniqueId === cube.uniqueId);
      if (index > -1) {
        this.selectedCubes.splice(index, 1);
      } else {
        const existingCubeOfSameType = this.selectedCubes.find(c => c.type === cube.type);
        if (existingCubeOfSameType) {
          const existingIndex = this.selectedCubes.findIndex(c => c.uniqueId === existingCubeOfSameType.uniqueId);
          this.selectedCubes.splice(existingIndex, 1);
        }
        this.selectedCubes.push(cube);
      }

      this.checkWord();
    },
    checkWord() {
      const selectedWord = this.wordplayData.find(wordData =>
        this.selectedCubes.length === 3 &&
        this.selectedCubes.some(cube => cube.type === 'prefix' && cube.value === wordData.prefix) &&
        this.selectedCubes.some(cube => cube.type === 'root' && cube.value === wordData.root) &&
        this.selectedCubes.some(cube => cube.type === 'suffix' && cube.value === wordData.suffix)
      );

      if (selectedWord) {
        this.counter++;
        this.correctWord = {
          prefix: selectedWord.prefix,
          root: selectedWord.root,
          suffix: selectedWord.suffix,
          word: selectedWord.word,
          meaning: selectedWord.meaning
        };
        this.feedback = "Congratulations, you are correct!";
        if (this.counter === this.wordplayData.length) {
          this.feedback = "Bravo, You did it. You've completed all the words!";
        }
        this.selectedCubes.forEach(cube => {
          cube.correct = true;
          cube.disabled = true;
          this.updateCubeState(cube, { correct: true, disabled: true });
        });
        this.selectedCubes = [];
      } else if (this.selectedCubes.length === 3) {
        this.correctWord = null;
        this.selectedCubes.forEach(cube => {
          cube.incorrect = true;
          this.updateCubeState(cube, { incorrect: true });
        });
        this.feedback = "Almost there! Give it another try, you can do it!";
        setTimeout(() => {
          this.selectedCubes.forEach(cube => {
            cube.incorrect = false;
            this.updateCubeState(cube, { incorrect: false });
          });
          this.selectedCubes = [];
        }, 1000);
      }
    },
    updateCubeState(cube, newState) {
      const cubeArrays = {
        prefix: this.shuffledPrefixes,
        root: this.shuffledRoots,
        suffix: this.shuffledSuffixes
      };

      const index = cubeArrays[cube.type].findIndex(c => c.uniqueId === cube.uniqueId);
      if (index !== -1) {
        Object.assign(cubeArrays[cube.type][index], newState);
      }
    }
  }
};
</script>

<style scoped>
.wordplay-container {
  display: flex;
  margin-top: 20px;
  justify-content: space-between;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  width: 100%;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
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

.wordplay-game {
  flex: 1;
  margin-right: 20px;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

p {
  color: #333;
  margin-bottom: 5px;
}

.word-grid {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.cube-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex: 1;
  border: 1px solid #b4a3a3;
  border-radius: 10px;
  padding: 15px;
}

.cube {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
  border: 1px solid #ccc;
}

.word-cube {
  text-transform: capitalize;
  font-size: 20px;
  font-weight: bold;
}

.prefix-cube {
  background-color: #D6A8E0;
}

.root-cube {
  background-color: #F5A3B6;
}

.suffix-cube {
  background-color: #FFA07A;
}

.cube.selected {
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  background-color: #4f83cc;
  color: #fff;
}

.cube.disabled {
  background-color: #f0f0f0 !important;
  cursor: not-allowed;
  color: #999;
}

.cube.incorrect {
  background-color: #ee5656;
  color: #fff;
}

.cube.correct {
  background-color: #90EE90 !important;
  cursor: not-allowed;
  color: #000000;
}

.feedback{
    /* margin-top: 0; */
    font-weight: normal;
    font-size: 16px;
}

.wordplay-results {
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  width: 300px;
}

.wordplay-results h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.canvas {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
}

.correct-word {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.correct-word .cube {
  width: 70px;
  height: 60px;
  font-size: 14px;
  padding: 10px;
}

.word-meaning {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

.word-definition {
  font-size: 14px;
  color: #333;
}
</style>