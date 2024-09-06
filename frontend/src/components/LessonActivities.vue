<template>
  <div class="body-bg" >
    <div>
      <BackButton />
    </div>
    <div class="lesson-activities">
      <h2 class="heading">Word Play</h2>
      <textarea v-model="userInput" placeholder="Let's get started! Please type in some content to begin."></textarea>
      <div v-if="!loading" class="button-container">
      <button @click="proceedToWordplay" class="submit-btn">Generate Word Play</button>
      <button class="reset-btn" @click="refreshPage"> Reset </button>
      </div>
      <WordplayGame v-if="showWordplayGame" :initialContent="userInput" />
    </div>
    </div>
  </template>
  
  <script>
  import WordplayGame from './WordplayGame.vue';
  import BackButton from '../components/BackButton.vue';
  
  export default {
    name: 'LessonActivities',
    components: {
      BackButton,
      WordplayGame
    },
    data() {
      return {
        userInput: '',
        showWordplayGame: false,
        resetKey: 0
      };
    },
    methods: {
      refreshPage() {
    // Reload the current page
        window.location.reload();
    },
      proceedToWordplay() {
        if (this.userInput.trim() !== '') {
          this.showWordplayGame = false;
          this.$nextTick(() => {
              this.resetKey += 1; // Update the key to force a re-render
              this.showWordplayGame = true; // to generate quiz multiple times
        });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .title{
    text-align: center;
    margin-bottom: 10px;
    color: #888;
  }
  .lesson-activities {
    /* display: none; */
    width: 100%;
    padding: 0px 20px 20px 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
    /* margin-bottom: 5px; */
    margin-left: 20px;
    margin-right: 20px;
  }
  
  textarea {
    width: 100%;
    height: 100px;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background-color: #fff;
  }
  
  /* button {
    background-color: #dbdada;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    color: black;
    padding: 10px 20px;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 0px;
    margin-bottom: 10px;
  } */
   button{
    width: 20%;
    margin-right: 6px;
   }

  
  /* button:hover {
    background-color: #e2e1e1;
  } */
  </style>
  