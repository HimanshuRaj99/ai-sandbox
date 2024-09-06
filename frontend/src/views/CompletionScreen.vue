<template>
    <div class="completion-screen">
      <div class="celebration">
        <h2>{{ finalResult() }}</h2>
        <p>You completed the activity!</p>
        <p>You answered <strong>{{ correctAnswers }}</strong> out of <strong>{{ totalSentences }}</strong> sentences correctly.</p>
        <p>Time Taken: <strong>{{ timeTaken }} seconds</strong></p>
        <p>Stars Earned: <strong>{{ starsEarned }}</strong> 🌟</p>
        <div class="confetti"></div>
      </div>
      <button class="submit-btn" @click="$emit('close')">Close</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      correctAnswers: {
        type: Number,
        required: true
      },
      totalSentences: {
        type: Number,
        required: true
      },
      timeTaken: {
        type: Number,
        required: true
      },
      starsEarned: {
        type: Number,
        required: true
      }
    },
    mounted() {
      this.launchConfetti();
    },
    methods: {
      finalResult() {
        const percentage = (this.correctAnswers / this.totalSentences) * 100;

        if (percentage === 100) {
          return "Congratulations !!";
        } else if (percentage >= 70) {
          return "Great job !!";
        } else if (percentage >= 50) {
          return "Good effort !!";
        } else {
          return "Don't give up !!";
        }
      },
      launchConfetti() {
        const confettiElement = this.$el.querySelector('.confetti');
        // Simple confetti animation - You can replace this with a more sophisticated library like 'canvas-confetti'
        confettiElement.classList.add('show');
        setTimeout(() => {
          confettiElement.classList.remove('show');
        }, 5000);
      }
    }
  };
  </script>
  
  <style scoped>
  .completion-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f0f0f0;
    border-radius: 10px;
    padding: 40px;
    margin: 20px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .celebration h2 {
    color: #28a745;
    font-size: 36px;
    margin-bottom: 20px;
  }
  
  .celebration p {
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  .confetti {
    width: 100%;
    height: 200px;
    background-image: url('@/assets/confetti.gif');
    /* background-repeat: no-repeat; */
    background-position: center;
    background-size: contain;
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
  }
  
  .confetti.show {
    opacity: 1;
  }

  .close {
    width: 100%;
    padding: 10px;
    background-color: #000;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 700;
    margin-top: 5%
  }
  </style>
  