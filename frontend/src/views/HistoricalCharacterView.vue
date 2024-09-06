<template>
  <div class="body-bg">
  <div>
    <BackButton />
  </div>
  <div class="historical-character">
    
    <HistoricalCharacterForm />
  </div>
  </div>
</template>

<script>
import HistoricalCharacterForm from '@/components/HistoricalCharacterForm.vue';
import BackButton from '../components/BackButton.vue';
export default {
  components: {
    HistoricalCharacterForm,
    BackButton
  }
}
</script>

<style scoped>

.historical-character {
  /* margin-top: 40px; */
  width: 60%;
  display: grid;
  flex-direction: column;
  align-items: flex-start;
  /* padding: 20px; */
  
}
</style>