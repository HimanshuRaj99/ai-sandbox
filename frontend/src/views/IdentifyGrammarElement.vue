<template>
  <div class="body-bg">
    <div>
      <BackButton />
    </div>
  <div class="svp-container">
    <h3 class="heading ">Identify Subject and Predicate</h3>
    <form @submit.prevent="submitParagraph">
      <textarea class="centered-textarea" v-model="paragraph" placeholder="Enter the text here..." rows="4" required></textarea>
      <div v-if="!loading" class="button-container">
        <button class="submit-btn" type="submit">Generate Quiz</button>
        <button class="reset-btn" @click="refreshPage"> Reset</button>
      </div>
    </form>
    <div v-if="loading" class="loading-overlay" >
          <div class="loading-spinner"></div>
       </div>
    <div class="activity-container">
    <div v-if="sentencesLen > 0" class="activity-box">
      <p>Drag and drop the <i>Subject</i> and <i>Predicate</i> parts of the sentence with the correct category.</p>
      <div v-for="(sentence, index) in sentences" :key="index">
        <p class = "sentence-val">{{ index + 1 }}. {{ sentence.sentence }} </p>
        <div class= "sentence-parts-container">
          <div class="sentence-parts">
              <div class="labels">
                <div class="sub">Subject</div>
                <div class="pred">Predicate</div>
              </div>
            <draggable v-model="draggableLists[index]" :options="dragOptions" class="draggable-box">
              
              <template #item="{element}">
                <div >
                  <div :key="element.id" class="draggable-item">
                    {{ element.text }}
                  </div>
                </div>
              </template>
            </draggable>

          </div>           
          <div class="result-message">
              <div v-if="sentence.isCorrect === false" class="result-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 500 512" fill-rule="evenodd" clip-rule="evenodd">
                  <path fill="#EB0100" d="M317.99 323.62c-17.23-19.89-35.3-40.09-54.23-60.09-62.06 59.35-119.53 126.18-161.12 201.73-51.02 92.68-126.31 16.84-92.15-50.33 27.46-61.28 98.07-146.3 182.94-220.07-46.74-41.72-97.97-79.34-154.08-107.07C-42.76 47.2 19.97-20.82 79.37 6.16c50.04 19.82 119.09 70.85 182.26 134.32 63.11-45.86 129.55-81.8 189.45-95.87 13-3.06 50.95-11.33 59.69 1.04 3.29 4.67-.33 11.68-7.08 19.29-22.99 25.96-84.78 67.12-114.72 90.82-21.61 17.11-43.55 34.99-65.37 53.71 23.2 28.81 43.94 58.64 60.47 88.17 14.37 25.66 25.55 51.1 32.42 75.46 3.14 11.13 11.75 43.64 1.38 51.66-3.91 3.03-10.11.16-16.95-5.38-23.34-18.89-61.29-70.77-82.93-95.76z"/>
                </svg>
                <p style="color: red;">Incorrect, Please try again.</p>
              </div>
              <div v-if="sentence.isCorrect === true" class="result-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="20" viewBox="-40 0 182.8 109.76">
                  <path fill="#01A601" d="M0,52.88l22.68-0.3c8.76,5.05,16.6,11.59,23.35,19.86C63.49,43.49,83.55,19.77,105.6,0h17.28 C92.05,34.25,66.89,70.92,46.77,109.76C36.01,86.69,20.96,67.27,0,52.88L0,52.88z"/>
                </svg>
                <p style="color: green;">Correct!</p>
              </div>
            </div>

        </div>
      </div>
      <div class="submit-container">
        <button class="submit-btn" @click="submitAnswer">Submit</button>
        <div v-if="result !== null" class="score-container">
          <div class="score-box correct" >
            <div class="score-value">{{ correctCount }}</div>
            <div class="score-label">Correct</div>
          </div>
          <div class="score-box incorrect">
            <div class="score-value">{{ incorrectCount }}</div>
            <div class="score-label">Incorrect</div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
  </div>
</template>
 <script>
 import draggable from 'vuedraggable';
 import BackButton from '../components/BackButton.vue';
 import { API_ENDPOINTS, BASE_URL } from '@/constants';

export default {
  components: {
    draggable,
    BackButton
  },
  data() {
    return {
      paragraph: "",
      sentences: [],  // Array of sentence components
      draggableLists: [],  // List of draggable items for each sentence
      correctOrder: [],  // The correct order of all components
      result: null,
      sentencesLen: 0,
      dragOptions: {
      animation: 200
      },
      gradeLevel: this.$route.query.gradeLevel,
      model: this.$route.query.model,
      standard: this.$route.query.standard, 
      numQuestions: this.$route.query.numQuestions,
      loading: false,
    };
  },
  methods: {
    shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  },
  refreshPage() {
      // Reload the current page
      window.location.reload();
    },
    async submitParagraph() {
      console.log("gradeLevel : ",this.gradeLevel)
      const payload = {
        paragraph: this.paragraph,
        gradeLevel: this.gradeLevel,
        model: this.model,
        standard: this.standard, 
        numQuestions: this.numQuestions
      };
      console.log("payload: ", payload);
      this.loading = true;
      try{
        const response = await fetch(`${BASE_URL}${API_ENDPOINTS.SVP}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      console.log(response);
      const data = await response.json();
      console.log("print data : ",data)
      this.sentences = data.sentences;
      console.log("sentence : ",this.sentences)
      this.sentencesLen = this.sentences.length;
      this.correctOrder = data.correctOrder;
      console.log("sentence val : ", this.sentences[0].sentence)
      
      console.log("draggable list : ",this.draggableLists);
      console.log("length of sentences len : ", this.sentencesLen);
      this.draggableLists = this.sentences.map(sentence => {
      const items = [
        { id: `sub-${sentence.subject}`, text: sentence.subject },
        { id: `pred-${sentence.predicate}`, text: sentence.predicate }
      ];
      console.log("draggable list : ",this.draggableLists)
      return this.shuffleArray(items); // Shuffle items here
    });
      this.result = null; 
    } catch (error) {
          console.error('Error calling the API:', error);
          this.errorMessage = 'An error occurred while fetching data. Please try again later.';
        } finally {
            this.loading = false;  // Set loading to false
        }
    },

    onDragStart(event, sentenceIndex, type) {
      event.dataTransfer.setData('text/plain', JSON.stringify({ sentenceIndex, type }));
    },

    onDrop(event, sentenceIndex, type) {
      const data = JSON.parse(event.dataTransfer.getData('text/plain'));
      const sourceIndex = data.sentenceIndex;
      const sourceType = data.type;

      if (!this.droppedItems[sentenceIndex]) {
        this.$set(this.droppedItems, sentenceIndex, {});
      }

      if (sourceIndex !== undefined) {
        // If dragged from another drop zone
        const temp = this.droppedItems[sourceIndex][sourceType];
        this.$set(this.droppedItems[sourceIndex], sourceType, this.droppedItems[sentenceIndex][type]);
        this.$set(this.droppedItems[sentenceIndex], type, temp);
      } else {
        // If dragged from the sentence display
        this.$set(this.droppedItems[sentenceIndex], type, this.sentences[sentenceIndex][type]);
      }
    },

   async  submitAnswer() {
    let isCorrect = true;
    let correctCount = 0;
    let incorrectCount = 0;

    this.sentences.forEach((sentence, index) => {
      const userOrder = this.draggableLists[index].map(item => item.text);
      const correctOrder = [
        sentence.subject,
        sentence.predicate
      ];

      // Check if the user's order matches the correct order
      for (let i = 0; i < 3; i++) {
        if (userOrder[i] !== correctOrder[i]) {
          isCorrect = false;
          this.sentences[index].isCorrect = false;
          incorrectCount++;
          break;
        }
      }

      if (isCorrect) {
        this.sentences[index].isCorrect = true;
        correctCount++;
      }

      isCorrect = true;
    });

    this.result = correctCount === this.sentences.length;
    this.correctCount = correctCount;
    this.incorrectCount = incorrectCount;
  }
}
};
</script>


<style scoped>
./* Mobile styles */
@media (max-width: 767px) {

  .centered-textarea {
    width: 90%;
  }

  .draggable-item {
    margin-left: 100px;
    margin-right: 100px;
    width: 70%;
  }

  .labels {
    width: 80px;
  }

  .labels div {
    padding: 8px;
    font-size: 12px;
    margin-left: 40px;
  }

  .score-box {
    padding: 8px 16px;
  }

  .score-value {
    font-size: 18px;
  }

  .score-label {
    font-size: 12px;
  }
}

/* Tablet styles */
@media (min-width: 768px) and (max-width: 1023px) {
  /* .svp-container{
    margin-top:40px;
  } */
  .centered-textarea {
    width: 85%;
  }

  .draggable-item {
    /* margin-left: 150px;
    margin-right: 150px;
    width: 60%; */
  }

  .labels {
    width: 90px;
  }

  .labels div {
    padding: 10px;
    font-size: 14px;
  }

  .score-box {
    padding: 10px 18px;
  }

  .score-value {
    font-size: 20px;
  }

  .score-label {
    font-size: 13px;
  }
}

/* Desktop styles */
@media (min-width: 1024px) {
  .centered-textarea {
    width: 80%;
  }

  .draggable-item {
    /* margin-left: 200px;
    margin-right: 200px;
    width: 50%; */
  }

  .labels {
    /* width: 100px; */
  }

  .labels div {
    /* padding: 12px; */
    font-size: 16px;
  }

  .score-box {
    padding: 12px 22px;
  }

  .score-value {
    font-size: 24px;
  }

  .score-label {
    font-size: 15px;
  }
}
/* .title{
   display: flex;
    font-size: 20px;
    justify-content: center;
    align-items: center;
    margin-top: 16px;
} */
.submit-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}
.svp-container{
  width: 80%;
  margin-top:20px;
  background-color: white;
  padding:0px 20px 20px 20px;
  border-radius: 8px;
}
.score-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
.result-message {
  /* flex: 2; */
  display: flex;
  /* justify-content: center;
  align-items: center; */
  height: 10px;
  /* text-align: center; */
  margin-left: 10px;
}

.result-message p {
  margin: 0;
}

.result-icon-container {
  display: flex;
  align-items: center;
  /* width: 80%; */
}

.score-box  {
  background-color: #5bce78;
  border-radius: 5px;
  padding: 10px 10px;
  width: 100px;
  text-align: center;
  margin: 20px 10px 0px 0px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  animation: score-bounce 0.5s ease-in-out;
}
.correct{
  background-color: #52ef46;
}
.incorrect{
  background-color: #ff5757;
}
.score-value {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

.score-label {
  font-size: 14px;
  color: #ffffff;
}

@keyframes score-bounce {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }
  50% {
    transform: translateY(5px);
    opacity: 1;
  }
  100% {
    transform: translateY(0);
  }
}


/* h2 {
  display: flex;
  font-size: 20px;
  justify-content: center;
  align-items: center;
  color: #696969;
  margin-top: 40px;
} */
p{
  padding: 10px;
}
.centered-textarea {
  display: block;
  margin: 0 auto;
  width: 80%;
  background-color: white;
  max-width: 800px;
  min-width: 300px;
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  resize: both;
  margin-top: 10px;
}

button {
  width: 20%;
  margin-right: 6px;
}
/* .reset {
  display: inline-block;
  padding: 6px 40px;
  border: none;
  width:126px;
  border-radius: 5px;
  background-color: #8f8f8f;
  color: white;
  font-size: 16px;
  cursor: pointer;
  box-shadow:  5px 5px 5px rgba(0, 0, 0, 0.349);
  margin-right: 6px;
  margin-left: 4px;
}
.reset:hover {
  background-color: #080808;
} */

.button:hover {
  background-color: #080808;
}

.loading-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px; 
  margin-top: 14px;
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
  /* z-index: 1000; */
  margin: 5px 100px 0px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.activity-container{
    display: flex;
    justify-content: center;
    margin-top: 30px;
}
.activity-box{
  /* padding: 20px 50px 50px 50px; */
  width: 80%;
}
.sentence-parts-container {
  background-color:#ffffff ;
  /* border: 1px 200px 1px 20px solid #ccc; */
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 10px;
  /* width: 100; */
  margin-bottom: 20px;
}
.sentence-parts {
  /* background-color:#2cbb44; */
    /* display: flex; */
    display: flex;
    justify-content: space-between;
    background-color: #fff;
    padding: 10px;
    border: 2px #000;
  /* align-items: stretch;
  margin-bottom: 20px; */
}
.sentence-val{
  background-color: #dee5ff;
  font-size: 16px;
  font-weight: 400;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}
.labels {
  /* flex:1;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 100px;
  margin-right: 10px; */
}

.labels div {
  padding: 10px;
  /* background-color: #f9f9f9; */
  border: 1px solid #a5a5a5;
  border-radius: 8px;
  margin-bottom: 20px;
  
  /* box-shadow:5px 5px 5px 5px rgba(0, 0, 0, 0.1); */
  /* border: 1px solid #555555;
  border-radius: 8px; */
  /* margin-bottom: 5px; */
  box-shadow: #080808;
  /* text-align: right; */
}
.sub{
  background-color: #D1E9F6;
  font-weight: 600;
  box-shadow:5px 5px 5px 5px rgb(16 98 113 / 15%);
}

.pred{
  background-color:#F1D3CE;
  font-weight: 600;
  box-shadow:5px 5px 5px 5px rgb(251 226 218 / 83%);
}
.draggable-box{
  /* flex: 6; */
  /* width: 2000px;*/
  width: 80%;
  
}
.draggable-item {
  display: flex;
  padding: 10px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  box-shadow:5px 5px 5px 5px rgba(0, 0, 0, 0.1);
  /* margin: 5px; */
  background-color: #f9f9f9;
  /* margin-left: 250px;
  margin-right: 250px; */
  /* width : 90%; */
  margin-bottom: 20px;
  cursor: pointer; 
}
.draggable-item.correct {
  background-color: green;
  color: white;
}

.draggable-item.incorrect {
  background-color: red;
  color: white;
}

.result {
  margin-left: 10px;
}
.container {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.paragraph-input {
  width: 80%;
  height: 100px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  resize: vertical;
}

/* .submit-btn {
  display: inline-block;
  padding: 6px 40px;
  border: none;
  width:126px;
  border-radius: 5px;
  background-color: #8f8f8f;
  color: white;
  font-size: 16px;
  cursor: pointer;
  box-shadow:  5px 5px 5px rgba(0, 0, 0, 0.349);
  margin-right: 6px;
  margin-left: 4px;
} */

.quiz-section {
  width: 100%;
}

.sentences-display {
  margin-bottom: 20px;
}

.sentence-row {
  margin-bottom: 10px;
}

.sentence-parts {
  display: flex;
  justify-content: space-between;
  background-color: #ffffff;
  padding: 10px;
  border: 2px black;
}

.part-box {
  border: 1px solid #ccc;
  padding: 5px;
  background-color: white;
  cursor: move;
}

.drop-zones-container {
  margin-bottom: 20px;
}

.sentence-drop-zones {
  margin-bottom: 15px;
}

.drop-zones {
  display: flex;
  justify-content: space-between;
}

.drop-zone {
  width: 30%;
  height: 40px;
  border: 2px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.dropped-item {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #3498db;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>