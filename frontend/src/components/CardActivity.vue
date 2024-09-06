<template>
  <div class="card-container">
    <div v-for="activity in activities" :key="activity.id" class="card"
    @click="navigate(activity.route)"
    :to="activity.route"
    >
    
      <div class="card-content">
        <div class="icon" v-html="activity.icon"></div>
        <div class="text">
          <h3>{{ activity.title }}</h3>
          <p>{{ activity.description }}</p>
        </div>
      </div>
      
        <!-- <div class="card-actions">
          <span v-if="activity.isNew" class="new-tag">NEW!</span>
          <span class="star-icon">☆</span>
        </div> -->
      
    </div>
  </div>
</template>

<script>
import { cards } from './cardData.js'

export default {
  data() {
    return {
      cards,
      activities: [],
      
    //   console.log(cards);
      
     };
     
    },
    created() {
    // Initialize cards data
    this.cards = cards;
    // Assign values from cards array to activities array
    this.activities = this.cards
    .filter(card => {
      return card.isActivity === true;
    }).map(card => card); // Using map for a direct copy
  },

    
 
    methods: {
    navigate(route) {
      this.$router.push(route);
    },
    isActive(route) {
      return this.$route.path === route;
    }
  }
}
</script>

<style scoped>
.card-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 16px;
  background-color: #f0f0f0; 
}
.card-container .card {
cursor: pointer;
}
.card:hover{
  background-color: rgb(207, 207, 203);
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 16px;
  display: flex;
  justify-content: space-between;
}

.card-content {
  display: flex;
  align-items: center;
}

.icon {
  margin-right: 16px;
  width: 40px;
  height: 40px;
}

.text h3 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.text p {
  margin: 4px 0 0;
  font-size: 14px;
  color: #666;
}

.card-actions {
  display: flex;
  align-items: center ;
  
}

.new-tag {
  
  background-color: #acaca6;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-right: 8px;
}

.star-icon {
  font-size: 20px;
  color: #ddd;
}
</style>