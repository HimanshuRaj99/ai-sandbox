<template>
  <div>
  <!-- <div>
    <BackButton />
  </div> -->
  <div class="topic">
    Tools
  </div>  
  <div>
    <CardTools />
  </div>
  </div>
</template>

<script>
import CardTools from '@/components/CardTools.vue';
// import BackButton from '../components/BackButton.vue';
export default {
  components: {
    CardTools,
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