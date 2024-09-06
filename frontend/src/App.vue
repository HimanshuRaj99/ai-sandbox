<template>
  <v-app>
    <SidebarView v-if="isAuthenticated" />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import SidebarView from './components/SidebarView.vue';
import { LOCAL_STORAGE_KEYS } from '@/constants';

export default {
  components: {
    SidebarView,
  },
  data() {
    return {
      isAuthenticated: false,
    };
  },
  created() {
    this.checkAuthStatus();
  },
  methods: {
    checkAuthStatus() {
      this.isAuthenticated = localStorage.getItem(LOCAL_STORAGE_KEYS.IS_AUTHENTICATED) === 'true';
    },
  },
  watch: {
    $route() {
      this.checkAuthStatus();
    },
  },
};
</script>

<style>
  @font-face {
    font-family: 'Inter';
    src: url('./assets/fonts/Inter-VariableFont_opsz\,wght.ttf');
  }
  body {
    font-family: 'Inter', sans-serif;
  }
  .body-bg{
    display: flex;
    justify-content: center;
    align-items: flex-start;
    background-color: #f5f5f5;
    height: 98%; /* Adjust as needed */
    margin-top: 40px; /* Keep the margin-top if needed */
  }

  .heading{
    display: flex;
    font-size: 20px;
    font-weight: normal;
    justify-content: center;
    align-items: center;
    margin-top: 16px;
    margin-bottom: 16px;
    color: #212121;
  }

  .title{
    display: flex;
    font-size: 20px;
    justify-content: center;
    align-items: center;
    margin-top: 16px;
}

  .button-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
  .submit-btn{
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  color: white !important;
  font-size: 16px;
  cursor: pointer;
  /* box-shadow:  5px 5px 5px rgba(0, 0, 0, 0.349); */
  font-size: 16px;
  /* font-weight: bold; */
  background-color: #438FE7;
  }

  .submit-btn:hover {
    background-color: #103d4e;
  }

  .submit-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .reset-btn {
  display: inline-block;
  /* align-items: center; */
  padding: 6px 40px;
  border-style: solid;
  border: 2px solid #438FE7;
  width:126px;
  border-radius: 5px;
  background-color: #ffffff;
  color: #000000;
  font-size: 16px;
  /* font-weight: bold; *
  cursor: pointer;
  /* box-shadow:  5px 5px 5px rgba(0, 0, 0, 0.349); */
  margin-right: 6px;
  margin-left: 20px;
}
.reset-btn:hover {
  color: white;
  background-color: #438FE7;
}

.secondary-button {
  display: flex;
  margin-top: 20px;
  background-color: #ffffff;
  padding: 6px 40px;
  border-style: solid;
  border: 2px solid #438fe7; 
  border-radius: 5px;
  padding: 5px; 
  font-size: 16px;
  cursor: pointer;
  /* transition: all 0.3s ease; */
  color: #000000; 
  margin-left: auto;
}

.secondary-button:hover {
  background-color: #103d4e;
  /* transform: translateY(-2px); */
  color: #fff;
  border: 2px solid #fff;
}
</style>