<template>
    <div>
      <SynonymSwapInput @synonym-swap-generated="handleSynonymSwapGenerated" />
      <SynonymSwapActivity
        v-if="synonymSwapData"
        :word-bank="synonymSwapData.word_bank"
        :sentences="formattedSentences"
      />
    </div>
  </template>
  
  <script>
  import SynonymSwapInput from './views/SynonymSwapInput.vue';
  import SynonymSwapActivity from './views/SynonymSwapActivity.vue';
  
  export default {
    components: {
      SynonymSwapInput,
      SynonymSwapActivity
    },
    data() {
      return {
        synonymSwapData: null,
      };
    },
    computed: {
      formattedSentences() {
        if (!this.synonymSwapData) return [];
  
        return this.synonymSwapData.sentences.map(sentence => ({
          text: sentence.original.replace(sentence.synonym, `<u>${sentence.synonym}</u>`),
          underlinedWord: sentence.synonym
        }));
      }
    },
    methods: {
      handleSynonymSwapGenerated(data) {
        console.log('Received data in SynonymSwapPage:', data);
        this.synonymSwapData = data;
      }
    },
    mounted() {
       console.log('SynonymSwapPage mounted, synonymSwapData:', this.synonymSwapData);
    }
  };
  </script>
  
  <style scoped>
  /* Add any parent-specific styling here */
  </style>
  