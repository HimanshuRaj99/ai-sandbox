<template>
    <div className='back-button-container'>
        <button class="back-button" @click="goBack">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 26 26"
                fill="currentColor"
                class="back-icon"
            >
                <path d="M19 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.8 13H19v-2z" />
            </svg>
          Back
        </button>
      </div>
</template>
<script>
//import { cards } from './cardData.js'

export default {
    methods: {
    goBack() {
      this.$router.back();
    },
    // isActive(route) {
    //   return this.$route.path === route;
    // }
  }
}
</script>

<style>
.back-button-container {
    display: flex;
    margin-left: 260px ; 
    position: absolute;
    
    top: 10px;
    left: 0px;
}
/* .back-button-container:hover{
    background-color: rgb(190, 190, 62);
} */
.back-button {
    
    
    color: #1e2325f3;
    display: flex;
    align-items: center;
    font-size: 12px;
    padding: 2px 7px 2px 5px;
    cursor: pointer;
    border-radius: 20px;
    border: 1px solid #ffffff;
    background-color: #fffefe;
}
.back-button:hover{
    background-color: rgb(187, 187, 187);
}
.back-icon {
    color: rgb(7, 7, 7);
    width: 20px;
    height: 20px;
    margin-right: 2px;
}
</style>