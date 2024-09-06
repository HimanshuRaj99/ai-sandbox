<template>
  <div>
  <!-- <div>
    <BackButton />
  </div> -->
  <div class="topic">
    Activities
  </div>  
  <div>
    <CardActivity />
  </div>
  </div>
</template>

<script>
import CardActivity from '@/components/CardActivity.vue';
// import BackButton from '../components/BackButton.vue';
export default {
  components: {
    CardActivity,
    // BackButton
  },
}
</script>
<style>
.topic {
    margin : 50px 30px 10px 30px;
    font-size: 30px;
}
</style>