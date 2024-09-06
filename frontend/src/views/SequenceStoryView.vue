<template>
  <div class="body-bg">
  <div>
    <BackButton/>
  </div>
  <div class="sequence-story-activity">
    <h1 class="heading">Story Sequence Activity</h1>

    <div class="content-wrapper">
      <div class="story-section">
        <h2>{{ storyTitle }}</h2>
        <img :src="imagePath" alt="{{storyTitle}}" class="story-image">
        <p class="story-text">{{ story }}</p>
      </div>

      <div class="sequence-section">
        <h2>Arrange the Events</h2>
        <p class="instructions">Drag and Drop the events to put them in the correct order!</p>
        <draggable 
          v-model="userSequence" 
          group="sequence" 
          @start="drag=true" 
          @end="drag=false" 
          item-key="id"
          class="sequence-list"
        >
          <template #item="{ element }">
            <div class="sequence-item">
              {{ element.content }}
            </div>
          </template>
        </draggable>

        <button @click="checkAnswer" class="submit-btn">
          Check Answer
        </button>

        <p v-if="feedback" class="feedback" :class="{ 'correct': isCorrect, 'incorrect': !isCorrect }">
          {{ feedback }}
        </p>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import image from '@/assets/flux_img.png';
import BackButton from '../components/BackButton.vue';
export default {
  name: 'SequenceStoryView',
  components: {
    draggable,
    BackButton
  },
  data() {
    return {
      storyTitle : this.$route.query.title,
      story :  this.$route.query.story,
      sequenceOrder : this.$route.query.sequenceOrder,
      correctSequence: [],
      userSequence: [],
      feedback: '',
      isCorrect: false,
      imagePath: image,
      drag: false
    };
  },
  created() {
    const sequenceOrder =JSON.parse(this.sequenceOrder);
    console.log("sequenceOrder : ", typeof(this.sequenceOrder))
      this.correctSequence = sequenceOrder.map(item => ({
        id: item.sequenceNumber,
        content: item.sequence,
      }));
    console.log(" correctSequence :",this.correctSequence)
    this.userSequence = [...this.correctSequence].sort(() => Math.random() - 0.5);
  },
  methods: {
    checkAnswer() {
      const isSequenceCorrect = this.userSequence.every((item, index) => item.id === index + 1);
      this.isCorrect = isSequenceCorrect;
      this.feedback = isSequenceCorrect
        ? "Great job! You've arranged the events correctly!"
        : "Oops! That's not quite right. Try again!";
    }
  }
}
</script>
<style scoped>
.sequence-story-activity {
  font-family: 'Comic Sans MS', cursive, sans-serif;
  max-width: 1000px;
  margin-top: 20px;
  /* margin: 0 auto; */
  padding: 0px 20px 20px 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.title {
  text-align: center;
  /* text-transform: capitalize; */
  color: #4a4a4a;
  font-size: 30px;
  margin-bottom: 20px;
}
.content-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.story-section, .sequence-section {
  flex: 1;
  min-width: 300px;
  background-color: white;
  padding: 20px;
  margin-top:10px;
  border: 1px solid #438FE7;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
h2 {
  color: #438FE7;
  font-size: 20px;
  margin-bottom: 15px;
}
.story-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 15px;
}
.story-text {
  line-height: 1.6;
  color: #4a4a4a;
}
.instructions {
  font-style: italic;
  margin-bottom: 10px;
  color: #7a7a7a;
}
.sequence-list {
  min-height: 200px;
  background-color: #e6f2ff;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 10px;
}
.sequence-item {
  background-color: #fff;
  border: 1px solid #438FE7;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  cursor: move;
  transition: background-color 0.3s;
}
.sequence-item:hover {
  background-color: #f5f5f5;
}
.check-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #23d160;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 15px;
}
.check-button:hover {
  background-color: #20bc56;
}
.feedback {
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
}
.feedback.correct {
  background-color: #effaf5;
  color: #257942;
}
.feedback.incorrect {
  background-color: #feecf0;
  color: #cc0f35;
}
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
}
</style>