<!-- CopyToClipboardButton.vue -->
<template>
  <button @click="copyToClipboard" class="copy-button" :title="buttonText">
    <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00cc00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
  </button>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      buttonText: 'Copy',
      copied: false
    };
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.text).then(() => {
        this.buttonText = 'Copied!';
        this.copied = true;
        setTimeout(() => {
          this.buttonText = 'Copy';
          this.copied = false;
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy text: ', err);
      });
    }
  }
};
</script>

<style scoped>
.copy-button {
  margin-left: 95%;
  background-color: #fff;
  border: none;
  padding: 0;
  border-radius: 1px;
  cursor: pointer;
  font-size: 0.8em;
}

.copy-button svg {
  margin-right: 5px;
}

.copy-button svg polyline {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: stroke-offset 0.5s ease forwards;
}

@keyframes stroke-offset {
  to {
    stroke-dashoffset: 0;
  }
}
</style>
