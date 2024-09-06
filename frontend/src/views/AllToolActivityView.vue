<template>
  <div>
  <div class="topic">
    All Tools and Activities
  </div>  
  <div>
    <CardToolActivity />
  </div>
  </div>
</template>

<script>
import CardToolActivity from '../components/CardToolActivity.vue'

export default {
  components: {
    CardToolActivity
  },
//   data() {
//     return {
//       cards: [
//         {
//           id: 1,
//           title: 'Image Generator',
//           description: 'Generate and edit images with AI from Adobe Express.',
//           isNew: true
//         },
//         {
//           id: 2,
//           title: 'Advanced Learning Plan (ALP)',
//           description: 'Generate draft of an Advanced Learning Plan (ALP) for a student.',
//           isNew: true
//         }
//       ]
//     }
//   }
}
</script>
<style>
.topic {
    margin : 50px 30px 10px 30px;
    font-size: 30px;
}
</style>